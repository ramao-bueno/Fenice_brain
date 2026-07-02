# Téo Empático + Loop de Aprendizado WOW — Design Spec

> **Fase 1 (Partes I+II): IMPLEMENTADA em 2026-07-02** — roteamento por intenção + modo
> descoberta live no IVR; tabela `fenice_tim_dialogos` + camada de reporting Power BI
> (views `vw_wow_*`, `vw_sfs_observatorio`). SFS = unidade própria. Parte III (loop de
> aprendizado) pendente — plano próprio quando houver massa de diálogos.

**Data:** 2026-07-02 · **Autor:** Ramão Bueno (Tech Lead) + Claude · **Status:** aprovado para plano

**Goal:** Fazer o Téo captar a intenção do usuário do jeito que ele quiser expressar
(sem nunca reenviar o modal na cara dele), acolhendo-o em um "modo descoberta" quando a
área não estiver clara — e, em paralelo, começar a **guardar os diálogos** para que a
Fenice aprenda com os próprios atendimentos e aprofunde o conceito WOW ao longo do tempo.

**Arquitetura:** Três frentes. (I) Roteamento empático na lógica de decisão do IVR
(`decidir_acao.js` + espelho no workflow N8N), com um novo estágio `descoberta` servido
por um prompt de acolhimento no Gemini. (II) Captura de cada turno de conversa em uma
tabela Supabase, ligada ao fluxo existente. (III) Loop de aprendizado: um processo
periódico que lê os diálogos, faz um brainstorm assistido por LLM e propõe melhorias
(palavras-chave, tom, template WOW) — sempre com humano no circuito, nunca auto-aplicado.

**Tech Stack:** N8N Cloud (IVR), Node.js (lógica testável + testes `node:test`),
Evolution API v2 (`fenice-tim-prod`), Gemini via `fenice_llm`, Supabase (Postgres),
Python (script de análise), Microsoft Graph (e-mail — já pronto).

## Global Constraints

- **JAMAIS perturbar o usuário:** card só na saudação inicial ou em `menu`; nunca em
  duplicata; descoberta é conversa fluida, não formulário; 1 resposta por mensagem.
- Persona **Téo — Intelligence Concierge**; nunca "assistente"/"bot"/"IA". Assinatura
  obrigatória `👤 *Teo — Intelligence Concierge*` / `© 2026 Fenice IT Justech.IA`.
- Nomenclatura de IA: nunca só "IA" — usar "com o auxílio das maiores plataformas de IA — CLAUDE & Open IA".
- Tratamento **Dr./Dra.**; RAG antes do Gemini; indicador de digitando; resposta pensada, nunca instantânea.
- Instância Evolution: **`fenice-tim-prod`**. Não alterar o workflow N8N sem mostrar o diff ao Ramão (regra #3).
- Segredos nunca vão ao git. Diálogos = PII → tratados sob LGPD (ver Parte II).
- N8N permanece o orquestrador central (não propor substituição).

---

# Parte I — Téo Empático (Fase 1)

## Árvore de decisão (ramo "sem área definida")

Substitui o atual `if (!areaAtual) return menu_principal`:

```
mensagem sem área (areaAtual == null) e não é opção de menu / reset / retomar:
  1. area = inferirArea(mensagem)           // palavras-chave de alta confiança
     ├─ se area != null           → _acao: "set_area" (entra na área, acolhe, SEM card)
  2. senão, se é só saudação        → _acao: "menu_principal" (mostra o card, entrada acolhedora)
  3. senão (tem conteúdo, área incerta) → _acao: "descoberta" (estágio "descoberta", Gemini acolhe)
```

No estágio `descoberta`, a cada nova mensagem:
```
  1. area = inferirArea(mensagem)
     ├─ se area != null → _acao: "set_area" (transição suave para a área)
  2. se é reset/menu    → _acao: "menu_principal"
  3. senão              → _acao: "descoberta" (continua acolhendo via Gemini)
```

## Componente: `inferirArea(mensagem)` — em `detectar_intencao.js`

Mapa termo→área, **só alta confiança** (ambíguo cai na descoberta de propósito):

```js
const AREA_KEYWORDS = {
  b2b:         ["tim", "corporativo", "operadora", "b2b", "plano da empresa", "plano corporativo"],
  academico:   ["faculdade", "estudar", "estudo", "prova", "concurso", "oab", "aula", "matéria", "materia", "univille"],
  observatorio:["monitorar", "monitoramento", "observatório", "observatorio", "acompanhar processo"],
  api:         ["api", "integração", "integracao", "webhook", "integrar sistema", "desenvolvedor"],
  juridico:    ["advogado", "processo judicial", "penal", "civil", "constitucional", "tributário",
                "tributario", "trabalhista", "dúvida jurídica", "duvida juridica", "petição", "peticao"],
  filosofia:   ["filosofia", "filosófico", "filosofico", "ética", "etica", "pensador", "existência", "existencia"],
};
// retorna a 1ª área cujo termo aparece na mensagem (lower, sem pontuação final), ou null.
// Empate/termo genérico ("direito", "lei", "sistema") NÃO entra no mapa — vai p/ descoberta.
```

Assinatura: `inferirArea(mensagem: string): string|null`. Determinístico, sem I/O.

## Componente: estágio `descoberta` + prompt de acolhimento (Gemini)

Novo valor de `estagio`. Não conta como `JA_CADASTRADO`. Não dispara convite de cadastro.

**System prompt do modo descoberta (Gemini):**
```
Você é o Téo, Intelligence Concierge da Fenice IT. O usuário ainda não disse claramente
o que precisa. Sua missão é acolher com calor e descobrir JUNTO com ele o que procura —
nunca pressione, nunca liste opções secas, nunca peça para "digitar um número".
Fale como um concierge atencioso: valide o que ele disse, faça 1 pergunta gentil que ajude
a entender a necessidade, e deixe claro que ele pode se expressar do jeito que quiser.
Máximo 3 linhas. Não use a palavra "IA" sozinha.
```

Primeira entrada no modo descoberta (quando ainda não há histórico) usa a mensagem-âncora:
> *"Fique totalmente à vontade — me conte com as suas palavras o que você procura, que a gente descobre juntos o melhor caminho."*

Toda resposta recebe o fecho WOW (assinatura) via o mesmo wrapper do nó 16b.

## Transição da descoberta → área

Quando `inferirArea` casa (em qualquer turno da descoberta), `_acao: set_area` com um
acolhimento de transição: *"Perfeito, Dr(a). {nome} — vou te ajudar com {área}."* seguido
da boas-vindas normal da área. Sem card.

## Não-perturbar (garantias desta parte)

- O card (`9a`) **só** dispara em `menu_principal` (saudação inicial / `menu` / reset).
  `set_area` e `descoberta` **nunca** enviam o card.
- Descoberta = no máximo 1 mensagem por mensagem do usuário; sem loop de modal.
- Se o Gemini falhar (timeout/erro), fallback = a mensagem-âncora de acolhimento (nunca o card, nunca silêncio no meio da conversa ativa).

## Arquivos (Parte I)

- Modificar: `scripts/n8n_logic/detectar_intencao.js` (+ `inferirArea`, `AREA_KEYWORDS`)
- Modificar: `scripts/n8n_logic/decidir_acao.js` (novo ramo sem-área + estágio `descoberta`)
- Modificar: `scripts/n8n_logic/detectar_intencao.test.js`, `decidir_acao.test.js` (novos casos)
- Modificar: `scripts/n8n_fenice_tim_v4.json` (espelhar lógica nos nós 2/7; novo ramo Gemini descoberta) — **diff ao Ramão antes de publicar**
- Modificar: `docs/superpowers/reports/2026-07-01-roteiro-teste-wow-whatsapp.md` (fase texto-livre)

## Testes (TDD — Parte I)

`inferirArea`: casa "quero estudar penal"→academico; "integração de api"→api;
"sobre a TIM"→b2b; "dúvida sobre filosofia"→filosofia; genérico "preciso de ajuda"→null;
vazio→null.
`decidirAcao` sem área: saudação "bom dia"→menu_principal; "quero estudar penal"→set_area(academico);
"me ajuda com uma coisa"→descoberta; em `descoberta` + "é sobre a OAB"→set_area(academico);
em `descoberta` + texto genérico→descoberta; `menu` em descoberta→menu_principal.

---

# Parte II — Captura de Diálogos (Fase 1b, junto com a I)

Começar a guardar desde já, para ter massa de dados quando a Parte III for construída.

## Modelo de dados: tabela `fenice_tim_dialogos` (Supabase)

| coluna | tipo | nota |
|---|---|---|
| id | bigint identity PK | |
| numero | text | telefone (liga a `fenice_tim_contatos.numero`) |
| ts | timestamptz default now() | momento do turno |
| direcao | text | `in` (usuário) \| `out` (Téo) |
| mensagem | text | conteúdo do turno |
| area | text | área no momento (ou `descoberta`/null) |
| estagio | text | estágio no momento |
| acao | text | `_acao` decidido (menu_principal, set_area, descoberta, responder, humano…) |
| intencao | text | intenção detectada (ou null) |

RLS ligada; acesso só via service key (server-side). Índice em `(numero, ts)`.

## Captura no workflow

Após o nó de decisão e após o envio da resposta, um nó `Log Diálogo` faz `INSERT`
(direcao=in para a mensagem recebida; direcao=out para a resposta do Téo). `continueOnFail`
ligado — logar **nunca** pode quebrar o atendimento nem atrasar a resposta ao usuário.

## Privacidade / LGPD

- Diálogos são PII → nunca vão ao git; ficam só no Supabase (service key).
- Finalidade declarada: melhoria do atendimento (WOW). Retenção a definir (sugestão: 180 dias).
- Anonimização na Parte III: a análise agrega/tira identificadores antes de virar relatório público.

## Arquivos (Parte II)

- Migração Supabase: cria `fenice_tim_dialogos` (via `apply_migration`).
- Modificar: `scripts/n8n_fenice_tim_v4.json` (nó `Log Diálogo`, `continueOnFail`).

---

# Parte III — Loop de Aprendizado WOW (Fase 2)

Objetivo: aprofundar o conceito WOW **a partir dos atendimentos reais**, com brainstorms
ocasionais assistidos por LLM — humano sempre no circuito.

## O que o loop aprende

1. **Frases que não rotearam** (caíram em descoberta e demoraram a resolver) → sugestões de
   novos termos para `AREA_KEYWORDS`.
2. **Descobertas que falharam** (usuário saiu sem achar a área) → onde o acolhimento perdeu.
3. **Causas de handoff** (o que levou ao humano / auto-intenção) → oportunidades de resposta.
4. **Demanda por área** (o que as pessoas mais procuram) → priorização de conteúdo/RAG.
5. **Tom & WOW** (onde as respostas soaram frias) → ajustes no template e nos prompts.

## Processo (`scripts/wow_learning/analisar_dialogos.py`)

```
1. Puxa diálogos recentes do Supabase (janela configurável, ex.: 7 dias), anonimizados.
2. Agrupa por sessão (numero + janela de tempo) e monta transcrições.
3. Envia para o LLM (chain Claude→OpenAI→Gemini via fenice_llm) um prompt de brainstorm WOW
   pedindo: padrões, falhas de roteamento, termos sugeridos, ajustes de tom — em JSON.
4. Passa pelo GIGO gate (check_source) — descarta ruído antes de virar sugestão.
5. Gera relatório em docs/superpowers/reports/AAAA-MM-DD-wow-aprendizado.md
   + atualiza uma memória de padrões WOW. NUNCA aplica em produção automaticamente:
   as sugestões de keyword/prompt viram um diff que o Ramão aprova (regra #3).
```

## Cadência

Manual sob demanda no início ("brainstorms ocasionais"); depois, opcional, um `monitor`
semanal (padrão dos monitores existentes, ex.: `monitor_bdsf.py`). Sem automação de escrita
em prod — só relatório + sugestão.

## Definição de WOW (aprofundamento — o norte do loop)

WOW = atendimento **HP UX** (High-Performance UX) + calor humano do concierge: (a) o usuário
se expressa como quiser e é entendido; (b) nunca é perturbado; (c) sente-se acolhido e
conduzido ("descobrir juntos"); (d) recebe contexto real (RAG) com tom Dr./Dra.; (e) cada
interação ensina o sistema a ser melhor na próxima. O loop da Parte III é o mecanismo que
transforma (e) em prática.

## Arquivos (Parte III)

- Criar: `scripts/wow_learning/analisar_dialogos.py` (+ teste com fixture de diálogos)
- Criar: `scripts/wow_learning/prompt_brainstorm_wow.md` (prompt versionado)
- Reusar: `scripts/llm-wiki/check_source.py` (GIGO), `fenice_llm.py` (chain)
- Saída: relatórios em `docs/superpowers/reports/` + memória de padrões WOW

---

## Estratégia de testes (global)

- **Parte I:** TDD nos dois arquivos JS (`node --test`). A lógica é pura e determinística.
- **Parte II:** teste da migração (colunas) + verificação de que o log tem `continueOnFail`
  (não quebra o fluxo). Teste vivo: 1 conversa → conferir linhas `in`/`out` no Supabase.
- **Parte III:** teste do analisador com fixture de diálogos sintéticos (sem PII) → valida
  o formato do relatório e o GIGO gate.
- **Vivo:** roteiro `2026-07-01-roteiro-teste-wow-whatsapp.md` + a nova fase texto-livre.

## Ordem de implementação

1. Parte I (TDD JS → workflow → diff → push → teste vivo).
2. Parte II junto (migração + nó de log) — para já acumular dados.
3. Parte III depois, quando houver massa de diálogos (fase 2, plano próprio).

## Self-review

- Placeholders: nenhum — keywords, schema, prompts e casos de teste estão concretos.
- Consistência: `descoberta` é estágio novo, não está em `JA_CADASTRADO` nem em `MENU_OPCOES`;
  card só em `menu_principal`; assinatura WOW em toda resposta.
- Escopo: 3 partes, mas I+II formam um plano coeso (Fase 1); III é plano separado (Fase 2).
- Ambiguidade: termos genéricos deliberadamente fora do mapa → descoberta (decisão de design).

*بِسْمِ اللهِ الرَّحْمَنِ الرَّحِيمِ · Fenice IT · Justech.IA*

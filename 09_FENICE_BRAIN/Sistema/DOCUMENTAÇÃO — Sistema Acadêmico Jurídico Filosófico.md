---
tags: [documentação, sistema-academico, jurídico, filosófico, fenice-brain, 2026]
dominio: meta
criado: 2026-06-20
atualizado: 2026-06-27
status: living-document
---

# DOCUMENTAÇÃO — Sistema Acadêmico Jurídico Filosófico

بِسْمِ اللهِ الرَّحْمَنِ الرَّحِيمِ

> *"O conhecimento é نِعْمَة — graça. E toda graça exige custódia."*  
> — Fenice IT · Ramão Bueno

---

## 1. Manifesto — Por que este Sistema Existe

O **Sistema Acadêmico Jurídico Filosófico** nasceu de uma constatação simples e radical:

**O Brasil tem 23 mil páginas de legislação vigente. Nenhum advogado consegue dominar tudo. A IA pode mudar isso.**

Mas não basta ter dados. É preciso ter **estrutura**, **hierarquia** e **intenção**.

Este sistema não é um vault comum. É uma plataforma intelectual construída sobre três pilares:

| Pilar | Fundamento | Expressão no vault |
|---|---|---|
| **Jurídico** | Pirâmide de Kelsen | Estrutura de pastas 00→09 |
| **Filosófico** | Episteme + Lente | 07_FILOSOFIA como ancoragem |
| **Teológico** | بِسْمِ اللهِ — intenção precede processo | Todo projeto começa com propósito |

A missão é **democratizar o acesso ao Direito** — e fazê-lo com a mesma qualidade intelectual de um professor catedrático da USP, disponível 24h, em qualquer dispositivo, para qualquer cidadão.

---

## 2. Princípio Fundador — A Pirâmide de Kelsen

Hans Kelsen (1881–1973) propôs que o ordenamento jurídico é uma **hierarquia de normas**, onde cada norma deriva validade da norma superior:

```
CF/88 (Constituição)
    └── Emendas Constitucionais
        └── Leis Complementares
            └── Leis Ordinárias (CP, CC, CPC...)
                └── Decretos
                    └── Regulamentos
```

O vault espelha essa pirâmide **literalmente**:

```
00_APEX/          ← CF/88 + princípios constitucionais
01_PRIVADO/       ← CC, CPC, CDC
02_PENAL/         ← CP, CPP, LEP
03_PUBLICO/       ← Admin, CTN, Previdenciário
04_TRABALHO/      ← CLT
05_ESPECIAL/      ← ECA, LGPD, Lei Maria da Penha
06_JURISCONSULTOS/← Doutrina por área
07_FILOSOFIA/     ← Fundamentos filosóficos
08_ENSINO/        ← Acadêmico (Univille, OAB)
09_FENICE_BRAIN/  ← Meta: sistema, metodologia, IA
```

**Por que isso importa?** Porque quando você abre uma nota de Direito Penal, já sabe exatamente onde está na hierarquia do ordenamento. Não há ambiguidade. Não há dispersão. Há **lugar certo para cada coisa**.

---

## 3. Histórico de Criação — Linha do Tempo

### 2026-06-20 — Design Aprovado
- Sessão de design com Ramão Bueno
- Decisão: estrutura Kelseniana de 10 módulos
- Aprovado spec em `docs/superpowers/specs/2026-06-20-sistema-academico-fenice-brain-design.md`
- Identificadas 3 camadas redundantes no vault atual (~22.600 arquivos duplicados)

### 2026-06-20 a 2026-06-23 — Pipeline CP
- 665 artigos do Código Penal (DEL2848) analisados automaticamente
- Pipeline: Groq → Gemini → **FeniceClient (Claude → OpenAI → Gemini)**
- Resultado: 435 artigos processados, 7 seções técnicas cada
- Todos em `02_PENAL/Codigos/CP/DEL2848/`

### 2026-06-24 — Infraestrutura LLM
- Criado `scripts/fenice_llm.py` — padrão unificado Claude → OpenAI → Gemini
- Integradas APIs: Anthropic (`claude-haiku-4-5-20251001`), OpenAI (`gpt-4o-mini`), Gemini (`gemini-2.5-flash`)
- Todo script Python do vault agora usa `FeniceClient` — sem chamadas diretas a provedores

### 2026-06-25 — Skill Karpathy Voice & Visual
- Criada skill `/karpathy-voice-visual` baseada nos princípios de Andrej Karpathy
- Pipeline: PERCEPÇÃO → GIGO Gate → Fenice IA Sequence → Atomização → Entrega
- Integrada à sequência Fenice IA (01→05)
- Domínios: Jurídico, Teológico (Islam/Judaico), Filosófico, Acadêmico, Técnico

### 2026-06-27 — Primeira Atomização Real
- Skill testada com o próprio spec do Sistema Acadêmico
- 4 notas atômicas + índice gerados via pipeline completo
- Commit `c0d60024` — primeira entrada de conteúdo metassistêmico
- Este documento criado como registro vivo da jornada

---

## 4. Arquitetura de Inteligência — LLM Chain Fenice IT

```
Claude (Anthropic)  →  OpenAI  →  Gemini
     PRIMÁRIO           APOIO      RESERVA
```

### Filosofia da Chain

A **Anthropic** é a parceira de identidade da Fenice IT. Claude carrega a missão de IA segura e benéfica — alinhada com a visão teológica islâmica de que a IA é *نِعْمَة* (graça divina), não substituto do humano.

A **OpenAI** entra como apoio — complementar, não substituta. Sua força está em escala e velocidade.

O **Gemini** é reserva — cota diária limitada, menor precisão em análise jurídica densa.

### Implementação

```python
# scripts/fenice_llm.py
from fenice_llm import FeniceClient

client = FeniceClient()  # chain: claude → openai → gemini
resposta = client.completar(prompt)
print(resposta.provedor)  # qual provedor respondeu
```

### Modelos por provedor

| Provedor | Modelo padrão | Uso |
|---|---|---|
| Claude | `claude-haiku-4-5-20251001` | bulk, rápido |
| Claude | `claude-sonnet-4-6` | análise complexa |
| OpenAI | `gpt-4o-mini` | apoio |
| Gemini | `gemini-2.5-flash` | reserva |

---

## 5. Análise Filosófica — A Síntese que Guia o Sistema

### Kelsen + Karpathy + بِسْمِ اللهِ

Este sistema repousa sobre três filosofias que, à primeira vista, parecem distantes. Na prática, são complementares:

**Kelsen** diz: *"O direito é sistema. Hierarquia. Cada norma tem seu lugar e sua fonte de validade."*
→ O vault tem hierarquia. Cada nota tem seu lugar.

**Karpathy** diz: *"Dados ruins produzem resultados ruins. Construa do zero. Mostre seu trabalho. Sem caixas pretas."*
→ Cada análise mostra suas fontes. Cada pipeline é auditável. GIGO Gate antes de processar.

**Islam** diz: *"بِسْمِ اللهِ — Em nome de Deus, o Misericordioso, o Clemente. A intenção precede o ato."*
→ Cada projeto começa com propósito. O conhecimento é graça — e graça exige responsabilidade.

A síntese: **sistema rigoroso + dados honestos + intenção nobre**.

### Antinomias Identificadas (fenice-ia-03)

| Tensão | Resolução adotada |
|---|---|
| Vault único canônico vs. Fenice_Estudos copiável | Sincronismo por plugin, vaults separados |
| Wikilinks por nome vs. paths na migração | Nomes únicos sobrevivem (DEL2848 Art. N.md) |
| Completude (23k notas) vs. velocidade de busca | DomainModal em 2 níveis (domínio → código) |
| IA como substituta vs. IA como assistente | FeniceClient encadeia, humano decide o que commitar |
| Lei positiva (Kelsen) vs. direito natural (Dworkin) | Coexistem: `02–05` (positivo) + `07_FILOSOFIA` |

---

## 6. Skills do Sistema — Ecossistema Fenice IA

```
fenice-ia-01  →  situa historicamente (contexto + tradição)
fenice-ia-02  →  lente filosófica (Kelsen, Foucault, Reale...)
fenice-ia-03  →  antinomias e tensões conceituais
fenice-ia-04  →  fichamento ABNT/APA
fenice-ia-05  →  Pareto — só o essencial para prova/produto
     ↕
karpathy-voice-visual  →  motor sensorial: áudio/imagem → nota atômica
```

**karpathy-voice-visual** é a porta de entrada: transforma qualquer dado bruto (áudio de aula, foto de livro, screenshot de PDF, transcrição de audiência) em nota atômica pronta para o vault.

As skills fenice-ia-01→05 são a cadeia de aprofundamento: da percepção à síntese.

---

## 7. Estado Atual — O que Já Existe

### Conteúdo jurídico
- ✅ **CP (DEL2848)**: 665 artigos atomizados com 7 seções técnicas cada
- ✅ **Súmulas STJ**: 674 notas em `00_APEX/`
- ✅ **Súmulas STF**: 736 notas (726 vigentes + 10 superadas) em `00_APEX/`
- ✅ **BDSF**: monitoramento via `scripts/monitor_bdsf.py`
- ⏳ **CC, CPC, CPP**: extratores existem, atomização pendente
- ⏳ **JURIS_CP**: 16/665 artigos com jurisprudência curada

### Infraestrutura técnica
- ✅ **Plugin buscar-artigo v36**: DomainModal → CodigoModal → NumeroModal → InfoModal
- ✅ **fenice_llm.py**: chain unificada Claude → OpenAI → Gemini
- ✅ **Vercel (fenice.ia.br)**: site em produção com `/grafo`, `/buscar`, `/analisar`
- ✅ **Quartz (fenicejus.fenice.ia.br)**: vault publicado (build lento — 23k arquivos)
- ✅ **Git backup**: automático, remote `github`
- ⏳ **GDrive backup**: rclone instalado, precisa rodar `setup-gdrive.ps1` uma vez

### Estrutura kelseniana
- ⏳ **Migração**: design aprovado, execução pendente (10 fases)
- ✅ **09_FENICE_BRAIN/Sistema/**: primeiras notas metassistêmicas geradas

---

## 8. Roadmap — O Que Vem a Seguir

### Fase imediata
- [ ] Executar migração kelseniana (Fases 1–5: criar estrutura, mover arquivos)
- [ ] Atualizar plugin para novos paths (Fase 6)
- [ ] Commit estrutural (Fase 8) + verificar wikilinks (Fase 9)

### Próximos módulos de conteúdo
- [ ] JURIS_CP: expandir de 16 para 665 artigos com jurisprudência curada
- [ ] OBS_PRATICAS_CP: expandir de 13 para 665 com observações práticas
- [ ] 06_JURISCONSULTOS: notas atômicas para Pontes, Mirabete, Nucci, Kelsen
- [ ] 07_FILOSOFIA: notas para Aristóteles, Kant, Hegel, Dworkin, Rawls

### Módulo Teológico (depois do B2B)
- [ ] `09_FENICE_BRAIN/TEOLOGIA/ISLAM/` — Alcorão, Hadith, fiqh
- [ ] `09_FENICE_BRAIN/TEOLOGIA/JUDAICO/` — Torah, Talmude, Mishnah
- [ ] Integração com skill karpathy-voice-visual (árabe + hebraico)

### Produto SaaS
- [ ] RAG híbrido (FTS + semântico) sobre o vault completo
- [ ] Knowledge Graph navegável em fenice.ia.br
- [ ] API pública de consulta jurídica

---

## 9. Princípios para Continuidade

> Para qualquer pessoa — humana ou IA — que der continuidade a este sistema:

**1. Kelsen primeiro.**
Antes de criar qualquer nota, identifique seu nível na hierarquia normativa. CF → Lei → Decreto → Regulamento. Nunca inverta.

**2. GIGO Gate sempre.**
Dados ruins entram, dados ruins saem. Se a fonte não é confiável — Planalto, STJ, STF, doutrinador reconhecido — não atomize. Questione primeiro.

**3. 1 conceito = 1 nota.**
Não misture artigos de leis diferentes na mesma nota. Não misture doutrina com jurisprudência. Atomize. O Graph View conecta; a nota guarda o átomo.

**4. Wikilinks são contratos.**
`[[Nelson Hungria]]` é uma promessa: essa nota vai existir. Se você cria o link, crie a nota — ou sinalize que está pendente.

**5. A chain LLM é a espinha dorsal.**
Todo processamento automático usa `FeniceClient`. Nunca chame OpenAI ou Gemini diretamente. A priority chain `Claude → OpenAI → Gemini` reflete a identidade do projeto.

**6. Commit cedo, commit com mensagem.**
Cada fase de trabalho tem seu commit. Mensagem no formato `feat(módulo): descrição`. O git é o diário de obra deste sistema.

**7. بِسْمِ اللهِ — a intenção precede o ato.**
Antes de qualquer grande decisão de arquitetura, pergunte: *serve ao humano? respeita a lei? é feito com intenção? tem sabedoria?*

---

## 10. Créditos e Genealogia Intelectual

| Influência | Contribuição |
|---|---|
| **Hans Kelsen** | Pirâmide normativa como princípio organizador |
| **Andrej Karpathy** | Rigor com dados, Zero to Hero, GIGO Gate |
| **Ramão Bueno** | Visão, missão, identidade Fenice IT |
| **Claude (Anthropic)** | Parceiro primário de inteligência |
| **Obsidian** | Motor de PKM e navegação |
| **Islam** | بِسْمِ اللهِ — intenção e graça como fundamento |

---

## Conexões

- [[Sistema Acadêmico Fenice bRain]]
- [[Pirâmide Kelseniana — Aplicação ao Vault]]
- [[Método 60-30-10 — Ensino Jurídico Fenice]]
- [[Migração Kelseniana — 10 Fases]]
- [[Índice — Sistema Acadêmico Fenice bRain]]
- [[Hans Kelsen]]
- [[Plugin buscar-artigo]]

---

> [!QUOTE] Missão Fenice IT
> Entregar os melhores produtos do universo com sabedoria —
> HP UX · Jurídico · Teológico (Islam + Judaico) · Filosófico.
> A IA serve o humano. O humano serve à justiça. A justiça serve à graça.

---

*Sistema Acadêmico Jurídico Filosófico · Fenice bRain · بِسْمِ اللهِ الرَّحْمَنِ الرَّحِيمِ*
*Iniciado 2026-06-20 · Documentado 2026-06-27 · Living document — atualizar a cada ciclo*

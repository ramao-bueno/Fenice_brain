# Téo Empático (Fase 1) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fazer o Téo rotear o usuário pela intenção em texto livre e acolhê-lo em "modo descoberta" quando a área não estiver clara — sem nunca reenviar o modal — e começar a guardar os diálogos no Supabase.

**Arquitetura:** Lógica pura e testável em `scripts/n8n_logic/*.js` (fonte da verdade, com testes `node:test`), espelhada nos nós de código do workflow N8N via script de patch idempotente (padrão `patch_push_leads.py`). Novo estágio `descoberta` servido por um ramo Gemini de acolhimento. Captura de diálogos em tabela Supabase com log `continueOnFail`.

**Tech Stack:** Node.js (`node:test`), N8N Cloud API v1, Evolution API v2 (`fenice-tim-prod`), Gemini, Supabase (Postgres), Python (patch scripts).

## Global Constraints

- JAMAIS perturbar: card só em `menu_principal`; `set_area` e `descoberta` nunca enviam card; 1 resposta por mensagem.
- Persona Téo — Intelligence Concierge; nunca "assistente"/"bot"/"IA". Assinatura `👤 *Teo — Intelligence Concierge*` / `© 2026 Fenice IT Justech.IA`.
- Nunca escrever só "IA": usar "com o auxílio das maiores plataformas de IA — CLAUDE & Open IA".
- Tratamento Dr./Dra.; RAG antes do Gemini; indicador de digitando.
- Instância Evolution: `fenice-tim-prod`. Não alterar workflow N8N sem mostrar o diff ao Ramão (regra #3). Backup live antes de todo PUT. PUT usa `settings` mínimo `{"executionOrder":"v1","saveManualExecutions":true}`.
- Segredos nunca ao git; diálogos = PII (só Supabase, service key).
- N8N permanece o orquestrador (não remover/substituir).

---

### Task 1: `inferirArea()` — roteamento por palavra-chave

**Files:**
- Modify: `scripts/n8n_logic/detectar_intencao.js`
- Test: `scripts/n8n_logic/detectar_intencao.test.js`

**Interfaces:**
- Produces: `inferirArea(mensagem: string): string|null` e `AREA_KEYWORDS` (exportados). Retorna a chave de área (`b2b|academico|observatorio|api|juridico|filosofia`) do 1º termo que casar, ou `null`.

- [ ] **Step 1: Escrever os testes que falham**

Adicionar ao fim de `scripts/n8n_logic/detectar_intencao.test.js`:
```js
const { inferirArea } = require("./detectar_intencao");

test("inferirArea roteia estudo -> academico", () => {
  assert.strictEqual(inferirArea("quero estudar penal para a prova"), "academico");
});
test("inferirArea roteia api -> api", () => {
  assert.strictEqual(inferirArea("preciso de integração de api"), "api");
});
test("inferirArea roteia tim -> b2b", () => {
  assert.strictEqual(inferirArea("é sobre a TIM corporativa"), "b2b");
});
test("inferirArea roteia filosofia -> filosofia", () => {
  assert.strictEqual(inferirArea("uma dúvida de filosofia"), "filosofia");
});
test("inferirArea termo genérico -> null", () => {
  assert.strictEqual(inferirArea("preciso de uma ajuda"), null);
});
test("inferirArea vazio -> null", () => {
  assert.strictEqual(inferirArea(""), null);
});
```

- [ ] **Step 2: Rodar e ver falhar**

Run: `node --test scripts/n8n_logic/detectar_intencao.test.js`
Expected: FAIL (`inferirArea is not a function`).

- [ ] **Step 3: Implementar**

Adicionar em `scripts/n8n_logic/detectar_intencao.js` (antes do `module.exports`):
```js
const AREA_KEYWORDS = {
  b2b:          ["tim", "corporativo", "operadora", "b2b", "plano da empresa", "plano corporativo"],
  academico:    ["faculdade", "estudar", "estudo", "prova", "concurso", "oab", "aula", "matéria", "materia", "univille"],
  observatorio: ["monitorar", "monitoramento", "observatório", "observatorio", "acompanhar processo"],
  api:          ["api", "integração", "integracao", "webhook", "integrar sistema", "desenvolvedor"],
  juridico:     ["advogado", "processo judicial", "penal", "civil", "constitucional", "tributário",
                 "tributario", "trabalhista", "dúvida jurídica", "duvida juridica", "petição", "peticao"],
  filosofia:    ["filosofia", "filosófico", "filosofico", "ética", "etica", "pensador", "existência", "existencia"],
};

function inferirArea(mensagem) {
  const m = (mensagem || "").toLowerCase();
  for (const [area, termos] of Object.entries(AREA_KEYWORDS)) {
    if (termos.some((t) => m.includes(t))) return area;
  }
  return null;
}
```
E atualizar o export:
```js
module.exports = { detectarIntencao, SINAIS_INTENCAO, inferirArea, AREA_KEYWORDS };
```

- [ ] **Step 4: Rodar e ver passar**

Run: `node --test scripts/n8n_logic/detectar_intencao.test.js`
Expected: PASS (todos, inclusive os 5 antigos).

- [ ] **Step 5: Commit**
```bash
git add scripts/n8n_logic/detectar_intencao.js scripts/n8n_logic/detectar_intencao.test.js
git commit -m "feat(teo): inferirArea roteia texto livre por palavra-chave"
```

---

### Task 2: `isSaudacao()` — distinguir cumprimento puro

**Files:**
- Modify: `scripts/n8n_logic/detectar_intencao.js`
- Test: `scripts/n8n_logic/detectar_intencao.test.js`

**Interfaces:**
- Consumes: nada.
- Produces: `isSaudacao(mensagem: string): boolean` (exportado). `true` quando a mensagem é essencialmente só um cumprimento.

- [ ] **Step 1: Escrever os testes que falham**

Adicionar em `detectar_intencao.test.js`:
```js
const { isSaudacao } = require("./detectar_intencao");

test("isSaudacao reconhece bom dia", () => {
  assert.strictEqual(isSaudacao("bom dia"), true);
});
test("isSaudacao reconhece oi/ola", () => {
  assert.strictEqual(isSaudacao("oi"), true);
  assert.strictEqual(isSaudacao("olá!"), true);
});
test("isSaudacao reconhece salam", () => {
  assert.strictEqual(isSaudacao("salam"), true);
});
test("isSaudacao NÃO dispara em pedido com conteúdo", () => {
  assert.strictEqual(isSaudacao("preciso de ajuda com um processo"), false);
});
```

- [ ] **Step 2: Rodar e ver falhar**

Run: `node --test scripts/n8n_logic/detectar_intencao.test.js`
Expected: FAIL (`isSaudacao is not a function`).

- [ ] **Step 3: Implementar**

Adicionar em `detectar_intencao.js`:
```js
const SAUDACOES = ["oi", "ola", "olá", "opa", "oie", "e ai", "eai", "hey", "hi",
  "bom dia", "boa tarde", "boa noite", "salam", "salaam", "as salamu alaikum", "saudações", "saudacoes"];

function isSaudacao(mensagem) {
  const m = (mensagem || "").toLowerCase().replace(/[!.?,]+$/g, "").trim();
  if (!m) return false;
  if (SAUDACOES.includes(m)) return true;
  // começa com saudação e é curta (≤ 3 palavras): "bom dia téo"
  const inicioSaudacao = SAUDACOES.some((s) => m.startsWith(s));
  return inicioSaudacao && m.split(/\s+/).length <= 3;
}
```
Atualizar export:
```js
module.exports = { detectarIntencao, SINAIS_INTENCAO, inferirArea, AREA_KEYWORDS, isSaudacao, SAUDACOES };
```

- [ ] **Step 4: Rodar e ver passar**

Run: `node --test scripts/n8n_logic/detectar_intencao.test.js`
Expected: PASS.

- [ ] **Step 5: Commit**
```bash
git add scripts/n8n_logic/detectar_intencao.js scripts/n8n_logic/detectar_intencao.test.js
git commit -m "feat(teo): isSaudacao distingue cumprimento puro de pedido"
```

---

### Task 3: `decidirAcao` — ramo empático (set_area por inferência + descoberta)

**Files:**
- Modify: `scripts/n8n_logic/decidir_acao.js:42-43` (o `if (!areaAtual) return menu_principal`)
- Test: `scripts/n8n_logic/decidir_acao.test.js`

**Interfaces:**
- Consumes: `inferirArea`, `isSaudacao` de `./detectar_intencao`.
- Produces: `decidirAcao` passa a emitir `_acao: "descoberta"` (com `estagio: "descoberta"`, `areaAtual: null`) e `_acao: "set_area"` (via inferência). Estágio `descoberta` não está em `JA_CADASTRADO`.

- [ ] **Step 1: Escrever os testes que falham**

Adicionar em `decidir_acao.test.js`:
```js
test("saudacao pura sem area mostra menu", () => {
  const r = decidirAcao({ numero: "55", nome: "X", mensagem: "bom dia" }, null, T0);
  assert.strictEqual(r._acao, "menu_principal");
});
test("texto livre com area inferida entra na area sem card", () => {
  const r = decidirAcao({ numero: "55", nome: "X", mensagem: "quero estudar penal" }, null, T0);
  assert.strictEqual(r._acao, "set_area");
  assert.strictEqual(r.areaAtual, "academico");
});
test("texto livre incerto vai para descoberta", () => {
  const r = decidirAcao({ numero: "55", nome: "X", mensagem: "preciso de uma ajuda" }, null, T0);
  assert.strictEqual(r._acao, "descoberta");
  assert.strictEqual(r.estagio, "descoberta");
});
test("em descoberta, area fica clara e transiciona", () => {
  const c = { area: null, estagio: "descoberta", ultimo_contato: T0.toISOString() };
  const r = decidirAcao({ numero: "55", nome: "X", mensagem: "é sobre a OAB" }, c, T0);
  assert.strictEqual(r._acao, "set_area");
  assert.strictEqual(r.areaAtual, "academico");
});
test("em descoberta, texto ainda incerto continua descoberta", () => {
  const c = { area: null, estagio: "descoberta", ultimo_contato: T0.toISOString() };
  const r = decidirAcao({ numero: "55", nome: "X", mensagem: "não sei bem" }, c, T0);
  assert.strictEqual(r._acao, "descoberta");
});
test("menu em descoberta volta ao card", () => {
  const c = { area: null, estagio: "descoberta", ultimo_contato: T0.toISOString() };
  const r = decidirAcao({ numero: "55", nome: "X", mensagem: "menu" }, c, T0);
  assert.strictEqual(r._acao, "menu_principal");
});
```

- [ ] **Step 2: Rodar e ver falhar**

Run: `node --test scripts/n8n_logic/decidir_acao.test.js`
Expected: FAIL (retorna `menu_principal` onde se espera `set_area`/`descoberta`).

- [ ] **Step 3: Implementar**

Em `scripts/n8n_logic/decidir_acao.js`, trocar o import da linha 1:
```js
const { detectarIntencao, inferirArea, isSaudacao } = require("./detectar_intencao");
```
E substituir o bloco `if (!areaAtual) return { ... _acao: "menu_principal" ... };` (atual linhas 42-43) por:
```js
  if (!areaAtual) {
    const areaInferida = inferirArea(mensagem);
    if (areaInferida)
      return { ...base, _acao: "set_area", areaAtual: areaInferida, msgCount: 0 };
    if (isSaudacao(mensagem))
      return { ...base, _acao: "menu_principal", areaAtual: null, msgCount: 0 };
    return { ...base, _acao: "descoberta", estagio: "descoberta", areaAtual: null };
  }
```
Nota: `isReset` já é tratado antes (linha 35), então `menu` em descoberta cai no reset → `menu_principal` (o teste "menu em descoberta" passa por lá).

- [ ] **Step 4: Rodar e ver passar**

Run: `node --test scripts/n8n_logic/decidir_acao.test.js`
Expected: PASS (16 testes — 10 antigos + 6 novos). Rode também `node --test scripts/n8n_logic/*.test.js`.

- [ ] **Step 5: Commit**
```bash
git add scripts/n8n_logic/decidir_acao.js scripts/n8n_logic/decidir_acao.test.js
git commit -m "feat(teo): decidirAcao roteia por intenção e acolhe em descoberta"
```

---

### Task 4: Espelhar a lógica no workflow + ramo Gemini de descoberta

**Files:**
- Create: `scripts/teo_empatico/patch_descoberta.py`
- Modify (via patch, live): workflow IVR `n8n_fenice_tim_v4.json` (ID `UKfz7lxQTQcnbOMV`) — nós de decisão (2/7) e Switch por Ação (8); novo nó Gemini descoberta + envio Evolution.

**Interfaces:**
- Consumes: lógica das Tasks 1-3 (a fonte JS).
- Produces: workflow live com `_acao: "descoberta"` roteado a um nó que chama o Gemini com o system prompt de acolhimento e envia via `fenice-tim-prod`.

- [ ] **Step 1: Ler a estrutura atual dos nós de decisão e do Switch**

Run: inspecionar `n8n_fenice_tim_v4.json` — nós "2. Extrair e Normalizar", "7. Decidir Próxima Ação", "8. Switch por Ação" (saídas/valores), e o nó Gemini existente (para reusar URL/modelo). Anotar como o `_acao` roteia no Switch.
Expected: entender onde inserir a saída `descoberta`.

- [ ] **Step 2: Escrever o patch (espelha a lógica JS nos jsCode dos nós 2/7)**

Em `scripts/teo_empatico/patch_descoberta.py` (modelar em `scripts/wow_leads/patch_push_leads.py`: `_env`, `call`, backup live, PUT com settings mínimo, verify):
- Substituir, no `jsCode` dos nós que contêm o ramo `!areaAtual → menu_principal`, pelo ramo empático das Tasks 1-3 (inferirArea + AREA_KEYWORDS + isSaudacao + SAUDACOES embutidos no jsCode, pois o nó não faz `require`).
- Adicionar saída `descoberta` no nó "8. Switch por Ação".
- Adicionar nó "9e. Gemini Descoberta" (httpRequest ao mesmo endpoint Gemini do nó existente) com system prompt:
  ```
  Você é o Téo, Intelligence Concierge da Fenice IT. O usuário ainda não disse claramente
  o que precisa. Acolha com calor e descubra JUNTO com ele o que procura — nunca pressione,
  nunca liste opções secas, nunca peça para "digitar um número". Valide o que ele disse,
  faça 1 pergunta gentil e deixe claro que ele pode se expressar do jeito que quiser.
  Máximo 3 linhas. Não use a palavra "IA" sozinha.
  ```
- Encadear "9e" → nó de envio Evolution (`sendText`, `fenice-tim-prod`) com wrapper de assinatura (mesmo do 16b). Fallback (Gemini erro/`continueOnFail`): enviar a âncora "Fique totalmente à vontade — me conte com as suas palavras o que você procura, que a gente descobre juntos o melhor caminho." + assinatura.

- [ ] **Step 3: Mostrar o diff ao Ramão (regra #3) e aguardar OK**

Run: `python scripts/teo_empatico/patch_descoberta.py --dry-run` (imprime nós adicionados/alterados sem PUT).
Expected: Ramão aprova o diff antes do push.

- [ ] **Step 4: Aplicar e verificar**

Run: `python scripts/teo_empatico/patch_descoberta.py`
Expected: `[PUT] 200`, `active=True`, verify confirma saída `descoberta` no Switch e nó `9e` presente. Backup `_backup_n8n_v4_LIVE_*.json` gravado.

- [ ] **Step 5: Teste vivo (WhatsApp)**

Enviar ao Téo (5547991041414): `bom dia` (→ modal), depois `quero estudar penal` (→ entra Acadêmico, sem card), depois em outra conversa `preciso de uma ajuda` (→ acolhimento descoberta, sem card). Conferir tom + assinatura + que o card NÃO se repete.

- [ ] **Step 6: Commit**
```bash
git add scripts/teo_empatico/patch_descoberta.py scripts/n8n_fenice_tim_v4.json
git commit -m "feat(teo): ramo descoberta no IVR + roteamento por intenção (live)"
```

---

### Task 5: Tabela de diálogos no Supabase (Parte II)

**Files:**
- Create: migração via `mcp__supabase__apply_migration` (nome `create_fenice_tim_dialogos`).

**Interfaces:**
- Produces: tabela `public.fenice_tim_dialogos` com colunas `id, numero, ts, direcao, mensagem, area, estagio, acao, intencao` + índice `(numero, ts)` + RLS on.

- [ ] **Step 1: Aplicar a migração**

Via `apply_migration` (nome `create_fenice_tim_dialogos`):
```sql
create table if not exists public.fenice_tim_dialogos (
  id bigint generated always as identity primary key,
  numero text not null,
  ts timestamptz not null default now(),
  direcao text not null check (direcao in ('in','out')),
  mensagem text,
  area text,
  estagio text,
  acao text,
  intencao text
);
create index if not exists idx_dialogos_numero_ts on public.fenice_tim_dialogos (numero, ts);
alter table public.fenice_tim_dialogos enable row level security;
```

- [ ] **Step 2: Verificar as colunas**

Run (via `execute_sql`):
```sql
select column_name from information_schema.columns
where table_schema='public' and table_name='fenice_tim_dialogos' order by ordinal_position;
```
Expected: `id, numero, ts, direcao, mensagem, area, estagio, acao, intencao`.

- [ ] **Step 3: Commit (registro da migração)**

Salvar o SQL em `scripts/teo_empatico/migration_dialogos.sql` e:
```bash
git add scripts/teo_empatico/migration_dialogos.sql
git commit -m "feat(wow): tabela fenice_tim_dialogos (captura de diálogos, LGPD)"
```

---

### Task 6: Nó `Log Diálogo` no workflow (captura, continueOnFail)

**Files:**
- Create: `scripts/teo_empatico/patch_log_dialogo.py`
- Modify (via patch, live): workflow IVR — nó `Log Diálogo` (Supabase REST insert), `continueOnFail`.

**Interfaces:**
- Consumes: tabela da Task 5; dados de decisão (numero, area, estagio, _acao, intencao) e a mensagem.
- Produces: cada turno logado (`in` na entrada, `out` na resposta). Log nunca bloqueia/atrasa a resposta.

- [ ] **Step 1: Escrever o patch**

Em `scripts/teo_empatico/patch_log_dialogo.py` (mesmo padrão de backup/PUT/verify):
- Adicionar nó httpRequest `Log Diálogo (in)` logo após o nó de decisão: `POST {SUPABASE_URL}/rest/v1/fenice_tim_dialogos` com header `apikey`/`Authorization: Bearer {service_key}`, `Prefer: return=minimal`, body `{numero, direcao:"in", mensagem, area, estagio, acao, intencao}`. `onError: continueRegularOutput` (continueOnFail).
- Adicionar `Log Diálogo (out)` após os nós de envio, body `{numero, direcao:"out", mensagem: <texto enviado>}`, também `continueOnFail`.
- Chaves Supabase lidas do `.env` no patch (nunca hardcode no git); no nó ficam como no padrão herdado (texto plano no workflow live, igual Evolution apikey).

- [ ] **Step 2: Dry-run + diff ao Ramão (regra #3)**

Run: `python scripts/teo_empatico/patch_log_dialogo.py --dry-run`
Expected: mostra os 2 nós de log e o rewire; Ramão aprova.

- [ ] **Step 3: Aplicar e verificar**

Run: `python scripts/teo_empatico/patch_log_dialogo.py`
Expected: `[PUT] 200`, `active=True`, verify acha os nós `Log Diálogo` com `continueOnFail=true`.

- [ ] **Step 4: Teste vivo + conferir Supabase**

Enviar 1 conversa curta ao Téo. Depois (via `execute_sql`):
```sql
select direcao, area, estagio, acao, left(mensagem,40) from public.fenice_tim_dialogos
where numero = '5547991041414' order by ts desc limit 6;
```
Expected: linhas `in`/`out` da conversa.

- [ ] **Step 5: Commit**
```bash
git add scripts/teo_empatico/patch_log_dialogo.py scripts/n8n_fenice_tim_v4.json
git commit -m "feat(wow): nó Log Diálogo captura conversas (continueOnFail)"
```

---

### Task 7: Atualizar roteiro de teste + status do spec

**Files:**
- Modify: `docs/superpowers/reports/2026-07-01-roteiro-teste-wow-whatsapp.md`
- Modify: `docs/superpowers/specs/2026-07-02-teo-empatico-wow-learning-design.md` (marcar Fase 1 concluída)

- [ ] **Step 1: Adicionar a fase "texto livre" ao roteiro**

Substituir o "Ponto de atenção" da Fase 1 por uma fase de teste real:
```markdown
### Fase 1b — Texto livre (empatia)
- 📲 `quero estudar penal` (sem número) → entra em Acadêmico, SEM card.
- 📲 `preciso de uma ajuda` → acolhimento descoberta, SEM card; Téo convida a falar à vontade.
- 📲 na sequência, `é sobre a OAB` → transiciona suave para Acadêmico.
- 🚫 Não-perturbar: o card NUNCA se repete nessas trocas.
```

- [ ] **Step 2: Marcar Fase 1 concluída no spec**

Adicionar no topo do spec: `> **Fase 1 (Partes I+II): implementada em 2026-…** — Parte III pendente.`

- [ ] **Step 3: Commit + push duplo**
```bash
git add docs/superpowers/reports/2026-07-01-roteiro-teste-wow-whatsapp.md docs/superpowers/specs/2026-07-02-teo-empatico-wow-learning-design.md
git commit -m "docs(teo): roteiro fase texto-livre + Fase 1 concluída no spec"
git push github main && git push fenice-justech main
```

---

## Self-Review

**Cobertura do spec (Fase 1):** Parte I → Tasks 1-4 (inferirArea, isSaudacao, decidirAcao, workflow+Gemini descoberta). Parte II → Tasks 5-6 (tabela + log). Roteiro/status → Task 7. Parte III é plano separado (fase 2) — fora deste plano por decisão de escopo.

**Placeholders:** nenhum nos passos de código JS/SQL (código completo). Task 4/6 dependem de ler a estrutura viva do workflow no Step 1 (inerente a patch de N8N), mas a lógica a inserir e o system prompt estão concretos.

**Consistência de tipos:** `inferirArea`/`isSaudacao` (Tasks 1-2) são consumidos por `decidirAcao` (Task 3) com as mesmas assinaturas; `_acao: "descoberta"` (Task 3) é o que o Switch da Task 4 roteia; colunas da Task 5 batem com o body do log da Task 6.

*بِسْمِ اللهِ الرَّحْمَنِ الرَّحِيمِ · Fenice IT · Justech.IA*

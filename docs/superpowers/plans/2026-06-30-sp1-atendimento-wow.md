# SP-1 · Motor de Atendimento WOW — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Consolidar o motor de atendimento WOW (N8N + Evolution + Gemini + RAG) para converter visitante desconhecido em prospect quente entregue ao Ramão.

**Architecture:** A lógica de roteamento e detecção de intenção é extraída para módulos JavaScript independentes e testáveis (`scripts/n8n_logic/`), depois embutida nos nós Code do workflow N8N. O e-mail WOW migra para Microsoft Graph API. Um script Python importa a carteira Farmer para o Supabase.

**Tech Stack:** N8N (workflow JSON), Node.js `node:test` (testes da lógica JS), Evolution API, Gemini 2.5 Flash, Supabase (PostgREST), Microsoft Graph API, Python 3 + httpx (import carteira).

## Global Constraints

- Menu: **6 opções** — `1=b2b 2=academico 3=observatorio 4=api 5=juridico 6=filosofia 0=humano`. Copiar verbatim.
- Persona: **Téo — Intelligence Concierge**. Nunca "assistente"/"bot"/"IA".
- Assinatura obrigatória: `👤 *Teo — Intelligence Concierge*` + `© 2026 Fenice IT Justech.IA`.
- Toda mensagem nova do bot DEVE conter um BOT_SIG: `["🏛️", "© 2026", "👤 *Atendimento", "Atendimento encerrado", "🎬 *"]`.
- Número corporativo/admin/handoff: `5547991041414`. `554797348385` NÃO existe.
- Captura apenas 4 campos: `nome`, `telefone`, `email`, `assunto`. Nunca CPF/endereço.
- Timeout de inatividade: `60` minutos. Palavra de retomada: `retomar`. Palavra de saída: `sair`.
- E-mail via **Microsoft Graph API** (`/sendMail`), nó com `continueOnFail: true`.
- Formato de telefone: `55` + DDD + número (13 dígitos com o 9, ex: `5547991041414`).
- Cobrança/BKO/CPF = fora de escopo (TIM).

---

### Task 1: Lógica de Decisão de Ação (módulo testável)

**Files:**
- Create: `scripts/n8n_logic/decidir_acao.js`
- Create: `scripts/n8n_logic/detectar_intencao.js`
- Test: `scripts/n8n_logic/decidir_acao.test.js`

**Interfaces:**
- Produces: `decidirAcao(dadosMsg, contato, agora?) → { _acao, numero, nome, mensagem, areaAtual, msgCount, estagio }`. `_acao ∈ {menu_principal, humano, set_area, responder, cadastro_invite, processar_cadastro, inatividade}`.
- Produces: `detectarIntencao(mensagem) → boolean`.
- Consumes (Task 3): ambos os módulos são inlinados nos nós Code do workflow.

- [ ] **Step 1: Write the failing test**

Create `scripts/n8n_logic/decidir_acao.test.js`:
```js
const test = require("node:test");
const assert = require("node:assert");
const { decidirAcao } = require("./decidir_acao");

const T0 = new Date("2026-06-30T12:00:00Z");

test("novo contato sem area vai ao menu", () => {
  const r = decidirAcao({ numero: "55", nome: "X", mensagem: "oi" }, null, T0);
  assert.strictEqual(r._acao, "menu_principal");
});

test("opcao 2 seleciona area academico", () => {
  const r = decidirAcao({ numero: "55", nome: "X", mensagem: "2" }, null, T0);
  assert.strictEqual(r._acao, "set_area");
  assert.strictEqual(r.areaAtual, "academico");
});

test("opcao 0 vira handoff humano", () => {
  const r = decidirAcao({ numero: "55", nome: "X", mensagem: "0" }, null, T0);
  assert.strictEqual(r._acao, "humano");
});

test("sair volta ao menu (nao e opt-out)", () => {
  const c = { area: "juridico", estagio: "atendimento", ultimo_contato: T0.toISOString() };
  const r = decidirAcao({ numero: "55", nome: "X", mensagem: "sair" }, c, T0);
  assert.strictEqual(r._acao, "menu_principal");
});

test("inatividade >60min encerra atendimento", () => {
  const velho = new Date("2026-06-30T10:00:00Z").toISOString();
  const c = { area: "juridico", estagio: "atendimento", ultimo_contato: velho };
  const r = decidirAcao({ numero: "55", nome: "X", mensagem: "ola" }, c, T0);
  assert.strictEqual(r._acao, "inatividade");
});

test("retomar sai de inativo direto ao gemini sem menu", () => {
  const c = { area: "juridico", estagio: "inativo", ultimo_contato: T0.toISOString() };
  const r = decidirAcao({ numero: "55", nome: "X", mensagem: "retomar" }, c, T0);
  assert.strictEqual(r._acao, "responder");
  assert.strictEqual(r.estagio, "atendimento");
});

test("auto-intencao escala para humano", () => {
  const c = { area: "juridico", estagio: "atendimento", ultimo_contato: T0.toISOString() };
  const r = decidirAcao({ numero: "55", nome: "X", mensagem: "quanto custa o plano?" }, c, T0);
  assert.strictEqual(r._acao, "humano");
});

test("mensagem normal em area responde via gemini", () => {
  const c = { area: "juridico", estagio: "atendimento", ultimo_contato: T0.toISOString() };
  const r = decidirAcao({ numero: "55", nome: "X", mensagem: "o que e usucapiao?" }, c, T0);
  assert.strictEqual(r._acao, "responder");
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `node --test scripts/n8n_logic/`
Expected: FAIL — `Cannot find module './decidir_acao'`

- [ ] **Step 3: Write the intent module**

Create `scripts/n8n_logic/detectar_intencao.js`:
```js
// Auto-detecção de intenção de compra (WOW proativo).
// V1: keywords. V2 (futuro): pontuação por Gemini.
const SINAIS_INTENCAO = [
  "quanto custa", "preço", "preco", "valor", "plano", "planos",
  "quero contratar", "como assino", "assinar", "fechar negócio", "fechar negocio",
  "falar com humano", "atendente", "falar com uma pessoa",
  "falar com alguem", "falar com alguém"
];

function detectarIntencao(mensagem) {
  const m = (mensagem || "").toLowerCase();
  return SINAIS_INTENCAO.some((s) => m.includes(s));
}

module.exports = { detectarIntencao, SINAIS_INTENCAO };
```

- [ ] **Step 4: Write the decision module**

Create `scripts/n8n_logic/decidir_acao.js`:
```js
const { detectarIntencao } = require("./detectar_intencao");

const MENU_OPCOES = {
  "1": "b2b", "2": "academico", "3": "observatorio",
  "4": "api", "5": "juridico", "6": "filosofia", "0": "humano"
};
const RESET_WORDS = ["menu", "inicio", "início", "voltar", "reiniciar", "sair"];
const STOP_WORDS = ["parar", "stop", "cancelar"];
const JA_CADASTRADO = ["cadastrado", "lead_site", "ignorou_cadastro"];
const TIMEOUT_MINUTOS = 60;

function decidirAcao(dadosMsg, contato, agora = new Date()) {
  const areaAtual = contato ? contato.area : null;
  const estagio = (contato && contato.estagio) || "novo";
  const msgCount = (contato && contato.dados && contato.dados.msgCount) || 0;
  const { numero, nome, mensagem } = dadosMsg;

  const msgLower = mensagem.toLowerCase().replace(/[!.?]+$/, "").trim();
  const opcaoMenu = MENU_OPCOES[msgLower] || null;
  const isReset = RESET_WORDS.includes(msgLower);
  const isRetomar = msgLower === "retomar";

  const ultimo = contato && contato.ultimo_contato ? new Date(contato.ultimo_contato) : null;
  const minutos = ultimo ? Math.floor((agora.getTime() - ultimo.getTime()) / 60000) : 0;
  const isInativo = estagio === "atendimento" && minutos > TIMEOUT_MINUTOS;

  const base = { numero, nome, mensagem, areaAtual, msgCount, estagio };

  if (isRetomar && estagio === "inativo")
    return { ...base, _acao: "responder", estagio: "atendimento", msgCount: msgCount + 1 };
  if (isInativo)
    return { ...base, _acao: "inatividade" };
  if (estagio === "aguardando_cadastro")
    return { ...base, _acao: "processar_cadastro" };
  if (isReset)
    return { ...base, _acao: "menu_principal", areaAtual: null, msgCount: 0 };
  if (opcaoMenu) {
    if (opcaoMenu === "humano")
      return { ...base, _acao: "humano", areaAtual: "humano", msgCount: 0 };
    return { ...base, _acao: "set_area", areaAtual: opcaoMenu, msgCount: 0 };
  }
  if (!areaAtual)
    return { ...base, _acao: "menu_principal", areaAtual: null, msgCount: 0 };
  if (detectarIntencao(mensagem))
    return { ...base, _acao: "humano", areaAtual: "humano" };

  const newMsgCount = msgCount + 1;
  if (newMsgCount >= 3 && !JA_CADASTRADO.includes(estagio))
    return { ...base, _acao: "cadastro_invite", msgCount: newMsgCount };
  return { ...base, _acao: "responder", msgCount: newMsgCount };
}

module.exports = { decidirAcao, detectarIntencao: require("./detectar_intencao").detectarIntencao, MENU_OPCOES, RESET_WORDS, STOP_WORDS };
```

- [ ] **Step 5: Run test to verify it passes**

Run: `node --test scripts/n8n_logic/`
Expected: PASS — 8 tests, 0 failures

- [ ] **Step 6: Commit**

```bash
git add scripts/n8n_logic/decidir_acao.js scripts/n8n_logic/detectar_intencao.js scripts/n8n_logic/decidir_acao.test.js
git commit -m "feat(sp1): lógica de decisão + intenção testável (6 opções, retomada, auto-intenção)"
```

---

### Task 2: Testes da Detecção de Intenção

**Files:**
- Test: `scripts/n8n_logic/detectar_intencao.test.js`

**Interfaces:**
- Consumes: `detectarIntencao(mensagem)` da Task 1.

- [ ] **Step 1: Write the failing test**

Create `scripts/n8n_logic/detectar_intencao.test.js`:
```js
const test = require("node:test");
const assert = require("node:assert");
const { detectarIntencao } = require("./detectar_intencao");

test("detecta pergunta de preço", () => {
  assert.strictEqual(detectarIntencao("quanto custa isso?"), true);
});

test("detecta pedido de humano", () => {
  assert.strictEqual(detectarIntencao("quero falar com atendente"), true);
});

test("detecta intenção de contratar", () => {
  assert.strictEqual(detectarIntencao("quero contratar já"), true);
});

test("mensagem jurídica comum NÃO dispara", () => {
  assert.strictEqual(detectarIntencao("o que é habeas corpus?"), false);
});

test("string vazia é segura", () => {
  assert.strictEqual(detectarIntencao(""), false);
});
```

- [ ] **Step 2: Run test to verify it passes**

Run: `node --test scripts/n8n_logic/detectar_intencao.test.js`
Expected: PASS — 5 tests (o módulo já existe da Task 1)

- [ ] **Step 3: Commit**

```bash
git add scripts/n8n_logic/detectar_intencao.test.js
git commit -m "test(sp1): cobertura da detecção de intenção"
```

---

### Task 3: Integrar Lógica no Workflow N8N (nós 2, 7, 8)

**Files:**
- Modify: `scripts/n8n_fenice_tim_v4.json` (nó "2. Extrair e Normalizar" — MENU_OPCOES 6 opções; nó "7. Decidir Próxima Ação" — inlinar decidirAcao+detectarIntencao; nó "8. Switch por Ação" — saída "inatividade")

**Interfaces:**
- Consumes: lógica validada da Task 1.
- Produces: workflow com roteamento de 6 opções + inatividade + retomada + auto-intenção.

- [ ] **Step 1: Corrigir MENU_OPCOES para 6 opções no nó 2**

No `jsCode` do nó "2. Extrair e Normalizar", localizar a linha `const MENU_OPCOES = ...` e garantir que seja exatamente (JSON escapado com `\"`):
```
const MENU_OPCOES = {\"1\":\"b2b\",\"2\":\"academico\",\"3\":\"observatorio\",\"4\":\"api\",\"5\":\"juridico\",\"6\":\"filosofia\",\"0\":\"humano\"};
```
E `STOP_WORDS` sem "sair": `const STOP_WORDS = [\"parar\",\"stop\",\"cancelar\"];`
E `RESET_WORDS` com "sair": `const RESET_WORDS = [\"menu\",\"inicio\",\"início\",\"voltar\",\"reiniciar\",\"sair\"];`

- [ ] **Step 2: Substituir o jsCode do nó 7 pela lógica inlinada**

No nó "7. Decidir Próxima Ação", substituir o campo `jsCode` inteiro pela versão inlinada de `decidirAcao` (a mesma lógica da Task 1, adaptada ao runtime N8N):
```
const dadosMsg = $('2. Extrair e Normalizar').first().json;
const contatosArr = ($input.first().json.contatos) || [];
const contato = contatosArr.length > 0 ? contatosArr[0] : null;
const SINAIS = ["quanto custa","preço","preco","valor","plano","planos","quero contratar","como assino","assinar","fechar negócio","fechar negocio","falar com humano","atendente","falar com uma pessoa","falar com alguem","falar com alguém"];
const detectarIntencao = (m) => { const s=(m||'').toLowerCase(); return SINAIS.some(x=>s.includes(x)); };
const MENU_OPCOES = {"1":"b2b","2":"academico","3":"observatorio","4":"api","5":"juridico","6":"filosofia","0":"humano"};
const RESET_WORDS = ["menu","inicio","início","voltar","reiniciar","sair"];
const JA_CADASTRADO = ["cadastrado","lead_site","ignorou_cadastro"];
const TIMEOUT_MINUTOS = 60;
const areaAtual = contato ? contato.area : null;
const estagio = (contato && contato.estagio) || "novo";
const msgCount = (contato && contato.dados && contato.dados.msgCount) || 0;
const { numero, nome, mensagem } = dadosMsg;
const msgLower = mensagem.toLowerCase().replace(/[!.?]+$/, "").trim();
const opcaoMenu = MENU_OPCOES[msgLower] || null;
const isReset = RESET_WORDS.includes(msgLower);
const isRetomar = msgLower === "retomar";
const ultimo = contato && contato.ultimo_contato ? new Date(contato.ultimo_contato) : null;
const minutos = ultimo ? Math.floor((new Date().getTime() - ultimo.getTime())/60000) : 0;
const isInativo = estagio === "atendimento" && minutos > TIMEOUT_MINUTOS;
const base = { numero, nome, mensagem, areaAtual, msgCount, estagio };
if (isRetomar && estagio === "inativo") return [{ json: { ...base, _acao: "responder", estagio: "atendimento", msgCount: msgCount + 1 } }];
if (isInativo) return [{ json: { ...base, _acao: "inatividade" } }];
if (estagio === "aguardando_cadastro") return [{ json: { ...base, _acao: "processar_cadastro" } }];
if (isReset) return [{ json: { ...base, _acao: "menu_principal", areaAtual: null, msgCount: 0 } }];
if (opcaoMenu) { if (opcaoMenu === "humano") return [{ json: { ...base, _acao: "humano", areaAtual: "humano", msgCount: 0 } }]; return [{ json: { ...base, _acao: "set_area", areaAtual: opcaoMenu, msgCount: 0 } }]; }
if (!areaAtual) return [{ json: { ...base, _acao: "menu_principal", areaAtual: null, msgCount: 0 } }];
if (detectarIntencao(mensagem)) return [{ json: { ...base, _acao: "humano", areaAtual: "humano" } }];
const newMsgCount = msgCount + 1;
if (newMsgCount >= 3 && !JA_CADASTRADO.includes(estagio)) return [{ json: { ...base, _acao: "cadastro_invite", msgCount: newMsgCount } }];
return [{ json: { ...base, _acao: "responder", msgCount: newMsgCount } }];
```

- [ ] **Step 3: Adicionar saída "inatividade" ao nó 8 (Switch)**

No nó "8. Switch por Ação", adicionar uma regra (antes de "menu_principal"): `leftValue = {{ $json._acao }}`, `rightValue = "inatividade"`, `operator = string/equals`, `outputKey = "inatividade"`.

- [ ] **Step 4: Validar o JSON**

Run: `python -m json.tool scripts/n8n_fenice_tim_v4.json > /dev/null && echo OK`
Expected: `OK`

- [ ] **Step 5: Commit**

```bash
git add scripts/n8n_fenice_tim_v4.json
git commit -m "feat(sp1): integrar decisão 6-opções + inatividade + auto-intenção no N8N (nós 2,7,8)"
```

---

### Task 4: Nós de Inatividade + Boas-vindas + Fiação (Switch → nós)

**Files:**
- Modify: `scripts/n8n_fenice_tim_v4.json` (adicionar nós "5c/5d" inatividade e "16a/16b" boas-vindas; conectar saídas do Switch)

**Interfaces:**
- Consumes: saídas do Switch da Task 3 (`inatividade`, `set_area`, `humano`).

- [ ] **Step 1: Adicionar nó "5c. Enviar MSG Inatividade"**

Nó httpRequest POST para `https://evolution-api-9fbw.srv1784289.hstgr.cloud/message/sendText/fenice-tim-prod` (headers apikey `XpwOsi1Zq6gLRnISF5bN9PvEFzeMfKA7` + Content-Type json), body:
```
number = {{ $('7. Decidir Próxima Ação').item.json.numero }}
text = "⏱️ *Por falta de interação estamos encerrando o atendimento.*\n\nCaso queira retomar a conversa, digite: *retomar*\n\n👤 *Teo — Intelligence Concierge*\n© 2026 Fenice IT Justech.IA"
```
`continueOnFail: true`.

- [ ] **Step 2: Adicionar nó "5d. Marcar como Inativo"**

Nó httpRequest POST para `https://qcfdssnpjzvjbvemhrik.supabase.co/rest/v1/fenice_tim_contatos` (headers apikey/Authorization service_key + Prefer `resolution=merge-duplicates,return=minimal`), body:
```
numero = {{ $('7. Decidir Próxima Ação').item.json.numero }}
estagio = "inativo"
```
`continueOnFail: true`.

- [ ] **Step 3: Adicionar nó "16a. Boas-vindas Área" (Code)**

`jsCode`:
```
const dados = $('7. Decidir Próxima Ação').first().json;
const { numero, nome, areaAtual } = dados;
const BV = {
  b2b: "*Bem-vindo à área B2B Corporativo!* 🏢\nSoluções enterprise de IA jurídica para escritórios e empresas.\nComo posso ajudar?",
  academico: "*Bem-vindo à área Acadêmica!* 🎓\nPesquisa jurídica, TCC, artigos com base em 5685 artigos + súmulas.\nComo posso ajudar?",
  observatorio: "*Observatório da Mulher SFS!* 👁️\n📞 EMERGÊNCIA? Disque 190 ou 180 imediatamente.\nLei Maria da Penha (11.340/2006). Como posso ajudar?",
  api: "*Bem-vindo à área API & Devs!* ⚡\nAPI REST Fenice — /buscar, /analisar, /hermeneutica.\nComo posso ajudar?",
  juridico: "*Bem-vindo à Consultoria Jurídica!* ⚖️\nDireito brasileiro: CC, CLT, CP, CF/88, CDC, Súmulas.\nComo posso ajudá-lo(a)?",
  filosofia: "*Filosofia & Teologia!* 🧠\nFilosofia jurídica, hermenêutica, ética, teologia.\nComo posso ajudar?"
};
const mensagem = BV[areaAtual] || BV.juridico;
return [{ json: { numero, nome, areaAtual, mensagem } }];
```

- [ ] **Step 4: Adicionar nó "16b. Enviar Boas-vindas" (httpRequest)**

POST sendText Evolution, body:
```
number = {{ $json.numero }}
text = {{ $json.mensagem + '\n\n👤 *Teo — Intelligence Concierge*\n© 2026 Fenice IT Justech.IA' }}
```
`continueOnFail: true`.

- [ ] **Step 5: Conectar no bloco "connections"**

Adicionar/ajustar:
```
"8. Switch por Ação" saída "inatividade" → "5c. Enviar MSG Inatividade"
"5c. Enviar MSG Inatividade" → "5d. Marcar como Inativo"
"16. Salvar Área Escolhida (Tim)" → "16a. Boas-vindas Área"
"16a. Boas-vindas Área" → "16b. Enviar Boas-vindas"
"16b. Enviar Boas-vindas" → "10. Montar Prompt por Área"
```

- [ ] **Step 6: Validar JSON e commitar**

Run: `python -m json.tool scripts/n8n_fenice_tim_v4.json > /dev/null && echo OK`
Expected: `OK`
```bash
git add scripts/n8n_fenice_tim_v4.json
git commit -m "feat(sp1): nós de inatividade (5c/5d) + boas-vindas por área (16a/16b) + fiação"
```

---

### Task 5: Menu de 6 Opções (texto)

**Files:**
- Modify: `scripts/n8n_fenice_tim_v4.json` (nó "9a. Enviar Menu Principal")

**Interfaces:**
- Consumes: saída "menu" do Switch.

- [ ] **Step 1: Substituir o texto do menu no nó 9a**

Campo `text` do nó "9a. Enviar Menu Principal":
```
👤 *Teo — Intelligence Concierge* 🤖

Olá! Sou o Téo, Intelligence Concierge da Fenice IT.
Em que posso ajudá-lo(a) hoje?

*1️⃣  B2B Corporativo*
*2️⃣  Acadêmico & Pesquisa*
*3️⃣  Observatório da Mulher SFS*
*4️⃣  API & Desenvolvedores*
*5️⃣  Consultoria Jurídica*
*6️⃣  Filosofia & Teologia*
*0️⃣  Falar com Especialista*

_Digite o número e pressione enviar_
💬 Para sair, digite: *sair*

© 2026 Fenice IT Justech.IA
```

- [ ] **Step 2: Validar JSON e commitar**

Run: `python -m json.tool scripts/n8n_fenice_tim_v4.json > /dev/null && echo OK`
Expected: `OK`
```bash
git add scripts/n8n_fenice_tim_v4.json
git commit -m "feat(sp1): menu principal com 6 opções + instrução sair"
```

---

### Task 6: Handoff com Contexto de 7 Elementos

**Files:**
- Modify: `scripts/n8n_fenice_tim_v4.json` (nó "9b. Enviar MSG Humano" + novo nó "9b-ctx. Montar Contexto Handoff")

**Interfaces:**
- Consumes: saída "humano" do Switch.
- Produces: mensagem de handoff ao Ramão (`5547991041414`) com 7 elementos.

- [ ] **Step 1: Adicionar nó "9b-ctx. Montar Contexto Handoff" (Code)**

`jsCode`:
```
const d = $('7. Decidir Próxima Ação').first().json;
const contatosArr = ($('6. Buscar Contato Tim (Supabase)').first().json.contatos) || [];
const c = contatosArr[0] || {};
const email = (c.dados && c.dados.email) || "não informado";
const resumo = "Prospect demonstrou interesse na área " + (d.areaAtual || "juridico") + ". Última mensagem: \"" + d.mensagem + "\".";
const texto =
  "🔥 *PROSPECT QUENTE — Handoff*\n\n" +
  "👤 *Nome:* " + d.nome + "\n" +
  "📱 *WhatsApp:* +" + d.numero + "\n" +
  "📧 *E-mail:* " + email + "\n" +
  "💼 *Assunto:* " + (d.areaAtual || "juridico") + "\n" +
  "🧭 *Intenção:* " + (/^0$/.test(d.mensagem.trim()) ? "pediu especialista (opção 0)" : "sinal de compra detectado") + "\n" +
  "📝 *Resumo:* " + resumo + "\n" +
  "➡️ *Próximo passo:* subir BKO / contatar prospect\n\n" +
  "© 2026 Fenice IT Justech.IA";
return [{ json: { numero_admin: "5547991041414", texto } }];
```

- [ ] **Step 2: Ajustar nó "9b. Enviar MSG Humano"**

Manter a mensagem ao prospect (confirmação de que um especialista falará com ele). Garantir que contém BOT_SIG (`© 2026`). Após ele, encadear o envio ao admin.

- [ ] **Step 3: Adicionar nó "9b-admin. Notificar Ramão" (httpRequest)**

POST sendText Evolution, body:
```
number = {{ $('9b-ctx. Montar Contexto Handoff').item.json.numero_admin }}
text = {{ $('9b-ctx. Montar Contexto Handoff').item.json.texto }}
```
`continueOnFail: true`.

- [ ] **Step 4: Conectar**

```
"8. Switch por Ação" saída "humano" → "9b-ctx. Montar Contexto Handoff"
"9b-ctx. Montar Contexto Handoff" → "9b. Enviar MSG Humano"
"9b. Enviar MSG Humano" → "9b-admin. Notificar Ramão"
```

- [ ] **Step 5: Validar JSON e commitar**

Run: `python -m json.tool scripts/n8n_fenice_tim_v4.json > /dev/null && echo OK`
Expected: `OK`
```bash
git add scripts/n8n_fenice_tim_v4.json
git commit -m "feat(sp1): handoff ao Ramão com contexto de 7 elementos"
```

---

### Task 7: Correção do Número Admin (fenice-leads)

**Files:**
- Modify: `scripts/n8n_fenice_leads.json` (nó "5a. WhatsApp Admin")

**Interfaces:**
- Consumes: workflow WOW disparado pelo `/leads`.

- [ ] **Step 1: Corrigir o número no nó 5a**

No nó "5a. WhatsApp Admin", campo `number`, trocar `554797348385` por `5547991041414`.

- [ ] **Step 2: Validar JSON e commitar**

Run: `python -m json.tool scripts/n8n_fenice_leads.json > /dev/null && echo OK`
Expected: `OK`
```bash
git add scripts/n8n_fenice_leads.json
git commit -m "fix(sp1): notificação de lead vai ao corporativo 5547991041414"
```

---

### Task 8: E-mail WOW via Microsoft Graph API

**Files:**
- Modify: `scripts/n8n_fenice_leads.json` (substituir nó "5b. E-mail Prospect (Office365)" por nó Graph API)

**Interfaces:**
- Consumes: `$('4. Extrair WOW Insight').item.json` (nome, primeiroNome, email, interesseLabel).

- [ ] **Step 1: Substituir o nó 5b por httpRequest Graph API**

Novo nó "5b. E-mail Prospect (Graph API)" httpRequest:
```
method = POST
url = https://graph.microsoft.com/v1.0/users/fenice_tech@fenice.ia.br/sendMail
authentication = predefinedCredentialType / httpHeaderAuth  (credential OAuth "Graph Mail" — a criar no N8N)
Content-Type = application/json
body (raw json):
{
  "message": {
    "subject": "Fenice IA recebeu seu contato, {{ $('4. Extrair WOW Insight').item.json.primeiroNome }}!",
    "body": { "contentType": "Text", "content": "Olá, {{ $('4. Extrair WOW Insight').item.json.primeiroNome }}!\n\nFicamos felizes com seu interesse em {{ $('4. Extrair WOW Insight').item.json.interesseLabel }}.\n\nEm instantes o Téo entrará em contato pelo WhatsApp.\n\nEquipe Fenice IT\nhttps://fenice.ia.br" },
    "toRecipients": [ { "emailAddress": { "address": "{{ $('4. Extrair WOW Insight').item.json.email }}" } } ]
  },
  "saveToSentItems": true
}
timeout = 15000
continueOnFail = true
```

- [ ] **Step 2: Documentar o pré-requisito Azure**

Adicionar comentário no topo do arquivo (via campo `notes` do nó ou no spec): app registration no Azure/Entra ID com permissão de aplicação `Mail.Send` concedida a `fenice_tech@fenice.ia.br`; credential OAuth2 client-credentials cadastrada no N8N como "Graph Mail".

- [ ] **Step 3: Validar JSON e commitar**

Run: `python -m json.tool scripts/n8n_fenice_leads.json > /dev/null && echo OK`
Expected: `OK`
```bash
git add scripts/n8n_fenice_leads.json
git commit -m "feat(sp1): e-mail WOW via Microsoft Graph API (substitui SMTP placeholder)"
```

---

### Task 9: Import da Carteira Farmer (Python)

**Files:**
- Create: `scripts/importar_carteira.py`
- Test: `scripts/test_importar_carteira.py`

**Interfaces:**
- Produces: `normalizar_telefone(bruto) → str`; `linha_para_contato(linha: dict) → dict`; `carregar_csv(caminho) → list[dict]`; `enviar_supabase(contatos, sb_url, sb_key) → int`.

- [ ] **Step 1: Write the failing test**

Create `scripts/test_importar_carteira.py`:
```python
from importar_carteira import normalizar_telefone, linha_para_contato


def test_normaliza_11_digitos_adiciona_55():
    assert normalizar_telefone("(47) 99104-1414") == "5547991041414"


def test_normaliza_ja_com_55_mantem():
    assert normalizar_telefone("5547991041414") == "5547991041414"


def test_linha_vira_contato_farmer():
    linha = {"nome": "João Silva", "telefone": "(47) 99104-1414",
             "email": "Joao@X.com", "assunto": "juridico"}
    c = linha_para_contato(linha)
    assert c["numero"] == "5547991041414"
    assert c["nome"] == "João Silva"
    assert c["area"] == "juridico"
    assert c["estagio"] == "pos_venda"
    assert c["dados"]["email"] == "joao@x.com"


def test_assunto_vazio_default_juridico():
    c = linha_para_contato({"nome": "X", "telefone": "47991041414", "email": "a@b.com", "assunto": ""})
    assert c["area"] == "juridico"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd scripts && python -m pytest test_importar_carteira.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'importar_carteira'`

- [ ] **Step 3: Write the implementation**

Create `scripts/importar_carteira.py`:
```python
"""Importa a carteira Farmer do Ramão para o Supabase fenice_tim_contatos.

Uso: python importar_carteira.py carteira.csv
CSV com colunas: nome, telefone, email, assunto
Estágio inicial: pos_venda (base existente = Farmer).
"""
import csv
import os
import sys

import httpx


def normalizar_telefone(bruto: str) -> str:
    dig = "".join(c for c in (bruto or "") if c.isdigit())
    if len(dig) == 11:
        dig = "55" + dig
    return dig


def linha_para_contato(linha: dict) -> dict:
    return {
        "numero": normalizar_telefone(linha.get("telefone", "")),
        "nome": (linha.get("nome") or "").strip(),
        "area": (linha.get("assunto") or "").strip() or "juridico",
        "estagio": "pos_venda",
        "dados": {"email": (linha.get("email") or "").strip().lower()},
    }


def carregar_csv(caminho: str) -> list:
    with open(caminho, encoding="utf-8-sig", newline="") as f:
        return [linha_para_contato(l) for l in csv.DictReader(f)]


def enviar_supabase(contatos: list, sb_url: str, sb_key: str) -> int:
    hdrs = {
        "apikey": sb_key,
        "Authorization": f"Bearer {sb_key}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal,resolution=merge-duplicates",
    }
    with httpx.Client(timeout=30) as c:
        r = c.post(
            f"{sb_url.rstrip('/')}/rest/v1/fenice_tim_contatos",
            params={"on_conflict": "numero"},
            headers=hdrs,
            json=contatos,
        )
    r.raise_for_status()
    return len(contatos)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python importar_carteira.py carteira.csv")
        sys.exit(1)
    contatos = carregar_csv(sys.argv[1])
    total = enviar_supabase(
        contatos,
        os.environ["SUPABASE_URL"],
        os.environ["SUPABASE_SERVICE_KEY"],
    )
    print(f"✅ {total} contatos Farmer importados.")
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd scripts && python -m pytest test_importar_carteira.py -v`
Expected: PASS — 4 tests

- [ ] **Step 5: Commit**

```bash
git add scripts/importar_carteira.py scripts/test_importar_carteira.py
git commit -m "feat(sp1): import da carteira Farmer para Supabase (com testes)"
```

---

### Task 10: Deploy N8N + Testes de Aceitação (manual)

**Files:**
- Nenhum arquivo — deploy e verificação.

**Interfaces:**
- Consumes: workflows atualizados das Tasks 3-8.

- [ ] **Step 1: Backup do workflow atual no N8N**

No painel `feniceit.app.n8n.cloud`: abrir "Fenice_Tim — WhatsApp IVR v4" → Export → salvar `n8n_fenice_tim_v4_backup_2026-06-30.json`. Repetir para "fenice-leads".

- [ ] **Step 2: Importar os dois workflows atualizados**

Importar `scripts/n8n_fenice_tim_v4.json` e `scripts/n8n_fenice_leads.json` (Overwrite). Criar credential OAuth "Graph Mail" (Task 8). Ativar ambos.

- [ ] **Step 3: Rodar os 11 testes de aceitação do spec**

Executar via WhatsApp para `5547991041414` a lista do spec (seção "Testes de Aceitação"):
1. "oi" → menu 6 opções
2. "5" → boas-vindas Jurídico
3. pergunta jurídica → RAG+Gemini
4. inativo >60min → encerramento com "retomar"
5. "retomar" → volta ao Gemini sem menu
6. "sair" → menu
7. "quanto custa?" → handoff (auto-intenção)
8. "0" → handoff manual com contexto de 7 elementos
9. formulário site → e-mail Graph + WhatsApp WOW <60s
10. Ramão recebe notificação em `5547991041414`
11. `python importar_carteira.py carteira.csv` → contatos `pos_venda`

Expected: todos passam. Registrar falhas para nova iteração (kaizen).

- [ ] **Step 4: Atualizar memória de estado**

Atualizar `system-estado-atual.md`: menu 6 opções confirmado, e-mail Graph ativo, handoff 7 elementos, número admin corrigido.

---

## Self-Review

**1. Spec coverage:**
- Menu 6 opções → Tasks 3, 5 ✅
- E-mail Graph API → Task 8 ✅
- Auto-intenção → Tasks 1, 3 ✅
- Retomada/inatividade → Tasks 1, 3, 4 ✅
- Handoff 7 elementos → Task 6 ✅
- Número admin → Tasks 6, 7 ✅
- Captura 4 campos → coberto pelo /leads existente + Task 9 ✅
- Carteira Farmer → Task 9 ✅
- Testes de aceitação → Task 10 ✅

**2. Placeholder scan:** Nenhum "TBD/TODO"; todo código completo. O pré-requisito Azure (Task 8) é documentado, não placeholder de código.

**3. Type consistency:** `_acao` (string) consistente entre Tasks 1 e 3; `decidirAcao`/`detectarIntencao` idênticos; `linha_para_contato`/`normalizar_telefone` consistentes entre Tasks 9 e testes.

**Nota de dependência:** Tasks 1-2 exigem Node.js 18+ (`node:test`). Task 9 exige `pytest` + `httpx`. Se Node não estiver disponível, a lógica ainda é válida (é copiada para o N8N na Task 3), mas os testes automatizados não rodam — nesse caso, confiar nos testes de aceitação da Task 10.

---

*بِسْمِ اللهِ الرَّحْمَنِ الرَّحِيمِ*

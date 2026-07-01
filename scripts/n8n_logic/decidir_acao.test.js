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

test("apos 3 mensagens na area convida cadastro", () => {
  const c = { area: "juridico", estagio: "atendimento", dados: { msgCount: 2 }, ultimo_contato: T0.toISOString() };
  const r = decidirAcao({ numero: "55", nome: "X", mensagem: "outra duvida" }, c, T0);
  assert.strictEqual(r._acao, "cadastro_invite");
  assert.strictEqual(r.msgCount, 3);
});

test("Farmer pos_venda nao recebe convite de cadastro", () => {
  const c = { area: "juridico", estagio: "pos_venda", dados: { msgCount: 5 }, ultimo_contato: T0.toISOString() };
  const r = decidirAcao({ numero: "55", nome: "X", mensagem: "duvida" }, c, T0);
  assert.strictEqual(r._acao, "responder");
});

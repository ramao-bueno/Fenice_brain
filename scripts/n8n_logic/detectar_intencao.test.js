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

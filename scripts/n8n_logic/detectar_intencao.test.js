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

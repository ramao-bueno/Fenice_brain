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

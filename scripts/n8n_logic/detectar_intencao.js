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

// Roteamento por intenção: termos de ALTA confiança por área.
// Termo ambíguo/genérico ("direito", "lei", "sistema") NÃO entra aqui — vai p/ descoberta.
const AREA_KEYWORDS = {
  b2b:          ["tim", "corporativo", "operadora", "b2b", "plano da empresa", "plano corporativo"],
  academico:    ["faculdade", "estudar", "estudo", "prova", "concurso", "oab", "aula", "matéria", "materia", "univille"],
  observatorio: ["monitorar", "monitoramento", "observatório", "observatorio", "acompanhar processo"],
  api:          ["api", "integração", "integracao", "webhook", "integrar sistema", "desenvolvedor"],
  juridico:     ["advogado", "processo judicial", "penal", "civil", "constitucional", "tributário",
                 "tributario", "trabalhista", "dúvida jurídica", "duvida juridica", "petição", "peticao"],
  filosofia:    ["filosofia", "filosófico", "filosofico", "ética", "etica", "pensador", "existência", "existencia"],
};

// termo curto sem espaço (ex.: "api", "oab", "b2b") casa só como palavra inteira,
// evitando falso-positivo em "terapia", "rapidamente" etc.
function _casa(termo, m) {
  if (termo.length <= 3 && !termo.includes(" ")) {
    return new RegExp(`\\b${termo.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}\\b`).test(m);
  }
  return m.includes(termo);
}

function inferirArea(mensagem) {
  const m = (mensagem || "").toLowerCase();
  if (!m) return null;
  for (const [area, termos] of Object.entries(AREA_KEYWORDS)) {
    if (termos.some((t) => _casa(t, m))) return area;
  }
  return null;
}

const SAUDACOES = ["oi", "ola", "olá", "opa", "oie", "e ai", "eai", "hey", "hi",
  "bom dia", "boa tarde", "boa noite", "salam", "salaam", "as salamu alaikum", "saudações", "saudacoes"];

// true quando a mensagem é essencialmente só um cumprimento.
function isSaudacao(mensagem) {
  const m = (mensagem || "").toLowerCase().replace(/[!.?,]+$/g, "").trim();
  if (!m) return false;
  if (SAUDACOES.includes(m)) return true;
  // começa com saudação e é curta (≤ 3 palavras): "bom dia téo"
  const inicioSaudacao = SAUDACOES.some((s) => m.startsWith(s));
  return inicioSaudacao && m.split(/\s+/).length <= 3;
}

module.exports = { detectarIntencao, SINAIS_INTENCAO, inferirArea, AREA_KEYWORDS, isSaudacao, SAUDACOES };

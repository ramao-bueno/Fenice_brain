const { detectarIntencao, inferirArea, isSaudacao } = require("./detectar_intencao");

const MENU_OPCOES = {
  "1": "b2b", "2": "academico", "3": "observatorio",
  "4": "api", "5": "juridico", "6": "filosofia", "0": "humano"
};
const RESET_WORDS = ["menu", "inicio", "início", "voltar", "reiniciar", "sair"];
const STOP_WORDS = ["parar", "stop", "cancelar"];
const JA_CADASTRADO = ["cadastrado", "lead_site", "ignorou_cadastro", "pos_venda"];
const TIMEOUT_MINUTOS = 60;

function decidirAcao(dadosMsg, contato, agora = new Date()) {
  const areaAtual = contato ? contato.area : null;
  const estagio = (contato && contato.estagio) || "novo";
  const msgCount = (contato && contato.dados && contato.dados.msgCount) || 0;
  const { numero, nome, mensagem } = dadosMsg;

  const msgLower = (mensagem || "").toLowerCase().replace(/[!.?]+$/, "").trim();
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
  if (!areaAtual) {
    const areaInferida = inferirArea(mensagem);
    if (areaInferida)
      return { ...base, _acao: "set_area", areaAtual: areaInferida, msgCount: 0 };
    if (isSaudacao(mensagem))
      return { ...base, _acao: "menu_principal", areaAtual: null, msgCount: 0 };
    return { ...base, _acao: "descoberta", estagio: "descoberta", areaAtual: null };
  }
  if (detectarIntencao(mensagem))
    return { ...base, _acao: "humano", areaAtual: "humano" };

  const newMsgCount = msgCount + 1;
  if (newMsgCount >= 3 && !JA_CADASTRADO.includes(estagio))
    return { ...base, _acao: "cadastro_invite", msgCount: newMsgCount };
  return { ...base, _acao: "responder", msgCount: newMsgCount };
}

module.exports = { decidirAcao, detectarIntencao, MENU_OPCOES, RESET_WORDS, STOP_WORDS };

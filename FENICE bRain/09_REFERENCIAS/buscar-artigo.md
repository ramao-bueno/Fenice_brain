<%*
// ============================================================
// FENICE BRAIN — Buscar Artigo por Codigo v2
// Atalho: Ctrl+Shift+B | Ctrl+P > "QuickAdd: Buscar Artigo"
// Fix: funciona em buscas subsequentes sem necessidade de clear
// ============================================================

// Define tR vazio ANTES de qualquer await — garante contexto limpo
// mesmo que o usuario cancele no meio da operacao
tR = "";

const CODIGOS = {
  "CF/88 — Constituicao Federal": {
    tag: "cf88",
    pasta: "00_CONSTITUIÇÃO_FEDERAL/Artigos",
    label: "CF/88"
  },
  "Codigo Civil (CC)": {
    tag: "cc",
    pasta: "02_DIREITO_CIVIL/Artigos",
    label: "CC"
  },
  "Codigo Penal (CP)": {
    tag: "direito-penal",
    pasta: "03_CÓDIGO_PENAL",
    label: "CP"
  },
  "CPC — Processo Civil": {
    tag: "cpc",
    pasta: "01_CÓDIGO_PROCESSO_CIVIL",
    label: "CPC"
  },
};

// Passo 1: selecionar o codigo
let codigoNome;
try {
  codigoNome = await tp.system.suggester(
    Object.keys(CODIGOS),
    Object.keys(CODIGOS),
    true,
    "1. Selecione o Codigo:"
  );
} catch(e) {
  return; // usuario pressionou Esc
}
if (!codigoNome) return;

const config = CODIGOS[codigoNome];

// Passo 2: numero do artigo
let numArtigo;
try {
  numArtigo = await tp.system.prompt(
    `2. Numero do Artigo (${config.label}):`,
    "",
    true
  );
} catch(e) {
  return; // usuario pressionou Esc
}
if (!numArtigo || !numArtigo.trim()) return;

const numLimpo = numArtigo.trim();

// Busca no vault: primeiro restrito a pasta, depois global por tag
const allFiles = app.vault.getFiles();

const encontrar = (restringirPasta) => allFiles.find(f => {
  if (restringirPasta && !f.path.includes(config.pasta)) return false;
  const meta = app.metadataCache.getFileCache(f)?.frontmatter;
  if (!meta) return false;
  const artigoOk = String(meta.artigo) === numLimpo;
  if (!restringirPasta) {
    return artigoOk && meta.tags && meta.tags.includes(config.tag);
  }
  return artigoOk;
});

const found = encontrar(true) || encontrar(false);

if (found) {
  // openLinkText: API correta para navegacao confiavel em qualquer contexto
  // Funciona independente do leaf atual — nao depende de estado anterior
  await app.workspace.openLinkText(found.basename, "", false);
  new Notice(`Art. ${numLimpo} — ${config.label} aberto!`, 3000);
} else {
  new Notice(`Art. ${numLimpo} nao encontrado em ${config.label}. Verifique se o pipeline foi executado.`, 4000);
}
%>

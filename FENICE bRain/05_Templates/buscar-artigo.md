<%*
// ============================================================
// FENICE BRAIN — Buscar Artigo por Codigo
// Atalho: Ctrl+P → "Buscar Artigo"
// ============================================================

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
const codigoNome = await tp.system.suggester(
  Object.keys(CODIGOS),
  Object.keys(CODIGOS),
  true,
  "1. Selecione o Codigo:"
);
if (!codigoNome) { tR = ""; return; }

const config = CODIGOS[codigoNome];

// Passo 2: numero do artigo
const numArtigo = await tp.system.prompt(
  `2. Numero do Artigo (${config.label}):`,
  "",
  true
);
if (!numArtigo) { tR = ""; return; }

const numLimpo = numArtigo.trim();

// Busca o arquivo no vault pelo frontmatter artigo + pasta
const allFiles = app.vault.getFiles();
const found = allFiles.find(f => {
  if (!f.path.includes(config.pasta)) return false;
  const meta = app.metadataCache.getFileCache(f)?.frontmatter;
  if (!meta) return false;
  return String(meta.artigo) === numLimpo;
});

if (found) {
  const leaf = app.workspace.getLeaf(false);
  await leaf.openFile(found);
  new Notice(`Art. ${numLimpo} (${config.label}) aberto!`);
} else {
  // Tenta busca mais ampla — sem restringir pasta
  const foundGlobal = allFiles.find(f => {
    const meta = app.metadataCache.getFileCache(f)?.frontmatter;
    if (!meta) return false;
    return String(meta.artigo) === numLimpo && meta.tags && meta.tags.includes(config.tag);
  });
  if (foundGlobal) {
    const leaf = app.workspace.getLeaf(false);
    await leaf.openFile(foundGlobal);
    new Notice(`Art. ${numLimpo} (${config.label}) encontrado!`);
  } else {
    new Notice(`Art. ${numLimpo} nao encontrado em ${config.label}. Verifique se o pipeline foi executado.`);
  }
}

// Nao insere conteudo — apenas navega
tR = "";
%>

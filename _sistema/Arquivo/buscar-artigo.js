// ============================================================
// FENICE BRAIN — Buscar Artigo por Código
// QuickAdd UserScript — funciona de qualquer contexto Obsidian
// Sequência: (1) Código → (2) Número → (3) Artigo + acessórios
// ============================================================

const CODIGOS = {
  "🏛️ CF/88 — Constituição Federal": {
    tag: "cf88",
    pasta: "00_CONSTITUIÇÃO_FEDERAL/Artigos",
    label: "CF/88",
    lei: "Constituição Federal de 1988"
  },
  "📘 Código Civil (CC)": {
    tag: "cc",
    pasta: "02_DIREITO_CIVIL/Artigos",
    label: "CC",
    lei: "Lei 10.406/2002 (Código Civil)"
  },
  "🛡️ Código do Consumidor (CDC)": {
    tag: "cdc",
    pasta: "08_CÓDIGO_CONSUMIDOR",
    label: "CDC",
    lei: "Lei 8.078/1990 (Código do Consumidor)"
  },
  "⚖️ Código Penal (CP)": {
    tag: "direito-penal",
    pasta: "03_CÓDIGO_PENAL",
    label: "CP",
    lei: "Decreto-Lei 2.848/1940 (Código Penal)"
  },
  "📋 CPC — Processo Civil": {
    tag: "cpc",
    pasta: "05_CÓDIGO_PROCESSO_CIVIL",
    label: "CPC",
    lei: "Lei 13.105/2015 (CPC)"
  },
};

module.exports = async (params) => {
  const { app, quickAddApi } = params;

  // ─── PASSO 1: Seleciona o Código ─────────────────────────
  const codigoNome = await quickAddApi.suggester(
    Object.keys(CODIGOS),
    Object.keys(CODIGOS)
  );
  if (!codigoNome) return;

  const config = CODIGOS[codigoNome];

  // ─── PASSO 2: Número do Artigo ───────────────────────────
  const numArtigo = await quickAddApi.inputPrompt(
    `Número do Artigo (${config.label}):`
  );
  if (!numArtigo || !numArtigo.trim()) return;

  const numLimpo = numArtigo.trim();

  // ─── BUSCA no vault ──────────────────────────────────────
  const allFiles = app.vault.getFiles();

  // Busca 1: restrita à pasta do código
  let found = allFiles.find(f => {
    if (!f.path.includes(config.pasta)) return false;
    const meta = app.metadataCache.getFileCache(f)?.frontmatter;
    return meta && String(meta.artigo) === numLimpo;
  });

  // Busca 2: global por tag (fallback)
  if (!found) {
    found = allFiles.find(f => {
      const meta = app.metadataCache.getFileCache(f)?.frontmatter;
      if (!meta) return false;
      const tags = meta.tags || [];
      return String(meta.artigo) === numLimpo && tags.includes(config.tag);
    });
  }

  if (!found) {
    new Notice(
      `⚠ Art. ${numLimpo} não encontrado em ${config.label}.\nVerifique se o pipeline foi executado.`,
      5000
    );
    return;
  }

  // ─── ABRE o artigo principal ─────────────────────────────
  await app.workspace.openLinkText(found.basename, "", false);

  // ─── BUSCA acessórios: parágrafos, incisos, alíneas ──────
  // Artigos do mesmo código que referenciam este artigo
  const acessorios = allFiles.filter(f => {
    if (!f.path.includes(config.pasta)) return false;
    if (f.path === found.path) return false;
    const meta = app.metadataCache.getFileCache(f)?.frontmatter;
    if (!meta) return false;
    // Mesmo número base (ex: Art. 5 e Art. 5-A)
    const artNum = String(meta.artigo || "");
    return artNum.startsWith(numLimpo + "-") || artNum.startsWith(numLimpo + "A");
  });

  // ─── BUSCA correspondentes em outros códigos ─────────────
  const correspondentes = allFiles.filter(f => {
    const meta = app.metadataCache.getFileCache(f)?.frontmatter;
    if (!meta) return false;
    // Artigos que referenciam este na base_constitucional
    const base = Array.isArray(meta.base_constitucional)
      ? meta.base_constitucional
      : [meta.base_constitucional || ""];
    return base.some(b => b && b.includes(`${config.label} Art. ${numLimpo}`));
  });

  // ─── NOTIFICAÇÃO com resumo ───────────────────────────────
  let msg = `✔ Art. ${numLimpo} — ${config.label} aberto!`;

  if (acessorios.length > 0) {
    msg += `\n📎 Acessórios: ${acessorios.map(f => f.basename).join(", ")}`;
  }
  if (correspondentes.length > 0) {
    msg += `\n🔗 Correspondentes: ${correspondentes.map(f => f.basename).join(", ")}`;
  }

  new Notice(msg, 6000);
};

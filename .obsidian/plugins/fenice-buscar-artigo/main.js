'use strict';

const { Plugin, SuggestModal, Modal, Notice } = require('obsidian');

const CODIGOS = [
  // ━━━ DIREITO CONSTITUCIONAL ━━━
  { label: 'CF/88 — Constituição Federal',  tag: 'cf88',          pasta: '02 - Áreas/Base Jurídica/00_ESTRUTURA_CONSTITUCIONAL/CONSTITUIÇÃO_FEDERAL/Artigos', codigo: 'CF/88' },

  // ━━━ DIREITO CIVIL ━━━
  { label: 'Código Civil (CC)',              tag: 'cc',            pastas: [
      '02 - Áreas/Base Jurídica/02_DIREITO_PRIVADO/DIREITO_CIVIL/Artigos/LIVRO-I',
      '02 - Áreas/Base Jurídica/02_DIREITO_PRIVADO/DIREITO_CIVIL/Artigos/LIVRO-II',
      '02 - Áreas/Base Jurídica/02_DIREITO_PRIVADO/DIREITO_CIVIL/Artigos/LIVRO-III',
      '02 - Áreas/Base Jurídica/02_DIREITO_PRIVADO/DIREITO_CIVIL/Artigos/LIVRO-IV',
      '02 - Áreas/Base Jurídica/02_DIREITO_PRIVADO/DIREITO_CIVIL/Artigos/LIVRO-V',
      'Fenice bRain/02_DIREITO_PRIVADO/DIREITO_CIVIL/Artigos/LIVRO-I',
      'Fenice bRain/02_DIREITO_PRIVADO/DIREITO_CIVIL/Artigos/LIVRO-II',
      'Fenice bRain/02_DIREITO_PRIVADO/DIREITO_CIVIL/Artigos/LIVRO-III',
      'Fenice bRain/02_DIREITO_PRIVADO/DIREITO_CIVIL/Artigos/LIVRO-IV',
      'Fenice bRain/02_DIREITO_PRIVADO/DIREITO_CIVIL/Artigos/LIVRO-V',
      '02 - Áreas/Base Jurídica/02_DIREITO_PRIVADO/DIREITO_CIVIL/Artigos/L10406',
      'Fenice bRain/02_DIREITO_PRIVADO/DIREITO_CIVIL/Artigos/L10406',
    ], codigo: 'CC' },
  { label: 'LINDB — Lei de Introdução',      tag: 'lindb',         pastas: ['02 - Áreas/Base Jurídica/02_DIREITO_PRIVADO/DIREITO_CIVIL/Artigos/LINDB', 'Fenice bRain/02_DIREITO_PRIVADO/DIREITO_CIVIL/Artigos/LINDB'], codigo: 'LINDB'},
  { label: 'D9830 — Decreto LINDB (2019)',   tag: 'd9830',         pasta: 'Fenice bRain/02_DIREITO_PRIVADO/DIREITO_CIVIL/Artigos/D9830',  codigo: 'D9830'},

  // ━━━ DIREITO PENAL ━━━
  { label: 'Código Penal (CP)',              tag: 'direito-penal', pastas: [
      '02 - Áreas/Base Jurídica/04_DIREITO_PENAL/CÓDIGO_PENAL/Crimes',
      'Fenice bRain/04_DIREITO_PENAL/CÓDIGO_PENAL/Artigos/DEL2848',
    ], codigo: 'CP' },

  // ━━━ DIREITO PROCESSUAL ━━━
  { label: 'CPC — Código Processo Civil',    tag: 'cpc',           pastas: [
      '02 - Áreas/Base Jurídica/03_PROCESSO_CIVIL/CÓDIGO_PROCESSO_CIVIL/Artigos/LIVRO-I',
      '02 - Áreas/Base Jurídica/03_PROCESSO_CIVIL/CÓDIGO_PROCESSO_CIVIL/Artigos/LIVRO-II',
      '02 - Áreas/Base Jurídica/03_PROCESSO_CIVIL/CÓDIGO_PROCESSO_CIVIL/Artigos/LIVRO-III',
      '02 - Áreas/Base Jurídica/03_PROCESSO_CIVIL/CÓDIGO_PROCESSO_CIVIL/Artigos/LIVRO-IV',
      '02 - Áreas/Base Jurídica/03_PROCESSO_CIVIL/CÓDIGO_PROCESSO_CIVIL/Artigos/LIVRO-V',
      'Fenice bRain/03_PROCESSO_CIVIL/CÓDIGO_PROCESSO_CIVIL/Artigos/LIVRO-I',
      'Fenice bRain/03_PROCESSO_CIVIL/CÓDIGO_PROCESSO_CIVIL/Artigos/LIVRO-II',
      'Fenice bRain/03_PROCESSO_CIVIL/CÓDIGO_PROCESSO_CIVIL/Artigos/LIVRO-III',
      'Fenice bRain/03_PROCESSO_CIVIL/CÓDIGO_PROCESSO_CIVIL/Artigos/LIVRO-IV',
      'Fenice bRain/03_PROCESSO_CIVIL/CÓDIGO_PROCESSO_CIVIL/Artigos/LIVRO-V',
      'Fenice bRain/03_PROCESSO_CIVIL/CÓDIGO_PROCESSO_CIVIL/Artigos/L13105',
    ], codigo: 'CPC' },
  { label: 'CPP — Código Processo Penal',    tag: 'cpp',           pasta: 'Fenice bRain/04_DIREITO_PENAL/CÓDIGO_PROCESSO_PENAL', codigo: 'CPP' },

  // ━━━ DIREITO CONSUMERISTA & COMERCIAL ━━━
  { label: 'Código do Consumidor (CDC)',     tag: 'cdc',           pastas: ['02 - Áreas/Base Jurídica/02_DIREITO_PRIVADO/CÓDIGO_CONSUMIDOR', 'Fenice bRain/02_DIREITO_PRIVADO/CÓDIGO_CONSUMIDOR'], codigo: 'CDC' },

  // ━━━ DIREITO ADMINISTRATIVO ━━━
  { label: 'Lei Improbidade (L8429)',        tag: 'improbidade',   pasta: 'Fenice bRain/07_DIREITO_ADMINISTRATIVO/DIREITO_ADMINISTRATIVO/Artigos/L8429',  codigo: 'L8429'},
  { label: 'Lei Anticorrupção (L12846)',     tag: 'anticorrupção', pasta: 'Fenice bRain/07_DIREITO_ADMINISTRATIVO/DIREITO_ADMINISTRATIVO/Artigos/L12846', codigo: 'L12846'},
  { label: 'Lei Acesso Info (L12527)',       tag: 'lai',           pasta: 'Fenice bRain/07_DIREITO_ADMINISTRATIVO/DIREITO_ADMINISTRATIVO/Artigos/L12527', codigo: 'L12527'},

  // ━━━ DIREITO PREVIDENCIÁRIO ━━━
  { label: 'Lei Custeio (L8212)',            tag: 'previdenciario', pasta: 'Fenice bRain/08_DIREITOS_ESPECIALIZADOS/DIREITO_PREVIDENCIARIO/Artigos/L8212', codigo: 'L8212'},
  { label: 'Lei Benefício (L8213)',          tag: 'previdenciario', pasta: 'Fenice bRain/08_DIREITOS_ESPECIALIZADOS/DIREITO_PREVIDENCIARIO/Artigos/L8213', codigo: 'L8213'},

  // ━━━ DIREITO DIGITAL & TECNOLOGIA ━━━
  { label: 'Marco Civil da Internet',        tag: 'marco-civil',   pasta: 'Fenice bRain/08_DIREITOS_ESPECIALIZADOS/DIREITO_DIGITAL/Artigos/L12965', codigo: 'MCI'  },
  { label: 'LGPD — Lei Proteção Dados',      tag: 'lgpd',          pasta: 'Fenice bRain/08_DIREITOS_ESPECIALIZADOS/DIREITO_DIGITAL/Artigos/L13709', codigo: 'LGPD' },

  // ━━━ DIREITO INTERNACIONAL & TRATADOS ━━━
  { label: 'CADH — Convenção Am. Dir. Hum.', tag: 'internacional', pasta: 'Fenice bRain/08_DIREITOS_ESPECIALIZADOS/DIREITO_INTERNACIONAL/Tratados/Convencao-Americana-Direitos-Humanos', codigo: 'CADH', isReferencia: true },
  { label: 'CVDT — Conv. Viena Tratados',    tag: 'internacional', pasta: 'Fenice bRain/08_DIREITOS_ESPECIALIZADOS/DIREITO_INTERNACIONAL/Tratados/Convencao-Viena-Direito-dos-Tratados', codigo: 'CVDT', isReferencia: true },

  // ━━━ JURISPRUDÊNCIA STF ━━━
  { label: 'SV — Súmulas Vinculantes STF',  tag: 'sumula-vinculante', pasta: '02 - Áreas/Base Jurídica/03_PROCESSO_CIVIL/STF_SUMULAS/Vinculantes', codigo: 'SV',    buscaPorSumula: true },
  { label: 'S-STF — Súmulas Comuns STF',    tag: 'sumula',            pasta: '02 - Áreas/Base Jurídica/03_PROCESSO_CIVIL/STF_SUMULAS/Comuns',    codigo: 'S-STF', buscaPorSumula: true },

  // ━━━ PROFISSÕES & ENTIDADES ━━━
  { label: 'OAB — Ordem dos Advogados',     tag: 'oab',           pasta: '02 - Áreas/Base Jurídica/09_REFERENCIAS/OAB', codigo: 'OAB', isReferencia: true },

  // ━━━ ESPECIAL: ENUNCIADOS ━━━
  { label: '📋 Enunciados CJF',             tag: 'enunciados-cjf', pasta: '02 - Áreas/Base Jurídica/00_ESTRUTURA_CONSTITUCIONAL/ENUNCIADOS_CJF', codigo: 'ENUM', isEnunciados: true },
  { label: '⚡ ATOMIZAR — Skill de IA',     tag: 'atomizar',       pasta: '', codigo: 'ATOM', isAtomizar: true },
];

// ─── Parseia o conteúdo do arquivo .md ───────────────────────
function parseArtigoMD(content) {
  content = content.replace(/\r\n/g, '\n');

  const result = {
    textoBase: '',
    paragrafos: [],       // [{label, texto}]
    incisos:    [],       // [{label, texto}]
    alineas:    [],       // [{label, texto}]
    correlatos: [],       // strings (wikilinks + texto)
    videLeis:   [],       // [{numero, ano, label}]
    emendas:    [],       // [{numero, descricao}]
    analiseTecnica: null, // {[titulo]: [linhas]}
  };

  // ── Extrai redação (bloco "> " após "## REDACAO LEGAL") ──
  const mRedacao = content.match(/##[^\n]*REDA[^\n]*\n+((?:>[^\n]*\n?)+)/i);
  let redacao = '';
  if (mRedacao) {
    redacao = mRedacao[1]
      .split('\n')
      .map(l => l.replace(/^>\s?/, '').trim())
      .filter(Boolean)
      .join(' ');
  }

  if (redacao && !redacao.startsWith('[Reda')) {
    // ── Texto base: tudo antes do primeiro § ou Parágrafo ──
    const baseEnd = redacao.search(/§\s*\d|[Pp]ar[áa]grafo\s+[úu]nico|\bI\s*[-–—]/);
    result.textoBase = (baseEnd > 0 ? redacao.slice(0, baseEnd) : redacao).trim();

    // ── Parágrafo único ──
    const mPU = redacao.match(/[Pp]ar[áa]grafo\s+[úu]nico\s*[.:]?\s*(.+?)(?=§\s*\d|[Pp]ar[áa]grafo\s+[úu]nico|\bI{1,3}V?\s*[-–—]|$)/s);
    if (mPU) result.paragrafos.push({ label: 'Parágrafo único', texto: mPU[1].replace(/\s+/g, ' ').trim() });

    // ── Parágrafos numerados: §1°, §2°, §3° ... ──
    const paragIter = [...redacao.matchAll(/§\s*(\d+)\s*[°oºO.]?\s+(.+?)(?=§\s*\d|[Pp]ar[áa]grafo\s+[úu]nico|$)/gs)];
    for (const m of paragIter) {
      result.paragrafos.push({ label: `§ ${m[1]}°`, texto: m[2].replace(/\s+/g, ' ').trim() });
    }

    // ── Incisos: I –, II –, III – ... até X ──
    const ROMANOS = ['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII','XIII','XIV','XV','XVI','XVII','XVIII','XIX','XX'];
    const incisoRE = new RegExp(
      `\\b(${ROMANOS.map(r => r.replace(/I/g,'I').replace(/V/g,'V').replace(/X/g,'X')).join('|')})\\s*[-–—]\\s*(.+?)(?=;?\\s*(?:${ROMANOS.join('|')})\\s*[-–—]|§|[Pp]ar[áa]grafo|$)`,
      'gs'
    );
    for (const m of [...redacao.matchAll(incisoRE)]) {
      const texto = m[2].replace(/\s+/g, ' ').trim().replace(/[;,]$/, '');
      if (texto.length > 3) result.incisos.push({ label: m[1], texto });
    }

    // ── Alíneas: a), b), c) ... ──
    for (const m of [...redacao.matchAll(/\b([a-h])\)\s*(.+?)(?=\b[a-h]\)|;|$)/gs)]) {
      const texto = m[2].replace(/\s+/g, ' ').trim();
      if (texto.length > 3) result.alineas.push({ label: `${m[1]})`, texto });
    }

    // ── Vide Lei XX.XXX[, de AAAA]: referências inline na redação ──
    const videLeiRE = /\(Vide\s+Lei[^)]*?n[ºo°]?\s*([\d.]+)(?:[,/]\s*(?:de\s*)?(\d{4}))?\)/gi;
    for (const m of [...redacao.matchAll(videLeiRE)]) {
      const numero = m[1];
      const ano = m[2] || '';
      if (!result.videLeis.some(v => v.numero === numero)) {
        result.videLeis.push({ numero, ano, label: `Lei nº ${numero}${ano ? `, de ${ano}` : ''}` });
      }
    }
  } else {
    // ── Fallback: template "## 📄 TEXTO LEGAL" com **Caput:** / **Parágrafo único:** / **§ N°:** ──
    const mTexto = content.match(/##[^\n]*TEXTO LEGAL[^\n]*\n+([\s\S]*?)(?=\n##|\n---|$)/i);
    if (mTexto) {
      const bloco = mTexto[1];

      const mCaput = bloco.match(/\*\*Caput:?\*\*\s*(.+?)(?=\n\n|\*\*|$)/si);
      if (mCaput) result.textoBase = mCaput[1].replace(/\s+/g, ' ').trim();

      const mPU = bloco.match(/\*\*Par[áa]grafo\s+[úu]nico:?\*\*\s*(.+?)(?=\n\n|\*\*|$)/si);
      if (mPU) result.paragrafos.push({ label: 'Parágrafo único', texto: mPU[1].replace(/\s+/g, ' ').trim() });

      for (const m of [...bloco.matchAll(/\*\*§\s*(\d+)\s*[°ºo]?:?\*\*\s*(.+?)(?=\n\n|\*\*|$)/gsi)]) {
        result.paragrafos.push({ label: `§ ${m[1]}°`, texto: m[2].replace(/\s+/g, ' ').trim() });
      }
    }
  }

  // ── Jurisprudência do corpo: seção ## JURISPRUDENCIA ou ## ⚖️ JURISPRUDÊNCIA ──
  // Só extrai se houver blockquotes reais (não placeholder)
  const mJurisCorpo = content.match(/##[^\n]*JURISPRUD[^\n]*\n([\s\S]*?)(?=\n##(?!#)|$)/i);
  if (mJurisCorpo) {
    const bloco = mJurisCorpo[1];
    const jurisCorpo = [];
    // Padrão: **TRIBUNAL — label**\n> texto
    const bolqRE = /\*\*([^*\n]+)\*\*[^\n]*\n((?:>[^\n]*\n?)+)/g;
    for (const m of [...bloco.matchAll(bolqRE)]) {
      const tribunal = m[1].trim();
      const texto = m[2].split('\n').map(l => l.replace(/^>\s?/, '').trim()).filter(Boolean).join(' ');
      if (texto && !texto.startsWith('[')) jurisCorpo.push({ tribunal, resumo: texto });
    }
    if (jurisCorpo.length) result.jurisCorpo = jurisCorpo;
  }

  // ── Súmulas: seção ## ENUNCIADO (quando não há REDACAO LEGAL) ──
  if (!redacao) {
    const mEnunciado = content.match(/##[^\n]*ENUNCIADO[^\n]*\n+((?:>[^\n]*\n?)+)/i);
    if (mEnunciado) {
      result.textoBase = mEnunciado[1]
        .split('\n')
        .map(l => l.replace(/^>\s?/, '').trim())
        .filter(Boolean)
        .join(' ');
    }

    // ── Base constitucional / correlatos da súmula ──
    const mBase = content.match(/##[^\n]*BASE\s+CONSTITU[^\n]*\n([\s\S]*?)(?=\n##(?!#)|$)/i);
    if (mBase) {
      const links = [...mBase[1].matchAll(/\[\[([^\]|]+)(?:\|[^\]]+)?\]\]([^\n]*)/g)];
      for (const l of links) {
        const nome = l[1].trim();
        const extra = l[2].replace(/^[\s\-—]+/, '').trim();
        if (nome) result.correlatos.push(extra ? `${nome} — ${extra}` : nome);
      }
    }
  }

  // ── Emendas Constitucionais: seção ## EMENDAS CONSTITUCIONAIS ──
  const mEmendas = content.match(/##[^\n]*EMENDA[^\n]*\n([\s\S]*?)(?=\n##(?!#)|$)/i);
  if (mEmendas) {
    const bloco = mEmendas[1];
    // Parse linhas tipo: - **EC nº 1/1992** — descrição
    const linhasEmendas = [...bloco.matchAll(/[-•*]\s*\*{1,2}EC\s+n[ºo°]?\s*([\d/]+)\*{1,2}\s*(?:[—–-]\s*)?([^\n]*)/gi)];
    for (const m of linhasEmendas) {
      const numero = m[1];
      const descricao = m[2].trim().replace(/([—–-]\s*)?/, '').trim();
      if (numero && !result.emendas.some(e => e.numero === numero)) {
        result.emendas.push({ numero, descricao });
      }
    }
  }

  // ── Análise Técnica: subseções ### dentro de ## ANÁLISE TÉCNICA ──
  const mAnalise = content.match(/##[^\n]*AN[ÁA]LISE\s+T[ÉE]CNICA[^\n]*\n([\s\S]*?)(?=\n##(?!#)|$)/i);
  if (mAnalise) {
    const bloco = mAnalise[1];
    const secoes = {};
    const reSubsec = /###\s+(.+?)\n([\s\S]*?)(?=\n###\s|$)/gi;
    for (const m of [...bloco.matchAll(reSubsec)]) {
      const titulo = m[1].trim();
      const linhas = (m[2] || '').split('\n').filter(l => {
        const t = l.trim();
        return t && !/^\|[\s\-:]+\|/.test(t) && !/^-{3,}$/.test(t); // remove separadores de tabela e <hr>
      });
      if (linhas.length) secoes[titulo] = linhas;
    }
    if (Object.keys(secoes).length) result.analiseTecnica = secoes;
  }

  // ── Correlatos: wikilinks da seção ARTIGOS CORRELATOS ──
  const mCorr = content.match(/##[^\n]*CORRELAT[^\n]*\n([\s\S]*?)(?=\n##(?!#)|$)/i);
  if (mCorr) {
    const links = [...mCorr[1].matchAll(/\[\[([^\]|]+)(?:\|[^\]]+)?\]\]([^\n]*)/g)];
    for (const l of links) {
      const nome = l[1].trim();
      const extra = l[2].replace(/^[\s\-—]+/, '').trim();
      if (nome && !nome.includes('INDEX')) {
        result.correlatos.push(extra ? `${nome} — ${extra}` : nome);
      }
    }
  }

  return result;
}

// ─── Helpers para busca multi-pasta ──────────────────────────
function obterPastas(config) {
  if (Array.isArray(config.pastas) && config.pastas.length) return config.pastas;
  if (config.pasta) return [config.pasta];
  return [];
}

function pastaEhAncestral(pasta, path) {
  if (!pasta) return true;
  const norm = p => p.replace(/\/+$/, '');
  const pastaNorm = norm(pasta);
  return path === pastaNorm || path.startsWith(pastaNorm + '/');
}

// ─── Modal 1: Selecionar Código ──────────────────────────────
class CodigoModal extends SuggestModal {
  constructor(app, onEscolha) {
    super(app);
    this.onEscolha = onEscolha;
    this.setPlaceholder('Selecione o Código Jurídico...');
  }
  getSuggestions(q) {
    return CODIGOS.filter(c => c.label.toLowerCase().includes(q.toLowerCase()));
  }
  renderSuggestion(item, el) { el.createEl('div', { text: item.label }); }
  onChooseSuggestion(item) { this.onEscolha(item); }
}

// ─── Modal 1.5: Resultados de Tema ───────────────────────────
class TemaModal extends SuggestModal {
  constructor(app, resultados, onEscolha) {
    super(app);
    this.resultados = resultados;
    this.onEscolha = onEscolha;
    this.setPlaceholder('Selecione um resultado...');
  }
  getSuggestions(q) {
    return this.resultados.filter(r => r.label.toLowerCase().includes(q.toLowerCase()));
  }
  renderSuggestion(item, el) {
    const div = el.createEl('div');
    div.createEl('strong', { text: item.label });
    if (item.meta.tags && Array.isArray(item.meta.tags)) {
      const tagsEl = div.createEl('div', { text: `Tags: ${item.meta.tags.slice(0, 3).join(', ')}` });
      Object.assign(tagsEl.style, { fontSize: '11px', color: 'var(--text-muted)' });
    }
  }
  onChooseSuggestion(item) { this.onEscolha(item); }
}

// ─── Modal 2: Número do Artigo ───────────────────────────────
class ArtigoModal extends Modal {
  constructor(app, config, onBuscar, placeholder) {
    super(app);
    this.config = config;
    this.onBuscar = onBuscar;
    this.placeholderText = placeholder || 'Ex: 48  |  121  |  1.228';
  }
  onOpen() {
    const { contentEl } = this;
    contentEl.empty();
    contentEl.createEl('h3', { text: `${this.config.codigo}` });

    const input = contentEl.createEl('input', {
      type: 'text', placeholder: this.placeholderText,
    });
    Object.assign(input.style, {
      width: '100%', fontSize: '18px', padding: '8px 12px',
      margin: '12px 0 16px', borderRadius: '6px', boxSizing: 'border-box',
      border: '1px solid var(--interactive-accent)',
      background: 'var(--background-secondary)', color: 'var(--text-normal)',
    });

    const row = contentEl.createEl('div');
    Object.assign(row.style, { display: 'flex', gap: '8px', justifyContent: 'flex-end' });

    row.createEl('button', { text: 'Cancelar' }).addEventListener('click', () => this.close());

    const btnOk = row.createEl('button', { text: 'Buscar →' });
    Object.assign(btnOk.style, {
      padding: '6px 20px', fontWeight: 'bold', cursor: 'pointer',
      background: 'var(--interactive-accent)', color: 'var(--text-on-accent)',
      border: 'none', borderRadius: '4px',
    });

    const dica = contentEl.createEl('div', {
      text: '💡 Dica: Digite um número (48, 121) ou um tema (tratado, viena, protocolo)'
    });
    Object.assign(dica.style, {
      fontSize: '12px', color: 'var(--text-muted)', marginTop: '8px', fontStyle: 'italic'
    });

    const go = () => {
      const n = input.value.trim();
      if (!n) return;
      this.close();
      this.onBuscar(n);
    };
    btnOk.addEventListener('click', go);
    input.addEventListener('keydown', e => { if (e.key === 'Enter') go(); if (e.key === 'Escape') this.close(); });
    setTimeout(() => input.focus(), 50);
  }
  onClose() { this.contentEl.empty(); }
}

// ─── Modal 3: Painel compacto — sem scroll ───────────────────
// Mostra apenas estrutura + correlatos (o texto está na nota aberta)
class InfoModal extends Modal {
  constructor(app, found, config, num, parsed, enunciados, acessorios, onNovaBusca, onBuscarLei) {
    super(app);
    this.found       = found;
    this.config      = config;
    this.num         = num;
    this.parsed      = parsed;
    this.enunciados  = enunciados || [];
    this.acessorios  = acessorios || null;
    this.emendas     = parsed.emendas || [];
    this.onNovaBusca = onNovaBusca;
    this.onBuscarLei = onBuscarLei;
    this.modalEl.style.maxWidth = '600px';
    this.modalEl.style.width   = '92vw';
  }

  onOpen() {
    const { contentEl } = this;
    contentEl.empty();
    Object.assign(contentEl.style, { maxHeight: '80vh', overflowY: 'auto', paddingRight: '4px' });

    const { textoBase, paragrafos, incisos, alineas, correlatos, videLeis, jurisCorpo, analiseTecnica } = this.parsed;

    // ── Cabeçalho ──
    const h = contentEl.createEl('div');
    Object.assign(h.style, {
      display: 'flex', justifyContent: 'space-between',
      alignItems: 'center', marginBottom: '10px',
    });
    const titulo = this.config.buscaPorSumula
      ? `Súmula ${this.num} — ${this.config.codigo}`
      : `Art. ${this.num} — ${this.config.codigo}`;
    h.createEl('strong', { text: titulo })
     .style.fontSize = '16px';

    // botão X no canto
    const btnX = h.createEl('button', { text: '✕' });
    Object.assign(btnX.style, {
      background: 'none', border: 'none', cursor: 'pointer',
      fontSize: '16px', color: 'var(--text-muted)', padding: '0 4px',
    });
    btnX.addEventListener('click', () => this.close());

    // ── Estrutura do artigo (compacta, sem scroll) ──
    const card = contentEl.createEl('div');
    Object.assign(card.style, {
      background: 'var(--background-secondary)',
      border: '1px solid var(--background-modifier-border)',
      borderRadius: '6px', padding: '10px 14px',
      fontSize: '13px', lineHeight: '1.6', marginBottom: '10px',
    });

    const temEstrutura = paragrafos.length || incisos.length || alineas.length;

    if (!temEstrutura && !textoBase) {
      card.createEl('p', { text: '⚠ Redação placeholder — rode o pipeline Planalto.' })
          .style.color = 'var(--text-muted)';
    } else {
      // Caput / Enunciado completo
      if (textoBase) {
        const caput = card.createEl('p');
        caput.style.marginTop = '0';
        const prefixo = this.config.buscaPorSumula ? `Súmula ${this.num}. ` : `Art. ${this.num}. `;
        caput.createEl('strong', { text: prefixo });
        caput.appendText(textoBase);
      }

      // Incisos — label + texto resumido
      if (incisos.length) {
        card.createEl('hr').style.margin = '6px 0';
        for (const inc of incisos) {
          const p = card.createEl('p');
          Object.assign(p.style, { marginBottom: '3px', marginLeft: '12px' });
          p.createEl('strong', { text: `${inc.label} — ` });
          const resumo = inc.texto.length > 150 ? inc.texto.slice(0, 150) + '…' : inc.texto;
          p.appendText(resumo);
        }
      }

      // Alíneas — label + texto resumido
      if (alineas.length) {
        for (const al of alineas) {
          const p = card.createEl('p');
          Object.assign(p.style, { marginBottom: '3px', marginLeft: '24px', color: 'var(--text-muted)' });
          p.createEl('strong', { text: `${al.label} ` });
          const resumo = al.texto.length > 120 ? al.texto.slice(0, 120) + '…' : al.texto;
          p.appendText(resumo);
        }
      }

      // Parágrafos — cada um com seu texto completo (geralmente curtos)
      if (paragrafos.length) {
        card.createEl('hr').style.margin = '6px 0';
        for (const pg of paragrafos) {
          const p = card.createEl('p');
          p.style.marginBottom = '4px';
          p.createEl('strong', { text: `${pg.label}. ` });
          p.appendText(pg.texto);
        }
      }
    }

    // ── Análise Técnica ──
    if (analiseTecnica) {
      for (const [titulo, linhas] of Object.entries(analiseTecnica)) {
        const isTable = linhas.some(l => l.trim().startsWith('|'));
        const sec = contentEl.createEl('div');
        Object.assign(sec.style, {
          borderTop: '1px solid var(--background-modifier-border)',
          paddingTop: '8px', marginBottom: '10px', fontSize: '12px',
        });
        sec.createEl('strong', { text: `📘 ${titulo}` }).style.fontSize = '13px';
        if (isTable) {
          const tbl = sec.createEl('table');
          Object.assign(tbl.style, {
            width: '100%', borderCollapse: 'collapse',
            marginTop: '6px', fontSize: '11px',
          });
          for (const linha of linhas) {
            if (!linha.trim().startsWith('|')) continue;
            const cells = linha.split('|').map(c => c.trim()).filter(Boolean);
            const tr = tbl.createEl('tr');
            for (const cell of cells) {
              const td = tr.createEl('td');
              Object.assign(td.style, {
                border: '1px solid var(--background-modifier-border)',
                padding: '3px 6px',
              });
              td.appendText(cell.replace(/\*\*/g, ''));
            }
          }
        } else {
          for (const linha of linhas) {
            const t = linha.trim();
            if (!t) continue;
            const p = sec.createEl('p');
            Object.assign(p.style, {
              marginTop: '4px', marginLeft: '4px',
              borderLeft: '2px solid var(--interactive-accent)',
              paddingLeft: '8px', lineHeight: '1.5',
              color: t.startsWith('[') ? 'var(--text-muted)' : 'inherit',
            });
            p.appendText(t);
          }
        }
      }
    }

    // ── Correlatos ──
    if (correlatos.length) {
      const sec = contentEl.createEl('div');
      Object.assign(sec.style, {
        borderTop: '1px solid var(--background-modifier-border)',
        paddingTop: '8px', marginBottom: '10px',
        fontSize: '13px',
      });
      sec.createEl('span', { text: '🔗 ' }).style.fontSize = '12px';
      sec.createEl('strong', { text: 'Correlatos  ' });
      correlatos.forEach((c, i) => {
        if (i) sec.appendText(' · ');
        const a = sec.createEl('span', { text: c });
        a.style.color = 'var(--text-accent)';
        a.style.cursor = 'pointer';
        a.title = `Abrir ${c}`;
        a.addEventListener('click', () => {
          this.close();
          const nome = c.split(' — ')[0].trim();
          this.app.workspace.openLinkText(nome, '', false);
        });
      });
    }

    // ── Vide Lei ──
    if (videLeis && videLeis.length) {
      const sec = contentEl.createEl('div');
      Object.assign(sec.style, {
        borderTop: '1px solid var(--background-modifier-border)',
        paddingTop: '8px', marginBottom: '10px',
        fontSize: '13px',
      });
      sec.createEl('span', { text: '📖 ' }).style.fontSize = '12px';
      sec.createEl('strong', { text: 'Vide  ' });
      videLeis.forEach((v, i) => {
        if (i) sec.appendText(' · ');
        const a = sec.createEl('span', { text: v.label });
        a.style.color = 'var(--text-accent)';
        a.style.cursor = 'pointer';
        a.title = `Buscar artigos da ${v.label}`;
        a.addEventListener('click', () => {
          this.close();
          if (this.onBuscarLei) this.onBuscarLei(v.numero);
        });
      });
    }

    // ── Emendas Constitucionais ──
    if (this.emendas && this.emendas.length) {
      const sec = contentEl.createEl('div');
      Object.assign(sec.style, {
        borderTop: '1px solid var(--background-modifier-border)',
        paddingTop: '8px', marginBottom: '10px',
        fontSize: '13px',
      });
      sec.createEl('span', { text: '📝 ' }).style.fontSize = '12px';
      sec.createEl('strong', { text: 'Emendas  ' });

      for (const em of this.emendas) {
        const p = sec.createEl('p');
        Object.assign(p.style, {
          marginLeft: '4px', marginBottom: '6px',
          borderLeft: '2px solid var(--interactive-accent)',
          paddingLeft: '8px', lineHeight: '1.4', fontSize: '12px',
        });
        const label = p.createEl('strong', { text: `EC nº ${em.numero}` });
        label.style.color = 'var(--text-accent)';
        if (em.descricao) {
          p.appendText(` — ${em.descricao}`);
        }
      }
    }

    // ── Enunciados CJF ──
    if (this.enunciados.length) {
      const sec = contentEl.createEl('div');
      Object.assign(sec.style, {
        borderTop: '1px solid var(--background-modifier-border)',
        paddingTop: '8px', marginBottom: '10px', fontSize: '13px',
      });
      const hdr = sec.createEl('p');
      hdr.style.marginBottom = '6px';
      hdr.createEl('strong', { text: '📋 Enunciados CJF' });

      for (const e of this.enunciados) {
        const p = sec.createEl('p');
        Object.assign(p.style, {
          marginLeft: '4px', marginBottom: '8px',
          borderLeft: '2px solid var(--interactive-accent)',
          paddingLeft: '8px', lineHeight: '1.5',
        });
        // Label clicável → abre o .md do enunciado
        const jSigla = (e.jornada.match(/^([IVX]+)/) || ['',''])[1];
        const link = p.createEl('span', { text: `Enunciado ${e.num} (${jSigla} JDC): ` });
        Object.assign(link.style, {
          color: 'var(--text-accent)', cursor: 'pointer', fontWeight: 'bold',
        });
        link.title = 'Abrir enunciado completo';
        link.addEventListener('click', () => {
          this.close();
          this.app.workspace.openLinkText(`Enunciado-${e.num}`, '', false);
        });
        p.appendText(e.texto);
      }
    }

    // ── Jurisprudência do corpo do artigo (seção ## JURISPRUDENCIA real) ──
    if (jurisCorpo && jurisCorpo.length && !this.acessorios?.jurisprudencia?.length) {
      const sec = contentEl.createEl('div');
      Object.assign(sec.style, {
        borderTop: '1px solid var(--background-modifier-border)',
        paddingTop: '8px', marginBottom: '10px', fontSize: '13px',
      });
      sec.createEl('strong', { text: '⚖️ Jurisprudência  ' });
      for (const j of jurisCorpo) {
        const p = sec.createEl('p');
        Object.assign(p.style, {
          marginLeft: '4px', marginBottom: '4px',
          borderLeft: '2px solid var(--interactive-accent)',
          paddingLeft: '8px', lineHeight: '1.4', fontSize: '12px',
        });
        p.createEl('strong', { text: `${j.tribunal}: ` });
        p.appendText(j.resumo || '');
      }
    }

    // ── Acessórios do frontmatter (LIVRO-* format) ──
    const ac = this.acessorios;
    if (ac) {
      // Jurisprudência
      const juris = ac.jurisprudencia || [];
      if (juris.length) {
        const sec = contentEl.createEl('div');
        Object.assign(sec.style, {
          borderTop: '1px solid var(--background-modifier-border)',
          paddingTop: '8px', marginBottom: '10px', fontSize: '13px',
        });
        sec.createEl('strong', { text: '⚖️ Jurisprudência  ' });
        for (const j of juris) {
          const p = sec.createEl('p');
          Object.assign(p.style, {
            marginLeft: '4px', marginBottom: '4px',
            borderLeft: '2px solid var(--interactive-accent)',
            paddingLeft: '8px', lineHeight: '1.4', fontSize: '12px',
          });
          p.createEl('strong', { text: `${j.tribunal}: ` });
          p.appendText(j.resumo || '');
        }
      }

      // Enunciados do frontmatter (complementa o índice JSON)
      const acEnums = ac.enunciados || [];
      if (acEnums.length && !this.enunciados.length) {
        const sec = contentEl.createEl('div');
        Object.assign(sec.style, {
          borderTop: '1px solid var(--background-modifier-border)',
          paddingTop: '8px', marginBottom: '10px', fontSize: '13px',
        });
        sec.createEl('strong', { text: '📋 Enunciados  ' });
        for (const e of acEnums) {
          const p = sec.createEl('p');
          Object.assign(p.style, { marginLeft: '4px', marginBottom: '3px', fontSize: '12px' });
          p.createEl('strong', { text: `Enunciado ${e.numero}` });
          if (e.tribunal) p.appendText(` (${e.tribunal})`);
        }
      }

      // Artigos relacionados do frontmatter (referências cruzadas reais)
      const acRel = ac.artigos_relacionados || [];
      if (acRel.length) {
        const sec = contentEl.createEl('div');
        Object.assign(sec.style, {
          borderTop: '1px solid var(--background-modifier-border)',
          paddingTop: '8px', marginBottom: '10px', fontSize: '13px',
        });
        sec.createEl('span', { text: '🔗 ' }).style.fontSize = '12px';
        sec.createEl('strong', { text: 'Relacionados  ' });
        acRel.forEach((r, i) => {
          if (i) sec.appendText(' · ');
          const label = `Art. ${r.artigo}${r.titulo ? ' — ' + r.titulo : ''}`;
          const a = sec.createEl('span', { text: label });
          a.style.color = 'var(--text-accent)';
          a.style.cursor = 'pointer';
          a.title = r.nota || `Abrir Art. ${r.artigo}`;
          a.addEventListener('click', () => {
            this.close();
            this.app.workspace.openLinkText(`Art. ${r.artigo}`, '', false);
          });
        });
      }
    }

    // ── Botões ──
    const row = contentEl.createEl('div');
    Object.assign(row.style, { display: 'flex', gap: '8px' });

    const btnNova = row.createEl('button', { text: '🔄 Nova Busca' });
    Object.assign(btnNova.style, {
      flex: '1', padding: '7px', fontWeight: 'bold', cursor: 'pointer',
      background: 'var(--interactive-accent)', color: 'var(--text-on-accent)',
      border: 'none', borderRadius: '4px',
    });
    btnNova.addEventListener('click', () => {
      this.close();
      setTimeout(() => this.onNovaBusca(), 120);
    });

    const btnFechar = row.createEl('button', { text: 'Fechar  [Esc]' });
    Object.assign(btnFechar.style, {
      padding: '7px 14px', cursor: 'pointer', borderRadius: '4px',
    });
    btnFechar.addEventListener('click', () => this.close());
  }

  onClose() { this.contentEl.empty(); }
}

// ─── Plugin Principal ────────────────────────────────────────
class FeniceBuscarArtigo extends Plugin {

  onload() {
    // Limpar console ao abrir Obsidian
    console.clear();
    console.log('✅ Fenice Buscar Artigo v12 — Pronto! (Análise Técnica no InfoModal)');

    // Ctrl+Shift+B — busca por código + número
    this.addCommand({
      id: 'buscar-artigo',
      name: 'Buscar Artigo (Código + Número)',
      hotkeys: [{ modifiers: ['Ctrl', 'Shift'], key: 'B' }],
      callback: () => this.iniciarBusca(),
    });

    // Ctrl+Shift+I — mostra painel do artigo atualmente aberto
    this.addCommand({
      id: 'info-artigo-atual',
      name: 'Info do Artigo Atual (§ Incisos Correlatos)',
      hotkeys: [{ modifiers: ['Ctrl', 'Shift'], key: 'I' }],
      callback: () => this.mostrarInfoAtual(),
    });

    // Carrega index de enunciados CJF
    this.enunciadosIndex = {};
    this.app.vault.adapter
      .read('02 - Áreas/Base Jurídica/00_ESTRUTURA_CONSTITUCIONAL/ENUNCIADOS_CJF/enunciados_index.json')
      .then(txt => {
        this.enunciadosIndex = JSON.parse(txt);
        console.log('Fenice: enunciados CJF carregados —',
          Object.keys(this.enunciadosIndex).length, 'artigos');
      })
      .catch(() => console.log('Fenice: enunciados_index.json nao encontrado'));
  }

  iniciarBusca() {
    new CodigoModal(this.app, (config) => {
      // Se é Atomizar, abre painel de seleção
      if (config.isAtomizar) {
        this.abrirAtomizar();
        return;
      }

      // Se é Enunciados, vai direto ao INDEX
      if (config.isEnunciados) {
        new Notice('📋 Abrindo Enunciados CJF...');
        this.app.workspace.openLinkText('02 - Áreas/Base Jurídica/00_ESTRUTURA_CONSTITUCIONAL/ENUNCIADOS_CJF/INDEX-ENUNCIADOS', '', false);
        return;
      }

      // Se é Referência (OAB, CADH, CVDT etc), vai direto ao INDEX
      if (config.isReferencia) {
        new Notice(`📚 Abrindo ${config.codigo}...`);
        this.app.workspace.openLinkText(`${config.pasta}/INDEX`, '', false);
        return;
      }

      // Casos normais: pede número do artigo ou tema
      const placeholder = config.buscaPorSumula
        ? `Número da Súmula (ex: 1, 10, 100)`
        : `Número do Artigo (ex: 48, 121) ou Tema (ex: direitos, responsabilidade)`;

      new ArtigoModal(this.app, config, (num) => {
        this.buscarEAbrir(config, num);
      }, placeholder).open();
    }).open();
  }

  // Painel para escolher qual área atomizar
  abrirAtomizar() {
    const areas = [
      { label: '📚 Direito Constitucional', pasta: '02 - Áreas/Base Jurídica/00_ESTRUTURA_CONSTITUCIONAL/CONSTITUIÇÃO_FEDERAL' },
      { label: '📖 Código Civil', pasta: '02 - Áreas/Base Jurídica/02_DIREITO_PRIVADO/DIREITO_CIVIL' },
      { label: '⚖️  Código Penal', pasta: '02 - Áreas/Base Jurídica/04_DIREITO_PENAL/CÓDIGO_PENAL' },
      { label: '📋 Processo Civil', pasta: '02 - Áreas/Base Jurídica/03_PROCESSO_CIVIL/CÓDIGO_PROCESSO_CIVIL' },
      { label: '🔨 Processo Penal', pasta: '02 - Áreas/Base Jurídica/04_DIREITO_PENAL/CÓDIGO_PROCESSO_PENAL' },
      { label: '🛡️  Direito Administrativo', pasta: '02 - Áreas/Base Jurídica/07_DIREITO_ADMINISTRATIVO/DIREITO_ADMINISTRATIVO' },
      { label: '💼 Direito Previdenciário', pasta: '02 - Áreas/Base Jurídica/08_DIREITOS_ESPECIALIZADOS/DIREITO_PREVIDENCIARIO' },
      { label: '🌐 Direito Digital', pasta: '02 - Áreas/Base Jurídica/08_DIREITOS_ESPECIALIZADOS/DIREITO_DIGITAL' },
      { label: '🌍 Direito Internacional', pasta: '02 - Áreas/Base Jurídica/08_DIREITOS_ESPECIALIZADOS/DIREITO_INTERNACIONAL' },
      { label: '🏪 Código Consumidor', pasta: '02 - Áreas/Base Jurídica/02_DIREITO_PRIVADO/CÓDIGO_CONSUMIDOR' },
    ];

    const modal = new SuggestModal(this.app);
    modal.setPlaceholder('Escolha a área para ATOMIZAR...');
    modal.getSuggestions = (q) => areas.filter(a => a.label.toLowerCase().includes(q.toLowerCase()));
    modal.renderSuggestion = (item, el) => el.createEl('div', { text: item.label });
    modal.onChooseSuggestion = (area) => {
      new Notice(`🤖 Iniciando atomização: ${area.label.replace(/^[📚📖⚖️🔨🛡️💼🌐🌍🏪]\s+/, '')}`);
      this.app.workspace.openLinkText(`${area.pasta}/INDEX`, '', false);
    };
    modal.open();
  }

  // Mostra o painel do artigo atualmente aberto no workspace
  async mostrarInfoAtual() {
    const activeFile = this.app.workspace.getActiveFile();
    if (!activeFile) {
      new Notice('Nenhum artigo aberto.', 2000);
      return;
    }

    const meta = this.app.metadataCache.getFileCache(activeFile)?.frontmatter;
    if (!meta?.artigo && !meta?.sumula) {
      new Notice('Arquivo atual não é um artigo ou súmula jurídica.', 3000);
      return;
    }

    // Detecta o código pelo tag do arquivo
    const tags = Array.isArray(meta.tags) ? meta.tags : [];
    const config = CODIGOS.find(c => tags.includes(c.tag))
                || { codigo: 'Lei', tag: '', pasta: '' };

    const num = String(meta.artigo ?? meta.sumula);
    let parsed = { textoBase: '', paragrafos: [], incisos: [], alineas: [], correlatos: [] };
    try {
      const content = await this.app.vault.read(activeFile);
      parsed = parseArtigoMD(content);
    } catch (e) { console.error('Fenice info:', e); }

    const chaveIdx = `${config.tag}:${num}`;
    const enunciados = (this.enunciadosIndex || {})[chaveIdx] || [];

    const acessorios1 = meta.acessorios || null;
    new InfoModal(this.app, activeFile, config, num, parsed, enunciados, acessorios1,
      () => this.iniciarBusca(),
      (lei) => this.buscarPorLei(lei)).open();
  }

  async buscarEAbrir(config, input) {
    const termo = input.trim();
    const isNumero = /^[\d.]+$/.test(termo);

    console.clear();
    console.log(`📥 Input: "${termo}"`);
    console.log(`📊 É número? ${isNumero}`);
    console.log(`⚙️ Config: ${config.codigo}`);

    if (isNumero) {
      console.log(`→ Chamando: buscarPorNumero`);
      this.buscarPorNumero(config, termo);
    } else {
      console.log(`→ Chamando: buscarPorTema`);
      this.buscarPorTema(config, termo);
    }
  }

  // Busca em todo o vault por artigos da Lei nº "numero" (ex: Vide Lei nº 13.105)
  buscarPorLei(numero) {
    const digitos = numero.replace(/\D/g, '');
    const config = { codigo: `Lei ${numero}`, tag: '', pasta: '', pastas: [] };
    this.buscarPorTema(config, digitos);
  }

  async buscarPorNumero(config, num) {
    console.clear();
    console.log(`🔍 Buscando: Art. ${num} em ${config.codigo}`);

    const allFiles = this.app.vault.getFiles();

    const campoChave = config.buscaPorSumula ? 'sumula' : 'artigo';
    const numInt = parseInt(num, 10);
    const bate = (meta) => {
      if (!meta) return false;
      const v = meta[campoChave];
      if (v == null) return false;
      const vs = String(v);
      return vs === num || parseInt(vs, 10) === numInt;
    };

    let found = null;
    for (const pasta of obterPastas(config)) {
      found = allFiles.find(f => pastaEhAncestral(pasta, f.path) && bate(this.app.metadataCache.getFileCache(f)?.frontmatter));
      if (found) break;
    }
    if (!found) {
      found = allFiles.find(f => {
        const meta = this.app.metadataCache.getFileCache(f)?.frontmatter;
        const tags = Array.isArray(meta?.tags) ? meta.tags : [];
        return bate(meta) && tags.includes(config.tag);
      });
    }
    if (!found) { this.avisarNaoEncontrado(config, num); return; }

    console.log(`✅ Encontrado: ${found.path}`);
    new Notice(`✅ Art. ${num} — ${config.codigo}`, 2000);

    await this.app.workspace.openLinkText(found.basename, '', false);

    let parsed = { textoBase: '', paragrafos: [], incisos: [], alineas: [], correlatos: [], videLeis: [], emendas: [] };
    try {
      const content = await this.app.vault.read(found);
      parsed = parseArtigoMD(content);
    } catch (e) { console.error('Fenice buscar:', e); }

    const chaveIdx = `${config.tag}:${num}`;
    const enunciados = (this.enunciadosIndex || {})[chaveIdx] || [];
    const acessorios2 = this.app.metadataCache.getFileCache(found)?.frontmatter?.acessorios || null;

    console.log(`   textoBase: ${parsed.textoBase?.slice(0,60)}...`);
    console.log(`   incisos: ${parsed.incisos.length} | paragrafos: ${parsed.paragrafos.length} | correlatos: ${parsed.correlatos.length}`);
    console.log(`   acessorios:`, acessorios2);

    new InfoModal(this.app, found, config, num, parsed, enunciados, acessorios2,
      () => {
        console.clear();
        this.iniciarBusca();
      },
      (lei) => this.buscarPorLei(lei)).open();
  }

  async buscarPorTema(config, tema) {
    const allFiles = this.app.vault.getFiles();
    const temaBaixo = tema.toLowerCase();
    const resultados = [];
    const MAX_LEITURAS = 300; // teto para não travar o vault

    const pastas = obterPastas(config);
    const pastasNorm = pastas.map(p => p.replace(/\\\\/g, '/'));

    console.log(`🔍 Buscando "${tema}" em ${config.codigo} (${allFiles.length} arquivos total)`);

    // Filtra primeiro por pasta usando só metadados (sem ler conteúdo)
    const candidatos = allFiles.filter(file => {
      const filePath = file.path.replace(/\\\\/g, '/');
      return pastasNorm.length === 0 || pastasNorm.some(p => filePath.startsWith(p.replace(/\/+$/, '') + '/'));
    });

    // Fase 1: busca rápida por título e tags (sem ler arquivo)
    for (const file of candidatos) {
      const meta = this.app.metadataCache.getFileCache(file)?.frontmatter || {};
      const titulo = file.basename.toLowerCase();
      const tags = Array.isArray(meta.tags) ? meta.tags.join(' ').toLowerCase() : '';
      const temNoTitulo = titulo.includes(temaBaixo);
      const temNasTags = tags.includes(temaBaixo);
      if (temNoTitulo || temNasTags) {
        const num = meta.numero || meta.artigo || meta.sumula || '';
        resultados.push({
          file, meta,
          label: num ? `Art. ${num} — ${file.basename}` : file.basename,
          titulo: file.basename,
          relevancia: (temNoTitulo ? 100 : 0) + (temNasTags ? 50 : 0),
          caminho: file.path,
        });
      }
    }

    // Fase 2: leitura de conteúdo só se não achou nada na fase 1 (limitado)
    if (resultados.length === 0) {
      let lidos = 0;
      for (const file of candidatos) {
        if (lidos >= MAX_LEITURAS) break;
        try {
          const content = await this.app.vault.read(file);
          lidos++;
          if (content.toLowerCase().includes(temaBaixo)) {
            const meta = this.app.metadataCache.getFileCache(file)?.frontmatter || {};
            const num = meta.numero || meta.artigo || meta.sumula || '';
            resultados.push({
              file, meta,
              label: num ? `Art. ${num} — ${file.basename}` : file.basename,
              titulo: file.basename,
              relevancia: 10,
              caminho: file.path,
            });
          }
        } catch (e) { console.error(`Erro ao ler ${file.basename}:`, e); }
      }
      if (lidos >= MAX_LEITURAS) {
        new Notice(`⚠ Busca limitada a ${MAX_LEITURAS} arquivos. Refine o termo.`, 4000);
      }
    }

    console.log(`   Candidatos: ${candidatos.length} | Resultados: ${resultados.length}`);

    if (resultados.length === 0) {
      new Notice(`⚠ Nenhum resultado para "${tema}" em ${config.codigo}.`, 4000);
      return;
    }

    // Ordena por relevância (descendente)
    resultados.sort((a, b) => b.relevancia - a.relevancia);

    console.log(`✅ ${resultados.length} resultado(s) encontrado(s)`);

    // Mostra modal de sugestões
    if (resultados.length === 1) {
      this.abrirArquivoTema(resultados[0], config);
    } else {
      new TemaModal(this.app, resultados, (result) => {
        this.abrirArquivoTema(result, config);
      }).open();
    }
  }

  async abrirArquivoTema(result, config) {
    await this.app.workspace.openLinkText(result.file.basename, '', false);

    let parsed = { textoBase: '', paragrafos: [], incisos: [], alineas: [], correlatos: [] };
    try {
      const content = await this.app.vault.read(result.file);
      parsed = parseArtigoMD(content);
    } catch (e) { console.error('Fenice buscar tema:', e); }

    const num = result.meta.numero || result.meta.artigo || result.titulo;

    // Limpar console para não congestionar
    console.clear();
    console.log(`✅ Aberto: ${result.titulo}`);

    const acessorios3 = result.meta?.acessorios || null;
    new InfoModal(this.app, result.file, config, num, parsed, [], acessorios3,
      () => {
        console.clear();
        this.iniciarBusca();
      },
      (lei) => this.buscarPorLei(lei)).open();
  }

  avisarNaoEncontrado(config, num) {
    if (config.avisoNucleoAusente) {
      new Notice(
        `⚠ Art. ${num} do CPP não encontrado.\n` +
        `O núcleo do DL 3.689/1941 (CPP) ainda não foi atomizado neste vault.\n` +
        `Disponíveis em "${config.codigo}": Lei de Execução Penal (L7210), ` +
        `Juizados Especiais (L9099), Pacote Anticrime (L13964), ` +
        `Abuso de Autoridade (L13869), Org. Criminosa (L12850), Sequestro-relâmpago (L7960).`,
        9000
      );
      return;
    }
    new Notice(`⚠ Art. ${num} não encontrado em ${config.codigo}.`, 4000);
  }

  onunload() {}
}

module.exports = FeniceBuscarArtigo;

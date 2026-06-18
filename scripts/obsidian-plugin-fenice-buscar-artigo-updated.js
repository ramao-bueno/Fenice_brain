'use strict';

const { Plugin, SuggestModal, Modal, Notice } = require('obsidian');

const CODIGOS = [
  // ━━━ DIREITO CONSTITUCIONAL ━━━
  { label: 'CF/88 — Constituição Federal',  tag: 'cf88',          pasta: '00_ESTRUTURA_CONSTITUCIONAL/CONSTITUIÇÃO_FEDERAL/Artigos', codigo: 'CF/88' },

  // ━━━ DIREITO CIVIL ━━━
  { label: 'Código Civil (CC)',              tag: 'cc',            pastas: ['02_DIREITO_PRIVADO/DIREITO_CIVIL/Livro-I_Parte-Geral/Codigo Civil/Artigos', '02_DIREITO_PRIVADO/DIREITO_CIVIL/Artigos/L10406'], codigo: 'CC'   },
  { label: 'LINDB — Lei de Introdução',      tag: 'lindb',         pasta: '02_DIREITO_PRIVADO/DIREITO_CIVIL/Artigos/LINDB',  codigo: 'LINDB'},
  { label: 'D9830 — Decreto LINDB (2019)',   tag: 'd9830',         pasta: '02_DIREITO_PRIVADO/DIREITO_CIVIL/Artigos/D9830',  codigo: 'D9830'},

  // ━━━ DIREITO PENAL ━━━
  { label: 'Código Penal (CP)',              tag: 'direito-penal', pastas: ['04_DIREITO_PENAL/CÓDIGO_PENAL/Crimes', '04_DIREITO_PENAL/CÓDIGO_PENAL/Artigos/DEL2848'], codigo: 'CP'   },

  // ━━━ DIREITO PROCESSUAL ━━━
  { label: 'CPC — Código Processo Civil',    tag: 'cpc',           pasta: '03_PROCESSO_CIVIL/CÓDIGO_PROCESSO_CIVIL/Artigos/L13105',        codigo: 'CPC'  },
  { label: 'CPP — Código Processo Penal',    tag: 'cpp',           pasta: '04_DIREITO_PENAL/CÓDIGO_PROCESSO_PENAL', codigo: 'CPP', avisoNucleoAusente: true },

  // ━━━ DIREITO CONSUMERISTA & COMERCIAL ━━━
  { label: 'Código do Consumidor (CDC)',     tag: 'cdc',           pasta: '02_DIREITO_PRIVADO/CÓDIGO_CONSUMIDOR',            codigo: 'CDC'  },

  // ━━━ DIREITO ADMINISTRATIVO ━━━
  { label: 'Lei Improbidade (L8429)',        tag: 'improbidade',   pasta: '07_DIREITO_ADMINISTRATIVO/DIREITO_ADMINISTRATIVO/Artigos/L8429',       codigo: 'L8429'},
  { label: 'Lei Anticorrupção (L12846)',     tag: 'anticorrupção', pasta: '07_DIREITO_ADMINISTRATIVO/DIREITO_ADMINISTRATIVO/Artigos/L12846',       codigo: 'L12846'},
  { label: 'Lei Acesso Info (L12527)',       tag: 'lai',           pasta: '07_DIREITO_ADMINISTRATIVO/DIREITO_ADMINISTRATIVO/Artigos/L12527',       codigo: 'L12527'},

  // ━━━ DIREITO PREVIDENCIÁRIO ━━━
  { label: 'Lei Custeio (L8212)',            tag: 'previdenciario', pasta: '08_DIREITOS_ESPECIALIZADOS/DIREITO_PREVIDENCIARIO/Artigos/L8212',      codigo: 'L8212'},
  { label: 'Lei Benefício (L8213)',          tag: 'previdenciario', pasta: '08_DIREITOS_ESPECIALIZADOS/DIREITO_PREVIDENCIARIO/Artigos/L8213',      codigo: 'L8213'},

  // ━━━ DIREITO DIGITAL & TECNOLOGIA ━━━
  { label: 'Marco Civil da Internet',        tag: 'marco-civil',   pasta: '08_DIREITOS_ESPECIALIZADOS/DIREITO_DIGITAL/Artigos/L12965',              codigo: 'MCI'  },
  { label: 'LGPD — Lei Proteção Dados',      tag: 'lgpd',          pasta: '08_DIREITOS_ESPECIALIZADOS/DIREITO_DIGITAL/Artigos/L13709',              codigo: 'LGPD' },

  // ━━━ DIREITO INTERNACIONAL & TRATADOS ━━━
  { label: 'CADH — Convenção Am. Dir. Hum.', tag: 'internacional', pasta: '08_DIREITOS_ESPECIALIZADOS/DIREITO_INTERNACIONAL/Tratados/Convencao-Americana-Direitos-Humanos',       codigo: 'CADH' },
  { label: 'CVDT — Conv. Viena Tratados',    tag: 'internacional', pasta: '08_DIREITOS_ESPECIALIZADOS/DIREITO_INTERNACIONAL/Tratados/Convencao-Viena-Direito-dos-Tratados',       codigo: 'CVDT' },

  // ━━━ JURISPRUDÊNCIA STF ━━━
  { label: 'SV — Súmulas Vinculantes STF',  tag: 'sumula-vinculante', pasta: '03_PROCESSO_CIVIL/STF_SUMULAS/Vinculantes', codigo: 'SV',     buscaPorSumula: true },
  { label: 'S-STF — Súmulas Comuns STF',    tag: 'sumula',            pasta: '03_PROCESSO_CIVIL/STF_SUMULAS/Comuns',    codigo: 'S-STF', buscaPorSumula: true },

  // ━━━ ESPECIAL: ENUNCIADOS ━━━
  { label: '📋 Enunciados CJF',             tag: 'enunciados-cjf', pasta: '00_ESTRUTURA_CONSTITUCIONAL/ENUNCIADOS_CJF',            codigo: 'ENUM', isEnunciados: true },
  { label: '⚡ ATOMIZAR — Skill de IA',     tag: 'atomizar',       pasta: '', codigo: 'ATOM', isAtomizar: true },
];

// ─── Parseia o conteúdo do arquivo .md ───────────────────────
function parseArtigoMD(content) {
  const result = {
    textoBase: '',
    paragrafos: [],  // [{label, texto}]
    incisos:    [],  // [{label, texto}]
    alineas:    [],  // [{label, texto}]
    correlatos: [],  // strings (wikilinks + texto)
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

  if (!redacao || redacao.startsWith('[Reda')) return result;

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

  // ── Correlatos: wikilinks da seção ARTIGOS CORRELATOS ──
  const mCorr = content.match(/##[^\n]*CORRELAT[^\n]*\n([\s\S]*?)(?=\n##|$)/i);
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

// ─── Modal 2: Número do Artigo ───────────────────────────────
class ArtigoModal extends Modal {
  constructor(app, config, onBuscar) {
    super(app);
    this.config = config;
    this.onBuscar = onBuscar;
  }
  onOpen() {
    const { contentEl } = this;
    contentEl.empty();
    contentEl.createEl('h3', { text: `Número do Artigo — ${this.config.codigo}` });

    const input = contentEl.createEl('input', {
      type: 'text', placeholder: 'Ex: 48  |  121  |  1.228',
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
  constructor(app, found, config, num, parsed, enunciados, onNovaBusca) {
    super(app);
    this.found      = found;
    this.config     = config;
    this.num        = num;
    this.parsed     = parsed;
    this.enunciados = enunciados || [];
    this.onNovaBusca = onNovaBusca;
    this.modalEl.style.maxWidth = '600px';
    this.modalEl.style.width   = '92vw';
  }

  onOpen() {
    const { contentEl } = this;
    contentEl.empty();

    const { textoBase, paragrafos, incisos, alineas, correlatos } = this.parsed;

    // ── Cabeçalho ──
    const h = contentEl.createEl('div');
    Object.assign(h.style, {
      display: 'flex', justifyContent: 'space-between',
      alignItems: 'center', marginBottom: '10px',
    });
    h.createEl('strong', { text: `Art. ${this.num} — ${this.config.codigo}` })
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
      // Caput resumido (primeiras 120 chars)
      if (textoBase) {
        const caput = card.createEl('p');
        caput.style.marginTop = '0';
        caput.createEl('strong', { text: `Art. ${this.num}. ` });
        const resumo = textoBase.length > 120 ? textoBase.slice(0, 120) + '…' : textoBase;
        caput.appendText(resumo);
      }

      // Incisos — só os labels
      if (incisos.length) {
        const row = card.createEl('p');
        row.style.marginBottom = '3px';
        row.style.marginLeft = '12px';
        row.style.color = 'var(--text-muted)';
        row.textContent = `Incisos: ${incisos.map(i => i.label).join(' · ')}`;
      }

      // Alíneas — só os labels
      if (alineas.length) {
        const row = card.createEl('p');
        row.style.marginBottom = '3px';
        row.style.marginLeft = '24px';
        row.style.color = 'var(--text-muted)';
        row.textContent = `Alíneas: ${alineas.map(a => a.label).join(' ')}`;
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
      .read('Fenice bRain/00_ESTRUTURA_CONSTITUCIONAL/ENUNCIADOS_CJF/enunciados_index.json')
      .then(txt => {
        this.enunciadosIndex = JSON.parse(txt);
        console.log('Fenice: enunciados CJF carregados —',
          Object.keys(this.enunciadosIndex).length, 'artigos');
      })
      .catch(() => console.log('Fenice: enunciados_index.json nao encontrado'));

    console.log('Fenice Buscar Artigo v6 (CORRIGIDO) — Ctrl+Shift+B | Ctrl+Shift+I');
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
        this.app.workspace.openLinkText('00_ESTRUTURA_CONSTITUCIONAL/ENUNCIADOS_CJF/INDEX-ENUNCIADOS', '', false);
        return;
      }

      // Casos normais: pede número do artigo
      new ArtigoModal(this.app, config, (num) => {
        this.buscarEAbrir(config, num);
      }).open();
    }).open();
  }

  // Painel para escolher qual área atomizar
  abrirAtomizar() {
    const areas = [
      { label: '📚 Direito Constitucional', pasta: '00_ESTRUTURA_CONSTITUCIONAL/CONSTITUIÇÃO_FEDERAL' },
      { label: '📖 Código Civil', pasta: '02_DIREITO_PRIVADO/DIREITO_CIVIL' },
      { label: '⚖️  Código Penal', pasta: '04_DIREITO_PENAL/CÓDIGO_PENAL' },
      { label: '📋 Processo Civil', pasta: '03_PROCESSO_CIVIL/CÓDIGO_PROCESSO_CIVIL' },
      { label: '🔨 Processo Penal', pasta: '04_DIREITO_PENAL/CÓDIGO_PROCESSO_PENAL' },
      { label: '🛡️  Direito Administrativo', pasta: '07_DIREITO_ADMINISTRATIVO/DIREITO_ADMINISTRATIVO' },
      { label: '💼 Direito Previdenciário', pasta: '08_DIREITOS_ESPECIALIZADOS/DIREITO_PREVIDENCIARIO' },
      { label: '🌐 Direito Digital', pasta: '08_DIREITOS_ESPECIALIZADOS/DIREITO_DIGITAL' },
      { label: '🌍 Direito Internacional', pasta: '08_DIREITOS_ESPECIALIZADOS/DIREITO_INTERNACIONAL' },
      { label: '🏪 Código Consumidor', pasta: '02_DIREITO_PRIVADO/CÓDIGO_CONSUMIDOR' },
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
    if (!meta?.artigo) {
      new Notice('Arquivo atual não é um artigo jurídico (sem frontmatter "artigo").', 3000);
      return;
    }

    // Detecta o código pelo tag do arquivo
    const tags = Array.isArray(meta.tags) ? meta.tags : [];
    const config = CODIGOS.find(c => tags.includes(c.tag))
                || { codigo: 'Lei', tag: '', pasta: '' };

    const num = String(meta.artigo);
    let parsed = { textoBase: '', paragrafos: [], incisos: [], alineas: [], correlatos: [] };
    try {
      const content = await this.app.vault.read(activeFile);
      parsed = parseArtigoMD(content);
    } catch (e) { console.error('Fenice info:', e); }

    const chaveIdx = `${config.tag}:${num}`;
    const enunciados = (this.enunciadosIndex || {})[chaveIdx] || [];

    new InfoModal(this.app, activeFile, config, num, parsed, enunciados,
      () => this.iniciarBusca()).open();
  }

  async buscarEAbrir(config, numArtigo) {
    const num = numArtigo.trim();
    const allFiles = this.app.vault.getFiles();

    const campoChave = config.buscaPorSumula ? 'sumula' : 'artigo';
    const numPadded  = config.buscaPorSumula ? num.padStart(2, '0') : num;
    const bate = (meta) => meta && (String(meta[campoChave]) === num || String(meta[campoChave]) === numPadded);

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

    await this.app.workspace.openLinkText(found.basename, '', false);

    let parsed = { textoBase: '', paragrafos: [], incisos: [], alineas: [], correlatos: [] };
    try {
      const content = await this.app.vault.read(found);
      parsed = parseArtigoMD(content);
    } catch (e) { console.error('Fenice buscar:', e); }

    const chaveIdx = `${config.tag}:${num}`;
    const enunciados = (this.enunciadosIndex || {})[chaveIdx] || [];

    new InfoModal(this.app, found, config, num, parsed, enunciados,
      () => this.iniciarBusca()).open();
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

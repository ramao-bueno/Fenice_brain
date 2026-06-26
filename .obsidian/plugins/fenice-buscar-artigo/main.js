'use strict';

const { Plugin, SuggestModal, Modal, Notice } = require('obsidian');

const CODIGOS = [
  // ━━━ DIREITO CONSTITUCIONAL ━━━
  { label: 'CF/88 — Constituição Federal',  tag: 'cf88',          pasta: '00_APEX/CONSTITUIÇÃO_FEDERAL/Artigos', codigo: 'CF/88' },

  // ━━━ DIREITO CIVIL ━━━
  { label: 'Código Civil (CC)',              tag: 'cc',            pastas: [
      '01_PRIVADO/Codigos/CC/Artigos/L10406',
      '01_PRIVADO/Codigos/CC/Artigos/LIVRO-I',
      '01_PRIVADO/Codigos/CC/Artigos/LIVRO-II',
      '01_PRIVADO/Codigos/CC/Artigos/LIVRO-III',
      '01_PRIVADO/Codigos/CC/Artigos/LIVRO-IV',
      '01_PRIVADO/Codigos/CC/Artigos/LIVRO-V',
    ], codigo: 'CC' },
  { label: 'LINDB — Lei de Introdução',      tag: 'lindb',         pasta: '01_PRIVADO/Codigos/CC/Artigos/LINDB', codigo: 'LINDB'},
  { label: 'D9830 — Decreto LINDB (2019)',   tag: 'd9830',         pasta: '01_PRIVADO/Codigos/CC/Artigos/D9830',  codigo: 'D9830'},

  // ━━━ DIREITO PENAL ━━━
  { label: 'Código Penal (CP)',              tag: 'direito-penal', pastas: [
      '02_PENAL/Codigos/CP/DEL2848',
      '02_PENAL/Codigos/CP/Crimes',
    ], codigo: 'CP' },

  // ━━━ DIREITO PROCESSUAL ━━━
  { label: 'CPC — Código Processo Civil',    tag: 'cpc',           pastas: [
      '01_PRIVADO/Codigos/CPC/CÓDIGO_PROCESSO_CIVIL/Artigos/LIVRO-I',
      '01_PRIVADO/Codigos/CPC/CÓDIGO_PROCESSO_CIVIL/Artigos/LIVRO-II',
      '01_PRIVADO/Codigos/CPC/CÓDIGO_PROCESSO_CIVIL/Artigos/LIVRO-III',
      '01_PRIVADO/Codigos/CPC/CÓDIGO_PROCESSO_CIVIL/Artigos/LIVRO-IV',
      '01_PRIVADO/Codigos/CPC/CÓDIGO_PROCESSO_CIVIL/Artigos/LIVRO-V',
      '01_PRIVADO/Codigos/CPC/CÓDIGO_PROCESSO_CIVIL/Artigos/L13105',
    ], codigo: 'CPC' },
  { label: 'CPP — Código Processo Penal',    tag: 'cpp',           pasta: '02_PENAL/Codigos/CPP/Artigos', codigo: 'CPP' },

  // ━━━ DIREITO CONSUMERISTA & COMERCIAL ━━━
  { label: 'Código do Consumidor (CDC)',     tag: 'cdc',           pasta: '05_ESPECIAL/Codigos/DIREITO_DIGITAL', codigo: 'CDC' },

  // ━━━ DIREITO ADMINISTRATIVO ━━━
  { label: 'Lei Improbidade (L8429)',        tag: 'improbidade',   pasta: '03_PUBLICO/Codigos/Admin/DIREITO_ADMINISTRATIVO/Artigos/L8429',  codigo: 'L8429'},
  { label: 'Lei Anticorrupção (L12846)',     tag: 'anticorrupção', pasta: '03_PUBLICO/Codigos/Admin/DIREITO_ADMINISTRATIVO/Artigos/L12846', codigo: 'L12846'},
  { label: 'Lei Acesso Info (L12527)',       tag: 'lai',           pasta: '03_PUBLICO/Codigos/Admin/DIREITO_ADMINISTRATIVO/Artigos/L12527', codigo: 'L12527'},

  // ━━━ DIREITO PREVIDENCIÁRIO ━━━
  { label: 'Lei Custeio (L8212)',            tag: 'previdenciario', pasta: '05_ESPECIAL/Codigos/DIREITO_PREVIDENCIARIO/Artigos/L8212', codigo: 'L8212'},
  { label: 'Lei Benefício (L8213)',          tag: 'previdenciario', pasta: '05_ESPECIAL/Codigos/DIREITO_PREVIDENCIARIO/Artigos/L8213', codigo: 'L8213'},

  // ━━━ DIREITO DIGITAL & TECNOLOGIA ━━━
  { label: 'Marco Civil da Internet',        tag: 'marco-civil',   pasta: '05_ESPECIAL/Codigos/DIREITO_DIGITAL/Artigos/L12965', codigo: 'MCI'  },
  { label: 'LGPD — Lei Proteção Dados',      tag: 'lgpd',          pasta: '05_ESPECIAL/Codigos/DIREITO_DIGITAL/Artigos/L13709', codigo: 'LGPD' },

  // ━━━ DIREITO INTERNACIONAL & TRATADOS ━━━
  { label: 'CADH — Convenção Am. Dir. Hum.', tag: 'internacional', pasta: '05_ESPECIAL/Codigos/DIREITO_INTERNACIONAL/Tratados/Convencao-Americana-Direitos-Humanos', codigo: 'CADH', isReferencia: true },
  { label: 'CVDT — Conv. Viena Tratados',    tag: 'internacional', pasta: '05_ESPECIAL/Codigos/DIREITO_INTERNACIONAL/Tratados/Convencao-Viena-Direito-dos-Tratados', codigo: 'CVDT', isReferencia: true },

  // ━━━ JURISPRUDÊNCIA STF / STJ ━━━
  { label: 'SV — Súmulas Vinculantes STF',  tag: 'sumula-vinculante', pasta: '00_APEX/SUMULAS STF/Sumulas', codigo: 'SV',    buscaPorSumula: true },
  { label: 'S-STF — Súmulas Comuns STF',    tag: 'sumula-stf',        pasta: '00_APEX/SUMULAS STF/Sumulas', codigo: 'S-STF', buscaPorSumula: true },
  { label: 'S-STJ — Súmulas STJ',           tag: 'sumula-stj',        pasta: '00_APEX/SUMULAS STJ/Sumulas', codigo: 'S-STJ', buscaPorSumula: true },

  // ━━━ JURISCONSULTOS ━��━
  { label: '⚖️ Jurisconsultos — Privado/Civil', tag: 'jurisconsultor', pastas: ['06_JURISCONSULTOS/Civil','06_JURISCONSULTOS/PRIVADO','06_JURISCONSULTOS/Processual'], codigo: 'JURISC-CIV', isReferencia: true },
  { label: '⚖️ Jurisconsultos — Constitucional', tag: 'jurisconsultor', pasta: '06_JURISCONSULTOS/Constitucional', codigo: 'JURISC-CONST', isReferencia: true },
  { label: '⚖️ Jurisconsultos — Penal',      tag: 'jurisconsultor', pasta: '06_JURISCONSULTOS/PENAL', codigo: 'JURISC-PEN', isReferencia: true },
  { label: '⚖️ Jurisconsultos — Público',    tag: 'jurisconsultor', pastas: ['06_JURISCONSULTOS/PUBLICO','06_JURISCONSULTOS/Tributario','06_JURISCONSULTOS/Trabalhista','06_JURISCONSULTOS/TRABALHO'], codigo: 'JURISC-PUB', isReferencia: true },

  // ━━━ FILÓSOFOS & MAESTROS ━━━
  { label: '🧠 Filósofos do Direito',        tag: 'filosofia', pastas: ['07_FILOSOFIA/Antigos','07_FILOSOFIA/Iluministas','07_FILOSOFIA/Modernos','07_FILOSOFIA/Contemporaneos','07_FILOSOFIA/Penalistas'], codigo: 'FILOS', isReferencia: true },
  { label: '🌟 MAESTROS — Guias Fenice',     tag: 'maestros',  pasta: '09_FENICE_BRAIN/MAESTROS', codigo: 'MAESTROS', isReferencia: true },

  // ━━━ PROFISSÕES & ENTIDADES ━━━
  { label: 'OAB — Ordem dos Advogados',     tag: 'oab',           pasta: '_SISTEMA/OAB', codigo: 'OAB', isReferencia: true },

  // ━━━ ESPECIAL: ENUNCIADOS ━━━
  { label: '📋 Enunciados CJF',             tag: 'enunciados-cjf', pasta: '00_APEX/ENUNCIADOS_CJF', codigo: 'ENUM', isEnunciados: true },
  { label: '⚡ ATOMIZAR — Skill de IA',     tag: 'atomizar',       pasta: '', codigo: 'ATOM', isAtomizar: true },
];

const DOMINIOS = [
  { label: '🏛️  00 · Constituição Federal',  key: 'apex',      codigos: ['CF/88'] },
  { label: '📘  01 · Direito Privado',        key: 'privado',   codigos: ['CC','LINDB','D9830','CPC','CDC'] },
  { label: '🔒  02 · Direito Penal',          key: 'penal',     codigos: ['CP','CPP'] },
  { label: '🏢  03 · Direito Público',        key: 'publico',   codigos: ['L8429','L12846','L12527'] },
  { label: '💼  04 · Direito do Trabalho',    key: 'trabalho',  codigos: [] },
  { label: '🛡️   05 · Legislação Especial',   key: 'especial',  codigos: ['L8212','L8213','MCI','LGPD','CADH','CVDT'] },
  { label: '📋  Súmulas & Enunciados',        key: 'juris',     codigos: ['SV','S-STF','S-STJ','OAB','ENUM'] },
  { label: '⚖️   Jurisconsultos & Filósofos', key: 'maestros',  codigos: ['JURISC-CIV','JURISC-CONST','JURISC-PEN','JURISC-PUB','FILOS','MAESTROS'] },
  { label: '⚡  ATOMIZAR — Skill de IA',      key: 'atom',      codigos: ['ATOM'] },
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

  // ── Fallback: formato dosimetria (Crimes/) — callouts [!info] + tabela Dados Essenciais ──
  if (!result.textoBase) {
    // Extrai texto do primeiro callout [!info] ou [!tip]
    const mCallout = content.match(/>\s*\[!(?:info|tip|warning)[^\]]*\][^\n]*\n((?:>[^\n]*\n?)+)/i);
    if (mCallout) {
      result.textoBase = mCallout[1]
        .split('\n')
        .map(l => l.replace(/^>\s?/, '').replace(/\*{1,2}/g, '').trim())
        .filter(Boolean).join(' ');
    }
    // Extrai tabela ## Dados Essenciais como analiseTecnica
    if (!result.analiseTecnica) {
      const mTab = content.match(/## ([^\n]+)\n((?:\|[^\n]+\n){2,})/);
      if (mTab) {
        const linhas = mTab[2].split('\n')
          .filter(l => l.includes('|') && !/^\s*\|[\s\-:]+\|/.test(l) && l.trim());
        if (linhas.length) result.analiseTecnica = { [mTab[1].trim()]: linhas };
      }
    }
    // Extrai wikilinks do ## Links Relacionados como correlatos
    if (!result.correlatos.length) {
      const mLinks = content.match(/## Links[^\n]*\n([\s\S]*?)(?=\n##|$)/i);
      if (mLinks) {
        for (const m of [...mLinks[1].matchAll(/\[\[([^\]|]+)(?:\|[^\]]+)?\]\]/g)]) {
          result.correlatos.push(m[1].trim());
        }
      }
    }
  }

  // ── §§ inline tipo-labels: "Furto qualificado § 4°" → pg.tipo = "Furto qualificado" ──
  if (result.paragrafos.length && redacao) {
    const tipoRE = /([A-ZÁÉÍÓÚÀÂÊÔÃÕÇÜ][a-záéíóúàâêôãõçü\s]{3,50}?)\s+§\s*(\d+)/g;
    const tipoMap = {};
    for (const m of [...redacao.matchAll(tipoRE)]) {
      const label = m[1].trim().replace(/\s+/g, ' ');
      const words = label.split(' ');
      if (words.length >= 2 && words.length <= 6 && /^[A-ZÁÉÍÓÚÀÂÊÔÃÕÇÜ]/.test(label))
        tipoMap[m[2]] = label;
    }
    for (const pg of result.paragrafos) {
      const num = pg.label.match(/\d+/)?.[0];
      if (num && tipoMap[num]) pg.tipo = tipoMap[num];
    }
  }

  // ── Jurisprudência do corpo: seção ## JURISPRUDENCIA ou ## ⚖️ JURISPRUDÊNCIA ──
  const mJurisCorpo = content.match(/##[^\n]*JURISPRUD[^\n]*\n([\s\S]*?)(?=\n##(?!#)|$)/i);
  if (mJurisCorpo) {
    const bloco = mJurisCorpo[1];
    const jurisCorpo = [];
    // Formato 1: **TRIBUNAL — label**\n> texto (blockquote)
    const bolqRE = /\*\*([^*\n]+)\*\*[^\n]*\n((?:>[^\n]*\n?)+)/g;
    for (const m of [...bloco.matchAll(bolqRE)]) {
      const tribunal = m[1].trim();
      const texto = m[2].split('\n').map(l => l.replace(/^>\s?/, '').trim()).filter(Boolean).join(' ');
      if (texto && !texto.startsWith('[')) jurisCorpo.push({ tribunal, resumo: texto });
    }
    // Formato 2: - TRIBUNAL — texto (lista simples, padrão CP/pipeline)
    if (!jurisCorpo.length) {
      const listaRE = /^[-•]\s*([A-ZÁ-Ú]{2,5}[^\n—–-]{0,20}?)\s*[—–-]\s*(.+)$/gm;
      for (const m of [...bloco.matchAll(listaRE)]) {
        const tribunal = m[1].trim();
        const texto    = m[2].trim();
        if (texto && !texto.startsWith('[')) jurisCorpo.push({ tribunal, resumo: texto });
      }
    }
    // Extrai referências de súmulas mencionadas: "Súmula 511", "STJ — Súmula 442"
    const sumulaRE = /S[úu]mula\s+(\d+)/gi;
    const sumulasJuris = [];
    for (const m of [...bloco.matchAll(sumulaRE)]) {
      if (!sumulasJuris.includes(m[1])) sumulasJuris.push(m[1]);
    }
    if (sumulasJuris.length) result.sumulasVide = sumulasJuris;
    if (jurisCorpo.length) result.jurisCorpo = jurisCorpo;
  }

  // ── Prática Forense: ## OBSERVACOES PRATICAS ──
  const mPratica = content.match(/##[^\n]*OBSERVA[^\n]*\n([\s\S]*?)(?=\n##(?!#)|$)/i);
  if (mPratica) {
    const linhas = mPratica[1].split('\n').filter(l => {
      const t = l.trim();
      return t && !/^-{3,}$/.test(t) && !t.startsWith('[') && !t.startsWith('##');
    });
    if (linhas.length) result.praticaForense = linhas;
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
        // remove separadores de tabela, <hr> e linhas de placeholder tipo "[texto...]"
        return t && !/^\|[\s\-:]+\|/.test(t) && !/^-{3,}$/.test(t) && !t.startsWith('[');
      });
      if (linhas.length) secoes[titulo] = linhas;
    }
    if (Object.keys(secoes).length) result.analiseTecnica = secoes;
  }

  // ── Correlatos: wikilinks da seção ARTIGOS CORRELATOS (com subsections) ──
  const mCorr = content.match(/##[^\n]*CORRELAT[^\n]*\n([\s\S]*?)(?=\n##(?!#)|$)/i);
  if (mCorr) {
    const bloco = mCorr[1];
    // Flat fallback — sempre popula result.correlatos
    const linksFlat = [...bloco.matchAll(/\[\[([^\]|]+)(?:\|[^\]]+)?\]\]([^\n]*)/g)];
    for (const l of linksFlat) {
      const nome = l[1].trim();
      const extra = l[2].replace(/^[\s\-—]+/, '').trim();
      if (nome && !nome.includes('INDEX'))
        result.correlatos.push(extra ? `${nome} — ${extra}` : nome);
    }
    // Subsections estruturadas para o campo "Vide artigos..."
    const subsecs = [];
    const subRE = /###\s*(.+?)\n([\s\S]*?)(?=\n###\s|$)/gi;
    for (const ms of [...bloco.matchAll(subRE)]) {
      const titulo = ms[1].trim();
      const links  = [...ms[2].matchAll(/\[\[([^\]|]+)(?:\|[^\]]+)?\]\]([^\n]*)/g)]
        .map(l => {
          const nome  = l[1].trim();
          const extra = l[2].replace(/^[\s\-—]+/, '').trim();
          return nome && !nome.includes('INDEX') ? (extra ? `${nome} — ${extra}` : nome) : null;
        }).filter(Boolean);
      if (links.length) subsecs.push({ titulo, links });
    }
    if (subsecs.length) result.correlatosSubsecs = subsecs;
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

// ─── Modal 0: Selecionar Domínio ─────────────────────────────
class DomainModal extends SuggestModal {
  constructor(app, onEscolha) {
    super(app);
    this.onEscolha = onEscolha;
    this.setPlaceholder('Selecione o ramo do Direito...');
  }
  getSuggestions(q) {
    return DOMINIOS.filter(d => d.label.toLowerCase().includes(q.toLowerCase()));
  }
  renderSuggestion(item, el) {
    const div = el.createEl('div');
    div.createEl('strong', { text: item.label });
  }
  onChooseSuggestion(item) { this.onEscolha(item); }
}

// ─── Modal J: Jurisconsultos & Filósofos (Ctrl+Shift+J) ─────
const MAESTROS_AREAS = [
  { label: '⚖️  Privado / Civil',       pastas: ['06_JURISCONSULTOS/Civil','06_JURISCONSULTOS/PRIVADO','06_JURISCONSULTOS/Processual'] },
  { label: '🔒  Penal',                 pastas: ['06_JURISCONSULTOS/PENAL'] },
  { label: '🏢  Público / Administrativo', pastas: ['06_JURISCONSULTOS/PUBLICO','06_JURISCONSULTOS/Tributario'] },
  { label: '💼  Trabalhista',           pastas: ['06_JURISCONSULTOS/Trabalhista','06_JURISCONSULTOS/TRABALHO'] },
  { label: '🏛️   Constitucional',        pastas: ['06_JURISCONSULTOS/Constitucional'] },
  { label: '📐  Teoria Geral / Método', pastas: ['06_JURISCONSULTOS/Teoria Geral','06_JURISCONSULTOS/METODOLOGIA'] },
  { label: '🧠  Filósofos — Antigos',   pastas: ['07_FILOSOFIA/Antigos'] },
  { label: '💡  Filósofos — Iluministas', pastas: ['07_FILOSOFIA/Iluministas'] },
  { label: '📖  Filósofos — Modernos',  pastas: ['07_FILOSOFIA/Modernos'] },
  { label: '🌐  Filósofos — Contemporâneos', pastas: ['07_FILOSOFIA/Contemporaneos'] },
  { label: '⚔️   Penalistas Clássicos', pastas: ['07_FILOSOFIA/Penalistas'] },
  { label: '🌟  MAESTROS — Guias Fenice', pastas: ['09_FENICE_BRAIN/MAESTROS'] },
];

class JurisconsultoAreaModal extends SuggestModal {
  constructor(app, plugin) {
    super(app);
    this.plugin = plugin;
    this.setPlaceholder('Selecione a área ou escola filosófica...');
  }
  getSuggestions(q) {
    return MAESTROS_AREAS.filter(a => a.label.toLowerCase().includes(q.toLowerCase()));
  }
  renderSuggestion(item, el) { el.createEl('div', { text: item.label }); }
  onChooseSuggestion(area) {
    new JurisconsultoSelectModal(this.app, this.plugin, area).open();
  }
}

class JurisconsultoSelectModal extends SuggestModal {
  constructor(app, plugin, area) {
    super(app);
    this.plugin = plugin;
    this.area   = area;
    this.setPlaceholder(`Selecione em ${area.label.trim()}...`);
    // Carrega de forma síncrona via getFiles() (já indexado pelo Obsidian)
    const allFiles = app.vault.getFiles(); // TFile[] — sem pastas
    const seen = new Set();
    this.items = [];
    for (const pasta of area.pastas) {
      const pastaNorm = pasta.replace(/\/$/, '');
      for (const f of allFiles) {
        if (f.path.startsWith(pastaNorm + '/') || f.path.startsWith(pastaNorm)) {
          if (!seen.has(f.path)) {
            seen.add(f.path);
            this.items.push({ nome: f.basename, file: f });
          }
        }
      }
    }
    this.items.sort((a, b) => a.nome.localeCompare(b.nome, 'pt-BR'));
    if (!this.items.length)
      this.setPlaceholder(`⚠️ Nenhum arquivo em ${area.label.trim()} — adicione notas ao vault`);
  }
  getSuggestions(q) {
    return this.items.filter(i => i.nome.toLowerCase().includes(q.toLowerCase()));
  }
  renderSuggestion(item, el) {
    el.createEl('div', { text: item.nome });
  }
  onChooseSuggestion(item) {
    this.app.workspace.getLeaf(false).openFile(item.file);
  }
}

// ─── Modal 1: Selecionar Código ──────────────────────────────
class CodigoModal extends SuggestModal {
  constructor(app, onEscolha, codigosKeys) {
    super(app);
    this.onEscolha  = onEscolha;
    this.lista      = codigosKeys
      ? CODIGOS.filter(c => codigosKeys.includes(c.codigo))
      : CODIGOS;
    this.setPlaceholder('Selecione o Código Jurídico...');
  }
  getSuggestions(q) {
    return this.lista.filter(c => c.label.toLowerCase().includes(q.toLowerCase()));
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
    this.placeholderText = placeholder || 'Ex: 48  |  121  |  121-A  |  1.228';
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
  constructor(app, found, config, num, parsed, enunciados, acessorios, jurisIdx, onNovaBusca, onBuscarLei, onBuscarArt) {
    super(app);
    this.found       = found;
    this.config      = config;
    this.num         = num;
    this.parsed      = parsed;
    this.enunciados  = enunciados || [];
    this.acessorios  = acessorios || null;
    this.jurisIdx    = jurisIdx   || [];
    this.emendas     = parsed.emendas || [];
    this.onNovaBusca = onNovaBusca;
    this.onBuscarLei = onBuscarLei;
    this.onBuscarArt = onBuscarArt || null;
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

      // Parágrafos — com tipo-label inline (ex: "Furto qualificado • § 4°.")
      if (paragrafos.length) {
        card.createEl('hr').style.margin = '6px 0';
        for (const pg of paragrafos) {
          const p = card.createEl('p');
          p.style.marginBottom = '4px';
          if (pg.tipo) {
            const tipoEl = p.createEl('em', { text: pg.tipo + '  •  ' });
            Object.assign(tipoEl.style, { color: 'var(--text-accent)', fontSize: '11px' });
          }
          p.createEl('strong', { text: `${pg.label}. ` });
          const resumo = pg.texto.length > 200 ? pg.texto.slice(0, 200) + '…' : pg.texto;
          p.appendText(resumo);
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
          const partes = c.split(' — ');
          const nomeRaw = partes[0].trim();
          const mNum = nomeRaw.match(/\d[\d.]*/);
          if (mNum && this.onBuscarArt) {
            // Resolve config pelo código no correlato (ex: "Art. 183 — CF" → config CF)
            const codigoHint = partes.slice(1).find(p => CODIGOS.some(cod => cod.codigo === p.trim()))?.trim();
            const cfgAlvo = codigoHint ? CODIGOS.find(cod => cod.codigo === codigoHint) : null;
            setTimeout(() => this.onBuscarArt(mNum[0], cfgAlvo), 120);
          } else {
            this.app.workspace.openLinkText(nomeRaw, '', false);
          }
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

    // ── Jurisprudência consolidada: índice JSON > frontmatter > corpo ──
    {
      const todasJuris = [];
      if (this.jurisIdx.length) {
        // Fonte primária: jurisprudencia_index.json (mais rico)
        for (const j of this.jurisIdx)
          todasJuris.push({ header: `${j.tribunal}${j.numero ? ' — ' + j.numero : ''}`, texto: j.ementa || '', link: j.link || '' });
      } else if (this.acessorios?.jurisprudencia?.length) {
        // Fonte secundária: acessorios frontmatter
        for (const j of this.acessorios.jurisprudencia)
          todasJuris.push({ header: j.tribunal, texto: j.resumo || '', link: '' });
      } else if (jurisCorpo?.length) {
        // Fonte terciária: corpo do artigo (## JURISPRUDENCIA)
        for (const j of jurisCorpo)
          todasJuris.push({ header: j.tribunal, texto: j.resumo || '', link: '' });
      }
      if (todasJuris.length) {
        const sec = contentEl.createEl('div');
        Object.assign(sec.style, {
          borderTop: '1px solid var(--background-modifier-border)',
          paddingTop: '8px', marginBottom: '10px', fontSize: '13px',
        });
        sec.createEl('strong', { text: '⚖️ Jurisprudência  ' });
        for (const j of todasJuris) {
          const p = sec.createEl('p');
          Object.assign(p.style, {
            marginLeft: '4px', marginBottom: '4px',
            borderLeft: '2px solid var(--interactive-accent)',
            paddingLeft: '8px', lineHeight: '1.4', fontSize: '12px',
          });
          p.createEl('strong', { text: j.header + ': ' });
          p.appendText(j.texto);
          if (j.link) {
            p.appendText(' ');
            const a = p.createEl('a', { text: '[↗]' });
            a.href = j.link;
            a.style.color = 'var(--text-accent)';
            a.target = '_blank';
          }
        }
      }
    }

    // ── Prática Forense (## OBSERVACOES PRATICAS) ──
    if (this.parsed.praticaForense?.length) {
      const sec = contentEl.createEl('div');
      Object.assign(sec.style, {
        borderTop: '1px solid var(--background-modifier-border)',
        paddingTop: '8px', marginBottom: '10px', fontSize: '13px',
      });
      sec.createEl('strong', { text: '🏛️ Prática Forense  ' });
      for (const linha of this.parsed.praticaForense) {
        const t = linha.trim();
        if (!t) continue;
        const p = sec.createEl('p');
        Object.assign(p.style, {
          marginTop: '5px', marginLeft: '4px', fontSize: '12px', lineHeight: '1.5',
          borderLeft: '2px solid var(--interactive-accent)', paddingLeft: '8px',
        });
        // remove markdown bold (**texto**) → exibe simples
        p.appendText(t.replace(/\*\*/g, ''));
      }
    }

    // ── Vide Artigos (subsections de ARTIGOS CORRELATOS) ──
    if (this.parsed.correlatosSubsecs?.length) {
      const sec = contentEl.createEl('div');
      Object.assign(sec.style, {
        borderTop: '1px solid var(--background-modifier-border)',
        paddingTop: '8px', marginBottom: '10px', fontSize: '13px',
      });
      sec.createEl('strong', { text: '🔗 Vide Artigos  ' });
      for (const sub of this.parsed.correlatosSubsecs) {
        const grp = sec.createEl('div');
        grp.style.marginTop = '4px';
        grp.createEl('em', { text: sub.titulo + ':  ' }).style.fontSize = '11px';
        sub.links.forEach((c, i) => {
          if (i) grp.appendText(' · ');
          const a = grp.createEl('span', { text: c.split(' — ')[0] });
          Object.assign(a.style, { color: 'var(--text-accent)', cursor: 'pointer', fontSize: '12px' });
          a.title = c;
          a.addEventListener('click', () => {
            this.close();
            const mNum = c.match(/\d[\d.]*/);
            if (mNum && this.onBuscarArt) setTimeout(() => this.onBuscarArt(mNum[0]), 120);
            else this.app.workspace.openLinkText(c.split(' — ')[0].trim(), '', false);
          });
        });
      }
    }

    // ── Vide Súmulas (extraídas da seção JURISPRUDENCIA) ──
    if (this.parsed.sumulasVide?.length) {
      const sec = contentEl.createEl('div');
      Object.assign(sec.style, {
        borderTop: '1px solid var(--background-modifier-border)',
        paddingTop: '8px', marginBottom: '10px', fontSize: '13px',
      });
      sec.createEl('strong', { text: '📌 Vide Súmulas  ' });
      this.parsed.sumulasVide.forEach((num, i) => {
        if (i) sec.appendText(' · ');
        const a = sec.createEl('span', { text: `Súmula ${num}` });
        Object.assign(a.style, { color: 'var(--text-accent)', cursor: 'pointer' });
        a.addEventListener('click', () => {
          this.close();
          this.app.workspace.openLinkText(`Súmula ${num}`, '', false);
        });
      });
    }

    // ── Acessórios do frontmatter (enunciados + relacionados) ──
    const ac = this.acessorios;
    if (ac) {

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
            if (this.onBuscarArt) {
              setTimeout(() => this.onBuscarArt(String(r.artigo)), 120);
            } else {
              this.app.workspace.openLinkText(`Art. ${r.artigo}`, '', false);
            }
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

// ─── Modal Graph: como visualizar? ──────────────────────────
class GraphModal extends Modal {
  constructor(app, plugin) {
    super(app);
    this.plugin = plugin;
    this.modalEl.style.maxWidth = '480px';
    this.modalEl.style.width   = '90vw';
  }

  onOpen() {
    const { contentEl } = this;
    contentEl.empty();

    const activeFile = this.app.workspace.getActiveFile();

    const h = contentEl.createEl('h3', { text: '📊 Visualização em Grafo' });
    h.style.marginBottom = '4px';

    if (activeFile) {
      const sub = contentEl.createEl('p', { text: activeFile.basename });
      Object.assign(sub.style, { color: 'var(--text-muted)', fontSize: '12px', marginBottom: '16px', marginTop: '0' });
    }

    const opcoes = [
      {
        icon: '📄',
        titulo: 'Artigo atual — links diretos',
        desc: 'Grafo local depth 1: mostra só os artigos diretamente linkados (CP, CC, CF…). Rápido.',
        badge: '⚡ rápido',
        badgeColor: 'var(--color-green)',
        action: () => {
          this.close();
          if (!activeFile) { new Notice('Nenhum artigo aberto.', 2000); return; }
          this.plugin._abrirGrafoLocal(activeFile, 1);
        },
      },
      {
        icon: '🇧🇷',
        titulo: 'Correlações entre ramos (depth 2)',
        desc: 'Grafo local depth 2: artigo atual + links + links dos links. Veja CC, CP e CF conectados.',
        badge: '🔍 correlações',
        badgeColor: 'var(--text-accent)',
        action: () => {
          this.close();
          if (!activeFile) { new Notice('Nenhum artigo aberto.', 2000); return; }
          this.plugin._abrirGrafoLocal(activeFile, 2);
        },
      },
    ];

    for (const opt of opcoes) {
      const btn = contentEl.createEl('div');
      Object.assign(btn.style, {
        display: 'flex', alignItems: 'flex-start', gap: '12px',
        padding: '12px', marginBottom: '8px', cursor: 'pointer',
        borderRadius: '6px', border: '1px solid var(--background-modifier-border)',
        background: 'var(--background-secondary)', transition: 'background 0.1s',
      });
      btn.addEventListener('mouseenter', () => btn.style.background = 'var(--background-modifier-hover)');
      btn.addEventListener('mouseleave', () => btn.style.background = 'var(--background-secondary)');
      btn.addEventListener('click', opt.action);

      const icon = btn.createEl('div', { text: opt.icon });
      Object.assign(icon.style, { fontSize: '22px', lineHeight: '1', paddingTop: '2px' });

      const info = btn.createEl('div');
      info.style.flex = '1';

      const titulo = info.createEl('div', { text: opt.titulo });
      Object.assign(titulo.style, { fontWeight: 'bold', marginBottom: '2px' });

      const desc = info.createEl('div', { text: opt.desc });
      Object.assign(desc.style, { fontSize: '12px', color: 'var(--text-muted)', lineHeight: '1.4' });

      if (opt.badge) {
        const badge = info.createEl('span', { text: opt.badge });
        Object.assign(badge.style, {
          fontSize: '10px', color: opt.badgeColor || 'var(--text-muted)',
          marginTop: '4px', display: 'inline-block', fontWeight: 'bold',
        });
      }
    }
  }

  onClose() { this.contentEl.empty(); }
}

// ─── Plugin Principal ────────────────────────────────────────
class FeniceBuscarArtigo extends Plugin {

  onload() {
    console.log('✅ Fenice Buscar Artigo v27 — §§ tipo-labels, jurisprudência lista, prática forense, vide artigos/súmulas, J-modal sync');

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

    // Ctrl+Shift+G — abre GraphModal com opções de visualização
    this.addCommand({
      id: 'graph-modal',
      name: 'Grafo Jurídico (escolher visualização)',
      hotkeys: [{ modifiers: ['Ctrl', 'Shift'], key: 'G' }],
      callback: () => new GraphModal(this.app, this).open(),
    });

    // Ctrl+Shift+J — Jurisconsultos & Filósofos (dois níveis: área → nome → abre nota)
    this.addCommand({
      id: 'jurisconsulto-modal',
      name: 'Jurisconsultos & Filósofos (área → selecionar)',
      hotkeys: [{ modifiers: ['Ctrl', 'Shift'], key: 'J' }],
      callback: () => new JurisconsultoAreaModal(this.app, this).open(),
    });

    // Listener global — garante que os atalhos funcionam mesmo quando
    // o Graph View está ativo (o canvas do grafo captura eventos de teclado
    // antes do sistema de comandos do Obsidian, bloqueando os addCommand acima).
    this.registerDomEvent(document, 'keydown', (e) => {
      if (!e.ctrlKey || !e.shiftKey) return;
      if (e.key === 'B') { e.preventDefault(); e.stopPropagation(); this.iniciarBusca(); }
      else if (e.key === 'G') { e.preventDefault(); e.stopPropagation(); new GraphModal(this.app, this).open(); }
      else if (e.key === 'I') { e.preventDefault(); e.stopPropagation(); this.mostrarInfoAtual(); }
      else if (e.key === 'J') { e.preventDefault(); e.stopPropagation(); new JurisconsultoAreaModal(this.app, this).open(); }
    });

    // Carrega index de enunciados CJF
    this.enunciadosIndex = {};
    this.app.vault.adapter
      .read('00_APEX/ENUNCIADOS_CJF/enunciados_index.json')
      .then(txt => {
        this.enunciadosIndex = JSON.parse(txt);
        console.log('Fenice: enunciados CJF carregados —',
          Object.keys(this.enunciadosIndex).length, 'artigos');
      })
      .catch(() => console.log('Fenice: enunciados_index.json nao encontrado'));

    // Carrega index de jurisprudência
    this.jurisprudenciaIndex = {};
    this.app.vault.adapter
      .read('scripts/jurisprudencia_index.json')
      .then(txt => {
        this.jurisprudenciaIndex = JSON.parse(txt);
        console.log('Fenice: jurisprudência carregada —',
          Object.keys(this.jurisprudenciaIndex).length, 'artigos');
      })
      .catch(() => console.log('Fenice: jurisprudencia_index.json nao encontrado (normal — ainda nao gerado)'));
  }

  // Garante que os índices JSON estão carregados (evita race condition no onload)
  async garantirIndexes() {
    const ps = [];
    if (!Object.keys(this.jurisprudenciaIndex).length)
      ps.push(this.app.vault.adapter.read('scripts/jurisprudencia_index.json')
        .then(t => { this.jurisprudenciaIndex = JSON.parse(t); })
        .catch(() => {}));
    if (!Object.keys(this.enunciadosIndex).length)
      ps.push(this.app.vault.adapter
        .read('00_APEX/ENUNCIADOS_CJF/enunciados_index.json')
        .then(t => { this.enunciadosIndex = JSON.parse(t); })
        .catch(() => {}));
    if (ps.length) await Promise.all(ps);
  }

  _limparCopilot() {
    const cp = this.app.plugins.plugins['copilot'];
    if (!cp?.chatUIState) return;
    cp.chatUIState.clearMessages();
    const leaf = this.app.workspace.getLeavesOfType('copilot-chat-view')[0];
    if (leaf?.view?.updateView) leaf.view.updateView();
  }

  iniciarBusca() {
    console.clear();
    this._limparCopilot();

    new DomainModal(this.app, (dominio) => {
      // ATOMIZAR — vai direto
      if (dominio.key === 'atom') {
        this.abrirAtomizar();
        return;
      }

      // Abre CodigoModal filtrado pelo domínio escolhido
      new CodigoModal(this.app, (config) => {
        this._abrirConfig(config);
      }, dominio.codigos.length ? dominio.codigos : null).open();

    }).open();
  }

  _abrirConfig(config) {
    // Se é Atomizar, abre painel de seleção
    if (config.isAtomizar) {
      this.abrirAtomizar();
      return;
    }

    // Se é Enunciados, vai direto ao INDEX
    if (config.isEnunciados) {
      new Notice('📋 Abrindo Enunciados CJF...');
      this.app.workspace.openLinkText('00_APEX/ENUNCIADOS_CJF/INDEX-ENUNCIADOS', '', false);
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
  }

  // Painel para escolher qual área atomizar
  abrirAtomizar() {
    const areas = [
      { label: '📚 Direito Constitucional', pasta: '00_APEX/CONSTITUIÇÃO_FEDERAL' },
      { label: '📖 Código Civil', pasta: '01_PRIVADO/Codigos/CC' },
      { label: '⚖️  Código Penal', pasta: '02_PENAL/Codigos/CP' },
      { label: '📋 Processo Civil', pasta: '01_PRIVADO/Codigos/CPC/CÓDIGO_PROCESSO_CIVIL' },
      { label: '🔨 Processo Penal', pasta: '02_PENAL/Codigos/CPP' },
      { label: '🛡️  Direito Administrativo', pasta: '03_PUBLICO/Codigos/Admin/DIREITO_ADMINISTRATIVO' },
      { label: '💼 Direito Previdenciário', pasta: '05_ESPECIAL/Codigos/DIREITO_PREVIDENCIARIO' },
      { label: '🌐 Direito Digital', pasta: '05_ESPECIAL/Codigos/DIREITO_DIGITAL' },
      { label: '🌍 Direito Internacional', pasta: '05_ESPECIAL/Codigos/DIREITO_INTERNACIONAL' },
      { label: '🏪 Código Consumidor', pasta: '05_ESPECIAL/Codigos/DIREITO_DIGITAL' },
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
    await this.garantirIndexes();
    let parsed = { textoBase: '', paragrafos: [], incisos: [], alineas: [], correlatos: [] };
    try {
      const content = await this.app.vault.adapter.read(activeFile.path);
      parsed = parseArtigoMD(content);
    } catch (e) { console.error('Fenice info:', e); }

    const chaveIdx = `${config.tag}:${num}`;
    const enunciados = (this.enunciadosIndex    || {})[chaveIdx] || [];
    const jurisIdx   = (this.jurisprudenciaIndex || {})[chaveIdx] || [];

    const acessorios1 = meta.acessorios || null;
    new InfoModal(this.app, activeFile, config, num, parsed, enunciados, acessorios1, jurisIdx,
      () => { console.clear(); this.iniciarBusca(); },
      (lei) => this.buscarPorLei(lei),
      (n, cfg) => this.buscarPorNumero(cfg || config, n)).open();
  }

  async buscarEAbrir(config, input) {
    const termo = input.trim();
    // Aceita: "121", "1.228", "121-A", "121-B", "1.228-A"
    const isNumero = /^[\d.]+(-?[A-Za-z])?$/.test(termo);

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
    const numNorm = num.trim().toUpperCase();
    const temSufixo = /[A-Za-z]$/.test(numNorm); // ex: "121-A", "121-B"
    const numInt = parseInt(numNorm, 10);
    const bate = (meta) => {
      if (!meta) return false;
      const v = meta[campoChave];
      if (v == null) return false;
      const vs = String(v).trim().toUpperCase();
      // Match exato (cobre "121", "121-A", "1.228")
      if (vs === numNorm) return true;
      // Match numérico puro só quando não há sufixo (evita "121" bater em "121-A")
      if (!temSufixo && /^[\d.]+$/.test(numNorm)) {
        if (parseInt(vs, 10) === numInt && !/[A-Za-z]/.test(vs)) return true;
      }
      return false;
    };

    let found = null;
    for (const pasta of obterPastas(config)) {
      found = allFiles.find(f => pastaEhAncestral(pasta, f.path) && bate(this.app.metadataCache.getFileCache(f)?.frontmatter));
      if (found) break;
    }
    if (!found) {
      // Fallback por tag — prefere arquivos das pastas configuradas
      const pastas = obterPastas(config);
      const candidatos = allFiles.filter(f => {
        const meta = this.app.metadataCache.getFileCache(f)?.frontmatter;
        const tags = Array.isArray(meta?.tags) ? meta.tags : [];
        return bate(meta) && tags.includes(config.tag);
      });
      candidatos.sort((a, b) => {
        const aOrd = pastas.findIndex(p => pastaEhAncestral(p, a.path));
        const bOrd = pastas.findIndex(p => pastaEhAncestral(p, b.path));
        return (aOrd < 0 ? 999 : aOrd) - (bOrd < 0 ? 999 : bOrd);
      });
      found = candidatos[0] || null;
    }
    if (!found) { this.avisarNaoEncontrado(config, num); return; }

    console.log(`✅ Encontrado: ${found.path}`);
    new Notice(`✅ Art. ${num} — ${config.codigo}`, 2000);

    await this.garantirIndexes();
    let parsed = { textoBase: '', paragrafos: [], incisos: [], alineas: [], correlatos: [], videLeis: [], emendas: [] };
    try {
      const content = await this.app.vault.adapter.read(found.path);
      parsed = parseArtigoMD(content);
    } catch (e) { console.error('Fenice buscar:', e); }

    const chaveIdx = `${config.tag}:${num}`;
    const enunciados = (this.enunciadosIndex    || {})[chaveIdx] || [];
    const jurisIdx   = (this.jurisprudenciaIndex || {})[chaveIdx] || [];
    const acessorios2 = this.app.metadataCache.getFileCache(found)?.frontmatter?.acessorios || null;

    console.log(`   textoBase: ${parsed.textoBase?.slice(0,60)}...`);
    console.log(`   incisos: ${parsed.incisos.length} | paragrafos: ${parsed.paragrafos.length} | correlatos: ${parsed.correlatos.length}`);
    console.log(`   acessorios:`, acessorios2);
    console.log(`   jurisIdx: ${jurisIdx.length} entradas`);

    // Abre artigo na folha ativa → Copilot autoAddActiveContentToContext captura o conteúdo
    await this.app.workspace.getLeaf(false).openFile(found);

    new InfoModal(this.app, found, config, num, parsed, enunciados, acessorios2, jurisIdx,
      () => {
        console.clear();
        this.iniciarBusca();
      },
      (lei) => this.buscarPorLei(lei),
      (n, cfg) => this.buscarPorNumero(cfg || config, n)).open();
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
    await this.garantirIndexes();
    let parsed = { textoBase: '', paragrafos: [], incisos: [], alineas: [], correlatos: [] };
    try {
      const content = await this.app.vault.adapter.read(result.file.path);
      parsed = parseArtigoMD(content);
    } catch (e) { console.error('Fenice buscar tema:', e); }

    const num = result.meta.numero || result.meta.artigo || result.titulo;

    console.clear();
    console.log(`✅ Aberto: ${result.titulo}`);

    const chaveIdxTema = `${config.tag}:${num}`;
    const jurisIdxTema = (this.jurisprudenciaIndex || {})[chaveIdxTema] || [];
    const enunciadosTema = (this.enunciadosIndex || {})[chaveIdxTema] || [];
    const acessorios3 = result.meta?.acessorios || null;
    new InfoModal(this.app, result.file, config, num, parsed, enunciadosTema, acessorios3, jurisIdxTema,
      () => {
        console.clear();
        this.iniciarBusca();
      },
      (lei) => this.buscarPorLei(lei),
      (n, cfg) => this.buscarPorNumero(cfg || config, n)).open();
  }

  // ── Graph: grafo local com depth configurável ──
  async _abrirGrafoLocal(activeFile, depth) {
    const gp = this.app.internalPlugins?.plugins?.['graph'];
    if (!gp?.enabled) { new Notice('⚠ Plugin de Grafo não está habilitado. Reinicie o Obsidian.', 6000); return; }

    // Tenta abrir via setViewState passando file e depth
    const leaf = this.app.workspace.getLeaf('tab');
    await leaf.setViewState({
      type: 'localgraph',
      state: { file: activeFile.path },
    });
    this.app.workspace.revealLeaf(leaf);

    // Após abrir, tenta ajustar depth no renderer do grafo local
    if (depth > 1) {
      await new Promise(r => setTimeout(r, 400));
      try {
        const view = leaf.view;
        if (view?.renderer?.setOptions) {
          view.renderer.setOptions({ depth });
        } else if (view?.dataEngine) {
          view.dataEngine.depth = depth;
          view.dataEngine.updateWorker?.();
        }
      } catch (e) { /* API interna indisponível — usuário ajusta depth no slider */ }
      new Notice(`📊 Grafo local aberto. Se quiser depth ${depth}, ajuste o slider "Profundidade" no painel de filtros do grafo.`, 5000);
    }
  }

  // ── Graph: opção 1 — correlações entre ramos (smart filter) ──
  async abrirGraphCorrelacoes(activeFile) {
    if (!activeFile) { new Notice('Nenhum artigo aberto.', 2000); return; }

    let content = '';
    try { content = await this.app.vault.read(activeFile); } catch(e) { return; }

    const wikilinks = [...content.matchAll(/\[\[([^\]|]+)(?:\|[^\]]+)?\]\]/g)].map(m => m[1].trim());

    const pathsToShow = new Set();

    // Pasta do artigo atual
    const pastaAtual = this._resolverPastaDeArquivo(activeFile.path);
    if (pastaAtual) pathsToShow.add(pastaAtual);

    // Resolve cada wikilink → pasta do arquivo linkado
    for (const link of wikilinks) {
      const linkedFile = this.app.metadataCache.getFirstLinkpathDest(link, activeFile.path);
      if (linkedFile) {
        const pasta = this._resolverPastaDeArquivo(linkedFile.path);
        if (pasta) pathsToShow.add(pasta);
      }
    }

    if (pathsToShow.size === 0) {
      new Notice('Nenhuma correlação encontrada. Verifique os wikilinks do artigo.', 4000);
      return;
    }

    const query = [...pathsToShow].map(p => `path:"${p}"`).join(' OR ');
    const modulos = [...pathsToShow].map(p => p.split('/')[0]).filter((v, i, a) => a.indexOf(v) === i);
    new Notice(`📊 Grafo: ${modulos.join(' · ')} (${pathsToShow.size} pasta(s))`, 3000);
    await this._abrirGraphComFiltro(query);
  }

  // Retorna a pasta CODIGOS mais específica que contém o arquivo
  _resolverPastaDeArquivo(filePath) {
    for (const cod of CODIGOS) {
      const pastas = obterPastas(cod);
      for (const pasta of pastas) {
        if (filePath.startsWith(pasta.replace(/\/+$/, '') + '/')) return pasta;
      }
    }
    // Fallback: primeiros 4 segmentos do path
    const partes = filePath.split('/');
    if (partes.length < 2) return null;
    return partes.slice(0, Math.min(4, partes.length - 1)).join('/');
  }

  // ── Graph: opção 2 — código específico (picker) ──
  abrirGraphCodigo() {
    new DomainModal(this.app, (dominio) => {
      new CodigoModal(this.app, async (config) => {
        const pastas = obterPastas(config);
        if (pastas.length === 0) { new Notice(`Sem pasta configurada para ${config.codigo}.`, 3000); return; }
        const query = pastas.map(p => `path:"${p}"`).join(' OR ');
        new Notice(`📊 Grafo: ${config.codigo} (${pastas.length} pasta(s))`, 2000);
        await this._abrirGraphComFiltro(query);
      }, dominio.codigos.length ? dominio.codigos : null).open();
    }).open();
  }

  // ── Graph: escreve filtro em graph.json e reabre o grafo ──
  async _abrirGraphComFiltro(query) {
    // Verifica se o plugin de grafo está habilitado
    const gPlugin = this.app.internalPlugins?.plugins?.['graph'];
    if (!gPlugin?.enabled) {
      new Notice('⚠ Plugin de Grafo não está habilitado. Reinicie o Obsidian.', 6000);
      return;
    }

    // Escreve filtro em graph.json
    const graphJsonPath = '.obsidian/graph.json';
    let cfg = { search: query, close: false, showAttachments: false, showOrphans: false, hideUnresolved: true };
    try {
      const old = JSON.parse(await this.app.vault.adapter.read(graphJsonPath));
      cfg = { ...old, search: query, close: false };
    } catch (e) {}
    await this.app.vault.adapter.write(graphJsonPath, JSON.stringify(cfg, null, 2));

    // Fecha leaves existentes
    this.app.workspace.getLeavesOfType('graph').forEach(l => l.detach());

    await new Promise(r => setTimeout(r, 250));

    // Tenta abrir via método do plugin interno
    const inst = gPlugin.instance;
    if (inst && typeof inst.openGlobalGraph === 'function') {
      inst.openGlobalGraph();
      return;
    }

    // Fallback: executa comando registrado pelo plugin
    if (this.app.commands.commands['graph:open']) {
      this.app.commands.executeCommandById('graph:open');
      return;
    }

    // Fallback final: cria leaf diretamente
    const leaf = this.app.workspace.getLeaf('tab');
    await leaf.setViewState({ type: 'graph' });
    this.app.workspace.revealLeaf(leaf);
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

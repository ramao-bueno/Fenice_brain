# Enunciados CJF — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Criar base completa de Enunciados do CJF integrada ao plugin Fenice Buscar Artigo, exibindo enunciados relevantes no painel InfoModal ao buscar um artigo.

**Architecture:** Script Python faz POST ao CJF (`/enunciados/pesquisa/resultado`) por norma+artigo, gera `enunciados_index.json` (lookup `{"cc:299": [{"num":16,"jornada":"I JDC","texto":"..."}]}`), plugin carrega o JSON e exibe no InfoModal. Arquivos .md individuais por enunciado para estudo aprofundado.

**Tech Stack:** Python 3 (requests, BeautifulSoup4), JSON, Obsidian plugin JS (já existente), Obsidian Markdown.

---

## Mapeamento de Arquivos

| Arquivo | Ação | Responsabilidade |
|---|---|---|
| `scripts/enunciados_cjf_extractor.py` | Criar | Scraping CJF → JSON index |
| `FENICE bRain/00_ENUNCIADOS_CJF/enunciados_index.json` | Criar | Lookup rápido artigo→enunciados |
| `FENICE bRain/00_ENUNCIADOS_CJF/INDEX-ENUNCIADOS.md` | Criar | Índice navegável no Obsidian |
| `FENICE bRain/00_ENUNCIADOS_CJF/{jornada}/Enunciado-{N}.md` | Criar | Um .md por enunciado |
| `.obsidian/plugins/fenice-buscar-artigo/main.js` | Modificar | Exibe enunciados no InfoModal |

---

## Task 1: enunciados_cjf_extractor.py

**Files:**
- Create: `scripts/enunciados_cjf_extractor.py`

- [ ] **Criar extrator com POST ao CJF**

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extrator de Enunciados do CJF — https://www.cjf.jus.br/enunciados/
API: POST /enunciados/pesquisa/resultado com campos do formulário
"""
import sys, re, html, json, time
sys.stdout.reconfigure(encoding='utf-8')
import requests
from pathlib import Path
from bs4 import BeautifulSoup

BASE_URL = 'https://www.cjf.jus.br/enunciados/'
RESULTADO_URL = BASE_URL + 'pesquisa/resultado'
CACHE_DIR = Path(__file__).parent / '_cache_cjf'

# Normas disponíveis no CJF (id: nome)
NORMAS = {
    '1':   ('cc',           'Código Civil 2002 - Lei n. 10.406/2002'),
    '21':  ('cdc',          'Código de Defesa do Consumidor'),
    '2':   ('cp',           'Código Penal'),
    '3':   ('cpc',          'Código de Processo Civil 2015'),
    '4':   ('cf88',         'Constituição Federal 1988'),
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Fenice Brain / Estudo Juridico)',
    'Referer': BASE_URL,
}


def fazer_sessao():
    s = requests.Session()
    s.headers.update(HEADERS)
    s.get(BASE_URL, timeout=20)  # pega cookies de sessão
    return s


def buscar_enunciados_artigo(sessao, norma_id: str, artigo: str) -> list:
    """Busca todos os enunciados CJF para uma norma + artigo específico."""
    cache_key = CACHE_DIR / f'norma{norma_id}_art{artigo}.json'
    if cache_key.exists():
        return json.loads(cache_key.read_text(encoding='utf-8'))

    try:
        r = sessao.post(RESULTADO_URL, data={
            'buscaLivre': '',
            'jornada.id': '',
            'tipoComissao.id': '',
            'referenciasLegislativas[0].norma.id': norma_id,
            'referenciasLegislativas[0].artigo': artigo,
            'referenciasLegislativas[0].paragrafo': '',
            'referenciasLegislativas[0].inciso': '',
            'referenciasLegislativas[0].id': '',
        }, timeout=20)
        r.raise_for_status()
    except Exception as e:
        print(f'  ERR {norma_id}/art{artigo}: {e}')
        return []

    enunciados = parse_resultado_html(r.text, norma_id, artigo)
    cache_key.parent.mkdir(parents=True, exist_ok=True)
    cache_key.write_text(json.dumps(enunciados, ensure_ascii=False, indent=2), encoding='utf-8')
    return enunciados


def parse_resultado_html(html_text: str, norma_id: str, artigo: str) -> list:
    """Parseia o HTML de resultado e extrai enunciados."""
    txt = html.unescape(re.sub(r'<[^>]+>', ' ', html_text))
    txt = re.sub(r'\s+', ' ', txt).strip()

    enunciados = []
    # Padrão: "X Jornada de Y - Enunciado N texto..."
    padrao = re.compile(
        r'((?:[IVX]+\s+Jornada[^-]+?)\s*-\s*Enunciado\s+(\d+))\s+'
        r'(.+?)(?=(?:[IVX]+\s+Jornada)|$)',
        re.DOTALL
    )
    for m in padrao.finditer(txt):
        jornada_nome = m.group(1).strip()
        num = int(m.group(2))
        texto = re.sub(r'\s+', ' ', m.group(3)).strip()
        if texto and len(texto) > 10:
            enunciados.append({
                'num': num,
                'jornada': jornada_nome,
                'texto': texto,
                'norma_id': norma_id,
                'artigo': artigo,
            })

    return enunciados


def processar_todos_artigos(artigos_por_norma: dict, delay: float = 0.5) -> dict:
    """
    artigos_por_norma: {'1': ['1','2','3',...,'2046'], '2': ['121','129',...]}
    Retorna: {'cc:1': [...], 'cc:2': [...], ...}
    """
    sessao = fazer_sessao()
    index = {}
    total = sum(len(v) for v in artigos_por_norma.values())
    processados = 0

    for norma_id, artigos in artigos_por_norma.items():
        codigo = NORMAS.get(norma_id, (norma_id, ''))[0]
        for artigo in artigos:
            chave = f'{codigo}:{artigo}'
            ens = buscar_enunciados_artigo(sessao, norma_id, artigo)
            if ens:
                index[chave] = ens
                print(f'  {chave}: {len(ens)} enunciados')
            processados += 1
            if processados % 50 == 0:
                pct = processados / total * 100
                print(f'  Progresso: {processados}/{total} ({pct:.0f}%)')
            time.sleep(delay)

    return index


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Extrator Enunciados CJF')
    parser.add_argument('--test', action='store_true', help='Testa com Art. 299 CC')
    parser.add_argument('--cc', action='store_true', help='Processa CC livros I e II (arts. 1-709)')
    parser.add_argument('--full', action='store_true', help='Processa CC completo (1-2046)')
    args = parser.parse_args()

    s = fazer_sessao()

    if args.test:
        ens = buscar_enunciados_artigo(s, '1', '299')
        print(f'Art. 299 CC — {len(ens)} enunciados:')
        for e in ens:
            print(f'  Enunciado {e["num"]} ({e["jornada"]}): {e["texto"][:100]}...')

    elif args.cc or args.full:
        fim = 2046 if args.full else 709
        artigos = [str(n) for n in range(1, fim + 1)]
        index = processar_todos_artigos({'1': artigos}, delay=0.3)
        out = Path(r'C:\Users\oicon\OneDrive\Allah - Islamismo\Stand Alone Legaltech\Fenice brain\FENICE bRain\00_ENUNCIADOS_CJF\enunciados_index.json')
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding='utf-8')
        total_ens = sum(len(v) for v in index.values())
        print(f'\nIndex salvo: {len(index)} artigos com enunciados, {total_ens} total')
```

- [ ] **Testar com Art. 299 CC**
```bash
cd scripts && python enunciados_cjf_extractor.py --test
```
Esperado:
```
Art. 299 CC — 2 enunciados:
  Enunciado 16 (I Jornada de Direito Civil): O art. 299 do Código Civil...
  Enunciado 648 (IX Jornada de Direito Civil): Art. 299: Aplica-se à...
```

- [ ] **Commit**
```bash
git add scripts/enunciados_cjf_extractor.py
git commit -m "feat: extrator enunciados CJF via POST API"
```

---

## Task 2: Gerar enunciados_index.json (CC livros I e II)

**Files:**
- Create: `FENICE bRain/00_ENUNCIADOS_CJF/enunciados_index.json`

- [ ] **Rodar para artigos CC 1-709 (com cache)**
```bash
python enunciados_cjf_extractor.py --cc
```
Esperado: ~200-400 artigos CC com enunciados, arquivo JSON gerado.

- [ ] **Verificar arquivo gerado**
```bash
python -c "
import json, sys; sys.stdout.reconfigure(encoding='utf-8')
d = json.load(open(r'FENICE bRain/00_ENUNCIADOS_CJF/enunciados_index.json', encoding='utf-8'))
print('Artigos com enunciados:', len(d))
print('Exemplo cc:299:', d.get('cc:299', []))
"
```

- [ ] **Commit**
```bash
git add "FENICE bRain/00_ENUNCIADOS_CJF/"
git commit -m "feat: enunciados_index.json CC arts 1-709"
```

---

## Task 3: Gerador de arquivos .md por Enunciado

**Files:**
- Create: `scripts/generate_enunciados_md.py`

- [ ] **Criar gerador de .md**

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera arquivos .md individuais para cada enunciado."""
import sys, json, re, yaml
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime

INDEX_PATH = Path(r'C:\Users\oicon\OneDrive\Allah - Islamismo\Stand Alone Legaltech\Fenice brain\FENICE bRain\00_ENUNCIADOS_CJF\enunciados_index.json')
OUT_BASE = INDEX_PATH.parent


def jornada_sigla(nome: str) -> str:
    """Converte 'IX Jornada de Direito Civil' -> 'IX-JDC'"""
    m = re.match(r'([IVX]+)\s+Jornada\s+(?:de\s+)?(.+)', nome, re.I)
    if m:
        num = m.group(1)
        tipo = m.group(2).strip()
        abrev = ''.join(p[0].upper() for p in tipo.split()[:2])
        return f'{num}-J{abrev}'
    return re.sub(r'\s+', '-', nome)[:20]


def gerar_md_enunciado(e: dict) -> str:
    num = e['num']
    jornada = e['jornada']
    texto = e['texto']
    artigo = e['artigo']
    codigo = e.get('norma_id_label', 'CC')
    sigla = jornada_sigla(jornada)

    fm = {
        'enunciado': str(num),
        'jornada': jornada,
        'jornada_sigla': sigla,
        'artigo_ref': artigo,
        'codigo_ref': codigo,
        'tags': ['enunciado', 'cjf', 'jdc', codigo, f'art-{artigo}', f'enunciado-{num}'],
        'created': datetime.now().strftime('%Y-%m-%d'),
    }
    fm_str = yaml.dump(fm, allow_unicode=True, default_flow_style=False, sort_keys=False)

    return f"""---
{fm_str}---

# Enunciado {num} — {jornada}

**Artigo de referência:** Art. {artigo} {codigo.upper()}
**Jornada:** {jornada}

---

## Texto

{texto}

---

## Artigo Referenciado

- [[Art. {artigo} — Código Civil]] — Art. {artigo} CC

## Links

- [[INDEX-ENUNCIADOS]] — Índice geral dos enunciados
"""


def main():
    if not INDEX_PATH.exists():
        print('index nao encontrado — rode enunciados_cjf_extractor.py --cc primeiro')
        return

    index = json.loads(INDEX_PATH.read_text(encoding='utf-8'))
    
    # Mapeia enunciado num -> dados (evita duplicatas)
    enunciados_unicos = {}
    for chave, lista in index.items():
        codigo = chave.split(':')[0]
        for e in lista:
            num = e['num']
            if num not in enunciados_unicos:
                e['norma_id_label'] = codigo
                enunciados_unicos[num] = e

    print(f'Gerando {len(enunciados_unicos)} arquivos .md...')
    gerados = 0
    for num, e in sorted(enunciados_unicos.items()):
        sigla = jornada_sigla(e['jornada'])
        pasta = OUT_BASE / sigla
        pasta.mkdir(parents=True, exist_ok=True)
        path = pasta / f'Enunciado-{num}.md'
        path.write_text(gerar_md_enunciado(e), encoding='utf-8')
        gerados += 1

    print(f'Gerados: {gerados} enunciados em {OUT_BASE}')
    
    # INDEX geral
    linhas = ['# INDEX — Enunciados CJF\n\n']
    for num, e in sorted(enunciados_unicos.items()):
        sigla = jornada_sigla(e['jornada'])
        linhas.append(f'- [[{sigla}/Enunciado-{num}|Enunciado {num}]] — Art. {e["artigo"]} CC\n')
    
    (OUT_BASE / 'INDEX-ENUNCIADOS.md').write_text(''.join(linhas), encoding='utf-8')
    print('INDEX-ENUNCIADOS.md gerado')


if __name__ == '__main__':
    main()
```

- [ ] **Rodar gerador**
```bash
python generate_enunciados_md.py
```

- [ ] **Commit**
```bash
git add scripts/generate_enunciados_md.py "FENICE bRain/00_ENUNCIADOS_CJF/"
git commit -m "feat: gera arquivos .md por enunciado CJF com frontmatter"
```

---

## Task 4: Atualizar plugin InfoModal para mostrar Enunciados

**Files:**
- Modify: `.obsidian/plugins/fenice-buscar-artigo/main.js`

- [ ] **Carregar enunciados_index.json no plugin**

Na função `onload()` do plugin, adicionar após `this.addCommand(...)`:

```javascript
// Carrega index de enunciados (caminho relativo ao vault root)
this.enunciadosIndex = {};
this.app.vault.adapter.read('FENICE bRain/00_ENUNCIADOS_CJF/enunciados_index.json')
  .then(txt => {
    this.enunciadosIndex = JSON.parse(txt);
    console.log('Fenice: enunciados carregados:', Object.keys(this.enunciadosIndex).length);
  })
  .catch(() => console.log('Fenice: enunciados_index.json nao encontrado'));
```

- [ ] **Passar enunciados para o InfoModal**

Em `buscarEAbrir` e `mostrarInfoAtual`, antes de `new InfoModal(...)`, adicionar:

```javascript
// Lookup no index: chave = "cc:299", "cf88:5", etc.
const chaveIndex = `${config.tag}:${num}`;
const enunciados = (this.enunciadosIndex || {})[chaveIndex] || [];
```

E passar `enunciados` como parâmetro extra: `new InfoModal(..., enunciados, ...)`.

- [ ] **Exibir enunciados no InfoModal.onOpen()**

Após a seção de correlatos, antes dos botões:

```javascript
// ── Enunciados CJF ──
if (enunciados && enunciados.length) {
  const sec = contentEl.createEl('div');
  Object.assign(sec.style, {
    borderTop: '1px solid var(--background-modifier-border)',
    paddingTop: '8px', marginBottom: '10px', fontSize: '13px',
  });
  const header = sec.createEl('p');
  header.style.marginBottom = '4px';
  header.createEl('strong', { text: '📋 Enunciados CJF' });
  
  for (const e of enunciados) {
    const p = sec.createEl('p');
    p.style.marginLeft = '8px';
    p.style.marginBottom = '6px';
    p.style.borderLeft = '2px solid var(--interactive-accent)';
    p.style.paddingLeft = '8px';
    p.style.lineHeight = '1.5';
    
    const link = p.createEl('span');
    link.style.color = 'var(--text-accent)';
    link.style.cursor = 'pointer';
    link.style.fontWeight = 'bold';
    const jSigla = e.jornada.match(/^([IVX]+)/)?.[1] || '';
    link.textContent = `Enunciado ${e.num} (${jSigla} JDC)`;
    link.title = 'Abrir enunciado completo';
    link.addEventListener('click', () => {
      this.close();
      this.app.workspace.openLinkText(`Enunciado-${e.num}`, '', false);
    });
    
    p.appendText(': ' + e.texto);
  }
}
```

- [ ] **Atualizar assinatura do InfoModal**

```javascript
class InfoModal extends Modal {
  constructor(app, found, config, num, parsed, enunciados, onNovaBusca) {
    // ... adicionar this.enunciados = enunciados || [];
  }
  // usar this.enunciados na seção de enunciados
}
```

- [ ] **Validar sintaxe**
```bash
node --check .obsidian/plugins/fenice-buscar-artigo/main.js
```
Esperado: sem output (= sem erros).

- [ ] **Commit**
```bash
git add ".obsidian/plugins/fenice-buscar-artigo/main.js"
# .obsidian está em .gitignore — OK
git add "FENICE bRain/00_ENUNCIADOS_CJF/"
git commit -m "feat: enunciados CJF no InfoModal + arquivos .md individuais"
```

---

## Task 5: Validação final no Obsidian

- [ ] Reload Obsidian (`Ctrl+P` → "Reload app without saving")
- [ ] `Ctrl+Shift+B` → CC → 299
- [ ] Verificar que InfoModal mostra:
  ```
  📋 Enunciados CJF
  Enunciado 16 (I JDC): O art. 299 do CC não exclui a possibilidade...
  Enunciado 648 (IX JDC): Art. 299: Aplica-se à cessão da posição...
  ```
- [ ] Clicar num enunciado — abre `Enunciado-16.md`
- [ ] `Ctrl+Shift+B` → CC → 48 — verificar enunciados do Art. 48
- [ ] Commit final se tudo OK

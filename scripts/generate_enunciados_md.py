#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera arquivos .md individuais para cada enunciado CJF."""
import sys, json, re, yaml
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent
INDEX_PATH = PROJECT_ROOT / 'Fenice bRain' / '00_ENUNCIADOS_CJF' / 'enunciados_index.json'
OUT_BASE   = INDEX_PATH.parent

CODIGO_NOMES = {
    'cc':   'Código Civil',
    'cpc':  'CPC',
    'cp':   'Código Penal',
    'cf88': 'CF/88',
}


def jornada_pasta(nome: str) -> str:
    """'IX Jornada de Direito Civil' -> 'IX-JDC'"""
    m = re.match(r'([IVX]+)\s+Jornada\s+(?:de\s+)?(.+)', nome, re.I)
    if m:
        num  = m.group(1)
        tipo = m.group(2).strip()
        sigla = ''.join(p[0].upper() for p in tipo.split()[:2])
        return f'{num}-J{sigla}'
    return re.sub(r'[^A-Za-z0-9]+', '-', nome)[:20]


def jornada_sigla(nome: str) -> str:
    """'IX Jornada de Direito Civil' -> 'IX JDC'"""
    m = re.match(r'([IVX]+)\s+Jornada\s+(?:de\s+)?(.+)', nome, re.I)
    if m:
        return f'{m.group(1)} JDC'
    return nome


def gerar_md(e: dict, codigo: str) -> str:
    num    = e['num']
    jnome  = e['jornada']
    texto  = e['texto']
    artigo = e['artigo']
    jsigla = jornada_sigla(jnome)
    cnome  = CODIGO_NOMES.get(codigo, codigo.upper())

    # Wikilink para o artigo
    wikilink_art = f'Art. {artigo} — {cnome}'

    fm = {
        'enunciado':    str(num),
        'jornada':      jnome,
        'jornada_sigla':jsigla,
        'artigo_ref':   artigo,
        'codigo_ref':   codigo,
        'tags': [
            'enunciado', 'cjf', 'jdc', codigo,
            f'art-{artigo}', f'enunciado-{num}',
        ],
        'created': datetime.now().strftime('%Y-%m-%d'),
    }
    fm_str = yaml.dump(fm, allow_unicode=True, default_flow_style=False, sort_keys=False)

    return f"""---
{fm_str}---

# Enunciado {num} — {jsigla}

**Artigo de referência:** Art. {artigo} {cnome.upper()}
**Jornada:** {jnome}

---

## Texto

{texto}

---

## Artigo Referenciado

- [[{wikilink_art}]] — Art. {artigo} {cnome}

## Links

- [[INDEX-ENUNCIADOS]] — Índice geral dos Enunciados CJF
- [[INDEX — CF/88 Completo]] — Hierarquia normativa
"""


def gerar_index(enunciados_unicos: dict) -> str:
    linhas = [
        '---\n',
        'tags: [enunciado, cjf, jdc, index]\n',
        f'created: {datetime.now().strftime("%Y-%m-%d")}\n',
        '---\n\n',
        '# INDEX — Enunciados CJF\n\n',
        f'**Total:** {len(enunciados_unicos)} enunciados | **Fonte:** CJF — Jornadas de Direito\n\n',
        '---\n\n',
    ]
    for num, (e, pasta) in sorted(enunciados_unicos.items()):
        sigla = jornada_sigla(e['jornada'])
        linhas.append(
            f'- [[{pasta}/Enunciado-{num}|Enunciado {num}]] '
            f'({sigla}) — Art. {e["artigo"]} {e.get("codigo","cc").upper()}\n'
        )
    return ''.join(linhas)


def main():
    if not INDEX_PATH.exists():
        print('index nao encontrado — rode enunciados_cjf_extractor.py --cc primeiro')
        return

    index = json.loads(INDEX_PATH.read_text(encoding='utf-8'))

    # Consolida enunciados únicos (mesmo num pode aparecer em vários artigos)
    unicos: dict[int, tuple] = {}   # num -> (enunciado, pasta)
    for chave, lista in index.items():
        codigo = chave.split(':')[0]
        for e in lista:
            num = e['num']
            e['codigo'] = codigo
            if num not in unicos:
                pasta = jornada_pasta(e['jornada'])
                unicos[num] = (e, pasta)

    print(f'Gerando {len(unicos)} arquivos .md de enunciados...')
    gerados = 0

    for num, (e, pasta_nome) in sorted(unicos.items()):
        pasta = OUT_BASE / pasta_nome
        pasta.mkdir(parents=True, exist_ok=True)
        path = pasta / f'Enunciado-{num}.md'
        path.write_text(gerar_md(e, e.get('codigo', 'cc')), encoding='utf-8')
        gerados += 1

    print(f'  {gerados} arquivos .md gerados')

    # INDEX geral
    idx_md = gerar_index(unicos)
    idx_path = OUT_BASE / 'INDEX-ENUNCIADOS.md'
    idx_path.write_text(idx_md, encoding='utf-8')
    print(f'  INDEX-ENUNCIADOS.md gerado')

    print(f'\nSaida: {OUT_BASE}')


if __name__ == '__main__':
    main()

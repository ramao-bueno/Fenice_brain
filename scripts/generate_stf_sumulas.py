#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera Súmulas Comuns do STF no padrão Fenice Brain
Fonte: portal.stf.jus.br (base=30)
IDs extraídos via Chrome DevTools do DOM renderizado

Uso:
    python generate_stf_sumulas.py --test      # Testa súmulas 1, 100, 700
    python generate_stf_sumulas.py --full      # Gera todas as 736
    python generate_stf_sumulas.py --limit 50  # Primeiras 50
"""
import sys, re, html as hlib, json, time, yaml, argparse
sys.stdout.reconfigure(encoding='utf-8')
import requests
from pathlib import Path
from datetime import datetime
import urllib3; urllib3.disable_warnings()

PROJECT_ROOT = Path(__file__).parent.parent
IDS_PATH     = Path(__file__).parent / '_stf_sumulas_ids.json'
CACHE_DIR    = Path(__file__).parent / '_cache_stf_sumulas'
OUTPUT_BASE  = PROJECT_ROOT / 'FENICE bRain' / '05_STF_SUMULAS' / 'Comuns'
STF_URL_BASE = 'https://portal.stf.jus.br/jurisprudencia/sumariosumulas.asp'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html',
    'Accept-Language': 'pt-BR,pt;q=0.9',
    'Referer': f'{STF_URL_BASE}?base=30',
}

STATUS_LABELS = {
    'vigente':  'vigente',
    'cancelada':'cancelada',
    'superada': 'superada',
    'revogada': 'revogada',
    'alterada': 'alterada',
}


def buscar_texto_sumula(stf_id: str, num: int, sessao: requests.Session) -> str:
    """Busca e extrai o texto da súmula pelo ID interno do STF."""
    cache = CACHE_DIR / f'{stf_id}.txt'
    if cache.exists():
        return cache.read_text(encoding='utf-8')

    url = f'{STF_URL_BASE}?base=30&sumula={stf_id}'
    try:
        r = sessao.get(url, timeout=20, verify=False)
        r.encoding = 'utf-8'
        limpo = hlib.unescape(re.sub(r'<[^>]+>', ' ', r.text))
        limpo = re.sub(r'\s+', ' ', limpo).strip()
    except Exception as e:
        print(f'  ERRO {num} (id={stf_id}): {e}')
        return ''

    # Extrai texto: vem após "Súmula N " até "Jurisprudência selecionada"
    m = re.search(
        rf'Súmula\s+{num}\s+(.+?)(?=Jurisprudência\s+selecionada|Aplicação\s+das\s+Súmulas|Mapa\s+do\s+Site)',
        limpo, re.DOTALL
    )
    texto = m.group(1).strip() if m else ''

    # Limpa quebras e espaços duplos
    texto = re.sub(r'\s+', ' ', texto).strip()

    if texto:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        cache.write_text(texto, encoding='utf-8')

    return texto


def gerar_md(num: int, texto: str, status: str) -> str:
    status_label = STATUS_LABELS.get(status, status)
    status_icon  = '✅' if status == 'vigente' else '⚠️' if status == 'alterada' else '❌'
    planalto_url = f'{STF_URL_BASE}?base=30&numero={num}'

    tags = ['stf', 'sumula', f'sumula-{num}', 'jurisprudencia', status_label]
    if status == 'vigente':
        tags.append('stf-vigente')

    fm = {
        'sumula':       str(num),
        'tipo':         'sumula-stf',
        'tribunal':     'STF',
        'status':       status_label,
        'planalto_url': planalto_url,
        'tags':         tags,
        'created':      datetime.now().strftime('%Y-%m-%d'),
    }
    fm_str = yaml.dump(fm, allow_unicode=True, default_flow_style=False, sort_keys=False)

    texto_display = texto if texto else f'[Texto não disponível — verificar em {planalto_url}]'

    return f"""---
{fm_str}---

# STF Súmula {num}

**Status:** {status_icon} {status_label.upper()}
**Fonte:** [STF — Súmulas]({planalto_url})

---

## ENUNCIADO

> {texto_display}

---

## APLICAÇÃO

[Notas de aplicação e contexto]

---

## JURISPRUDÊNCIA RELACIONADA

[Precedentes que deram origem a esta súmula]

---

**Tribunal:** Supremo Tribunal Federal
**Tipo:** Súmula (não vinculante — persuasiva)
**Última atualização:** {datetime.now().strftime('%Y-%m-%d')}
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--test',  action='store_true', help='Testa 3 súmulas (1, 100, 700)')
    parser.add_argument('--full',  action='store_true', help='Gera todas as 736 súmulas')
    parser.add_argument('--limit', type=int, default=20, help='Gera N primeiras súmulas')
    args = parser.parse_args()

    sep = '=' * 60
    print(f'\n{sep}')
    print('GERADOR SÚMULAS STF (Comuns — base=30)')
    print(f'{sep}\n')

    # Carrega lista de IDs
    lista = json.loads(IDS_PATH.read_text(encoding='utf-8'))
    print(f'{len(lista)} súmulas mapeadas')

    # Filtra
    if args.test:
        lista = [x for x in lista if x['num'] in [1, 100, 700]]
    elif not args.full:
        lista = lista[:args.limit]

    print(f'Processando {len(lista)} súmulas...\n')

    OUTPUT_BASE.mkdir(parents=True, exist_ok=True)
    sessao = requests.Session()
    sessao.headers.update(HEADERS)

    salvos = 0
    erros = 0

    for i, item in enumerate(lista, 1):
        num    = item['num']
        stf_id = item['id']
        status = item['status']

        texto = buscar_texto_sumula(stf_id, num, sessao)
        if not texto and status == 'vigente':
            erros += 1

        conteudo = gerar_md(num, texto, status)
        fname = f'Sumula-{num:04d}.md'
        (OUTPUT_BASE / fname).write_text(conteudo, encoding='utf-8')
        salvos += 1

        if texto:
            print(f'  ✔ {fname}: {texto[:60]}...')
        else:
            print(f'  ⚠ {fname}: texto vazio ({status})')

        if i % 50 == 0:
            print(f'  --- {i}/{len(lista)} ({i/len(lista)*100:.0f}%) ---')

        time.sleep(0.25)  # respeita o servidor

    # INDEX
    todos = json.loads(IDS_PATH.read_text(encoding='utf-8')) if args.full else lista
    vigentes    = [x for x in todos if x['status'] == 'vigente']
    nao_vig     = [x for x in todos if x['status'] != 'vigente']

    idx_linhas = [
        '---\n',
        'tags: [stf, sumula, jurisprudencia, index]\n',
        f'created: {datetime.now().strftime("%Y-%m-%d")}\n',
        '---\n\n',
        '# INDEX — Súmulas STF (Comuns)\n\n',
        f'**Total:** {len(todos)} | **Vigentes:** {len(vigentes)} | **Não vigentes:** {len(nao_vig)}\n',
        f'**Fonte:** [portal.stf.jus.br]({STF_URL_BASE}?base=30)\n\n',
        '---\n\n',
        '## Súmulas Vigentes\n\n',
    ]
    for x in vigentes:
        idx_linhas.append(f'- [[Sumula-{x["num"]:04d}|Súmula {x["num"]}]]\n')

    if nao_vig:
        idx_linhas.append('\n## Não Vigentes (cancelada/superada/revogada/alterada)\n\n')
        for x in nao_vig:
            idx_linhas.append(f'- [[Sumula-{x["num"]:04d}|Súmula {x["num"]}]] ({x["status"]}) ⚠️\n')

    idx_linhas += [
        '\n---\n\n',
        '## Links\n\n',
        '- [[INDEX-SV-STF]] — Súmulas Vinculantes\n',
        '- [[INDEX — CF/88 Completo]] — Constituição Federal\n',
        '- [[00_NAVIGATOR]] — Busca por código\n',
    ]
    (OUTPUT_BASE.parent / 'INDEX-Sumulas-STF.md').write_text(''.join(idx_linhas), encoding='utf-8')

    print(f'\n{sep}')
    print(f'CONCLUIDO: {salvos} súmulas geradas ({erros} sem texto)')
    print(f'Saída: {OUTPUT_BASE}')
    print(sep)


if __name__ == '__main__':
    main()

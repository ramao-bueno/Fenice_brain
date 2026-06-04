#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extrator de Enunciados do CJF — https://www.cjf.jus.br/enunciados/
API: POST /enunciados/pesquisa/resultado

Uso:
    python enunciados_cjf_extractor.py --test        # Art. 299 CC
    python enunciados_cjf_extractor.py --cc          # CC arts 1-709
    python enunciados_cjf_extractor.py --full        # CC arts 1-2046
"""
import sys, re, html, json, time, argparse
sys.stdout.reconfigure(encoding='utf-8')
import requests
from pathlib import Path

BASE_URL    = 'https://www.cjf.jus.br/enunciados/'
RESULTADO   = BASE_URL + 'pesquisa/resultado'
CACHE_DIR   = Path(__file__).parent / '_cache_cjf'
PROJECT_ROOT = Path(__file__).parent.parent
INDEX_OUT   = PROJECT_ROOT / 'FENICE bRain' / '00_ENUNCIADOS_CJF' / 'enunciados_index.json'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Fenice Brain / Estudo Juridico)',
    'Referer': BASE_URL,
}

# norma_id: (codigo_tag, nome)
NORMAS = {
    '1': ('cc',   'Código Civil 2002'),
    '3': ('cpc',  'CPC 2015'),
    '2': ('cp',   'Código Penal'),
    '4': ('cf88', 'Constituição Federal 1988'),
}


def fazer_sessao() -> requests.Session:
    s = requests.Session()
    s.headers.update(HEADERS)
    s.get(BASE_URL, timeout=20)
    return s


def buscar_artigo(sessao: requests.Session, norma_id: str, artigo: str) -> list:
    """Retorna lista de enunciados para norma+artigo. Usa cache local."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache = CACHE_DIR / f'n{norma_id}_a{artigo}.json'

    if cache.exists():
        return json.loads(cache.read_text(encoding='utf-8'))

    try:
        r = sessao.post(RESULTADO, data={
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
        print(f'  ERRO {norma_id}/art{artigo}: {e}')
        return []

    resultado = _parse_html(r.text, norma_id, artigo)
    cache.write_text(json.dumps(resultado, ensure_ascii=False, indent=2), encoding='utf-8')
    return resultado


def _parse_html(html_text: str, norma_id: str, artigo: str) -> list:
    """Parseia HTML de resultado e extrai enunciados."""
    txt = html.unescape(re.sub(r'<[^>]+>', ' ', html_text))
    txt = re.sub(r'\s+', ' ', txt).strip()

    enunciados = []
    # Padrão: "I/II/.../IX Jornada de ... - Enunciado N texto..."
    padrao = re.compile(
        r'([IVX]+\s+Jornada[^-]+?-\s*Enunciado\s+(\d+))\s+'
        r'(.+?)(?=[IVX]+\s+Jornada|\Z)',
        re.DOTALL
    )
    for m in padrao.finditer(txt):
        jornada = re.sub(r'\s+', ' ', m.group(1)).strip()
        num     = int(m.group(2))
        texto   = re.sub(r'\s+', ' ', m.group(3)).strip()
        if texto and len(texto) > 10:
            enunciados.append({
                'num':      num,
                'jornada':  jornada.replace(' - Enunciado ' + str(num), '').strip(),
                'texto':    texto,
                'norma_id': norma_id,
                'artigo':   artigo,
            })
    return enunciados


def processar_norma(norma_id: str, artigos: list, delay: float = 0.4) -> dict:
    """Processa todos os artigos de uma norma. Retorna sub-index."""
    codigo = NORMAS.get(norma_id, (norma_id,))[0]
    sessao = fazer_sessao()
    sub = {}
    total = len(artigos)

    for i, artigo in enumerate(artigos, 1):
        ens = buscar_artigo(sessao, norma_id, artigo)
        if ens:
            chave = f'{codigo}:{artigo}'
            sub[chave] = ens
            print(f'  {chave}: {len(ens)} enunciados')
        if i % 50 == 0 or i == total:
            print(f'  Progresso: {i}/{total} ({i/total*100:.0f}%)')
        time.sleep(delay)

    return sub


def salvar_index(index: dict):
    INDEX_OUT.parent.mkdir(parents=True, exist_ok=True)
    INDEX_OUT.write_text(
        json.dumps(index, ensure_ascii=False, indent=2), encoding='utf-8'
    )
    total_ens = sum(len(v) for v in index.values())
    print(f'\nIndex salvo: {len(index)} artigos, {total_ens} enunciados')
    print(f'Arquivo: {INDEX_OUT}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extrator Enunciados CJF')
    parser.add_argument('--test', action='store_true',
                        help='Testa com Art. 299 CC')
    parser.add_argument('--cc', action='store_true',
                        help='CC arts 1-709 (Livros I e II)')
    parser.add_argument('--full', action='store_true',
                        help='CC arts 1-2046 completo')
    parser.add_argument('--artigo', type=str,
                        help='Artigo especifico (ex: --artigo 48)')
    args = parser.parse_args()

    if args.test:
        s = fazer_sessao()
        ens = buscar_artigo(s, '1', '299')
        print(f'\nArt. 299 CC — {len(ens)} enunciados:')
        for e in ens:
            print(f'  [{e["num"]}] {e["jornada"]}: {e["texto"][:120]}...')

    elif args.artigo:
        s = fazer_sessao()
        ens = buscar_artigo(s, '1', args.artigo)
        print(f'\nArt. {args.artigo} CC — {len(ens)} enunciados:')
        for e in ens:
            print(f'  [{e["num"]}] {e["jornada"]}: {e["texto"][:120]}...')

    elif args.cc or args.full:
        fim = 2046 if args.full else 709
        artigos = [str(n) for n in range(1, fim + 1)]
        print(f'Processando CC arts 1-{fim} ({len(artigos)} artigos)...')
        idx = processar_norma('1', artigos, delay=0.3)
        salvar_index(idx)

    else:
        parser.print_help()

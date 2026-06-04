#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pipeline CF: Planalto.gov.br -> Markdown estruturado

Busca o texto oficial da CF/88 diretamente do Planalto,
garantindo texto atual com todas as Emendas Constitucionais.

Uso:
    python pipeline_cf.py              # 5 primeiros artigos (teste)
    python pipeline_cf.py --full       # Todos os artigos
    python pipeline_cf.py --limit 20   # Primeiros N artigos
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

from pathlib import Path
from config_cf import OUTPUT_BASE, TITULO_MAPEAMENTO, LEI_NOME
from cf_planalto_extractor import CFPlanaltoExtractor
from markdown_generator_cf import MarkdownGeneratorCF


def pipeline_cf(limit=None):
    sep = "=" * 60
    print(f"\n{sep}")
    print("PIPELINE CF/88: Planalto.gov.br -> Markdown")
    print(f"{sep}\n")

    print("ETAPA 1: Extraindo artigos do Planalto.gov.br...")
    extractor = CFPlanaltoExtractor()
    artigos = extractor.extract_articles()

    if not artigos:
        print("ERRO: Nenhum artigo extraido!")
        return False

    if limit:
        artigos = artigos[:limit]
        print(f"  Limitado a {limit} artigos para teste")

    print(f"  {len(artigos)} artigos prontos\n")

    print("ETAPA 2: Gerando notas Markdown...")
    gerador = MarkdownGeneratorCF(OUTPUT_BASE)

    salvos = 0
    erros = 0
    por_titulo = {}

    for i, art in enumerate(artigos, 1):
        try:
            titulo = art.get("livro", "SEM_TITULO")
            conteudo = gerador.gerar_nota_artigo(art, titulo)
            filepath = gerador.salvar_artigo(art, conteudo, titulo)
            if filepath:
                salvos += 1
                por_titulo[titulo] = por_titulo.get(titulo, 0) + 1

            if i % 25 == 0 or i == len(artigos):
                pct = (i / len(artigos)) * 100
                print(f"  {i:>4d}/{len(artigos)} artigos processados ({pct:.0f}%)")

        except Exception as e:
            erros += 1
            continue

    print(f"\n{sep}")
    print("PIPELINE CF/88 CONCLUIDO!")
    print(f"{sep}")
    print(f"\nESTATISTICAS:")
    print(f"  Artigos extraidos : {len(artigos)}")
    print(f"  Artigos salvos    : {salvos}")
    print(f"  Erros             : {erros}")

    if salvos > 0:
        print("\n  Por Titulo:")
        for titulo in sorted(TITULO_MAPEAMENTO.keys()):
            count = por_titulo.get(titulo, 0)
            if count > 0:
                nome = TITULO_MAPEAMENTO[titulo]["nome"]
                print(f"    {titulo}: {count} artigos  ({nome})")

    print(f"\n  Saida: {OUTPUT_BASE}\n")
    return salvos > 0


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Pipeline CF/88: Planalto -> Markdown"
    )
    parser.add_argument("--full", action="store_true",
                        help="Gerar todos os artigos")
    parser.add_argument("--limit", type=int, default=5,
                        help="Numero maximo de artigos (padrao: 5)")

    args = parser.parse_args()
    limit_artigos = None if args.full else args.limit

    sucesso = pipeline_cf(limit=limit_artigos)
    sys.exit(0 if sucesso else 1)

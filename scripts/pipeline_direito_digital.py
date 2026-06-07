#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pipeline Direito Digital: HTML local (Planalto) -> Markdown estruturado

Processa as 4 leis substantivas com numeração padrão "Art. N" já salvas como
HTML em DIREITO_DIGITAL/: Marco Civil (12.965), LGPD (13.709), Lei do Software
(9.609) e Lei de Direitos Autorais (9.610).

Leis modificativas (L12737, L14155 — inserem tipos penais no CP) ficam fora
do pipeline regex e são atomizadas via skill `atomizar-juridico`.

Reaproveita o extractor genérico de leis nacionais (LeiNacionalLocalExtractor),
já validado em Direito Internacional e Direito Previdenciário.

Uso:
    python pipeline_direito_digital.py              # 5 primeiros artigos de cada lei (teste)
    python pipeline_direito_digital.py --full       # todos os artigos
    python pipeline_direito_digital.py --limit 20   # primeiros N artigos de cada lei
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

from config_direito_digital import OUTPUT_BASE, LEIS_NACIONAIS
from direito_internacional_extractor import LeiNacionalLocalExtractor
from markdown_generator_dd import MarkdownGeneratorDD


def pipeline_dd(limit=None):
    sep = "=" * 60
    print(f"\n{sep}")
    print("PIPELINE DIREITO DIGITAL: HTML local -> Markdown")
    print(f"{sep}\n")

    gerador = MarkdownGeneratorDD(OUTPUT_BASE)
    total_salvos = 0
    total_erros = 0

    for sigla, cfg in LEIS_NACIONAIS.items():
        print(f"--- {sigla}: {cfg['nome']} (Lei {cfg['lei_numero']}) ---")
        extractor = LeiNacionalLocalExtractor(cfg["arquivo"], cfg["categoria"], cfg["max_artigo"])
        artigos = extractor.extract_articles()

        if not artigos:
            print(f"  AVISO: nenhum artigo extraído de {sigla}, pulando.\n")
            continue

        if limit:
            artigos = artigos[:limit]
            print(f"  Limitado a {limit} artigos para teste")

        salvos = 0
        erros = 0
        for art in artigos:
            try:
                conteudo = gerador.gerar_nota_artigo(art, cfg, sigla)
                filepath = gerador.salvar_artigo(art, conteudo, sigla)
                if filepath:
                    salvos += 1
            except Exception:
                erros += 1
                continue

        print(f"  {salvos} artigos salvos, {erros} erros\n")
        total_salvos += salvos
        total_erros += erros

    print(f"{sep}")
    print("PIPELINE DIREITO DIGITAL CONCLUIDO!")
    print(f"{sep}")
    print(f"\nESTATISTICAS GERAIS:")
    print(f"  Total salvos : {total_salvos}")
    print(f"  Total erros  : {total_erros}")
    print(f"\n  Saida: {OUTPUT_BASE}\n")
    return total_salvos > 0


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Pipeline Direito Digital: HTML local -> Markdown"
    )
    parser.add_argument("--full", action="store_true",
                        help="Gerar todos os artigos")
    parser.add_argument("--limit", type=int, default=5,
                        help="Numero maximo de artigos por lei (padrao: 5)")

    args = parser.parse_args()
    limit_artigos = None if args.full else args.limit

    sucesso = pipeline_dd(limit=limit_artigos)
    sys.exit(0 if sucesso else 1)

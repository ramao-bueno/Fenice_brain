#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pipeline CC: PDF Código Civil → Markdown estruturado

Reutiliza pdf_extractor e markdown_generator com config_cc

Uso:
    python pipeline_cc.py                 # 10 primeiros artigos (teste)
    python pipeline_cc.py --full          # Todos os artigos
    python pipeline_cc.py --limit 50      # Primeiros 50
"""

import sys
from pathlib import Path

# Importa config CC
from config_cc import PDF_PATH, OUTPUT_BASE, LIVRO_MAPEAMENTO, LEI_NUMERO, LEI_NOME

# Reutiliza extrator e gerador
from pdf_extractor import CPCExtractor
from markdown_generator import MarkdownGenerator

# Override LIVRO_MAPEAMENTO no extrator
import pdf_extractor as px_module
px_module.LIVRO_MAPEAMENTO = LIVRO_MAPEAMENTO

def pipeline_cc(limit=None):
    """Pipeline específico para Código Civil."""

    print("\n" + "="*60)
    print("🔄  PIPELINE CC: PDF → Markdown")
    print("="*60 + "\n")

    # Extrai
    print("📖 ETAPA 1: Extraindo artigos do PDF...")
    extractor = CPCExtractor(str(PDF_PATH))
    artigos = extractor.extract_articles()

    if not artigos:
        print("❌ Nenhum artigo extraído! Abortar.")
        return False

    if limit:
        artigos = artigos[:limit]
        print(f"⚠️  Limitado a {limit} artigos para teste")

    print(f"✅ {len(artigos)} artigos prontos para processar\n")

    # Gera Markdown
    print("📝 ETAPA 2: Gerando notas Markdown...")
    gerador = MarkdownGenerator(OUTPUT_BASE)

    artigos_salvos = 0
    artigos_errados = 0

    for i, art in enumerate(artigos, 1):
        try:
            conteudo = gerador.gerar_nota_artigo(art, art["livro"])
            filepath = gerador.salvar_artigo(art, conteudo, art["livro"])

            if filepath:
                artigos_salvos += 1

            if i % 100 == 0 or i == len(artigos):
                percentual = (i / len(artigos)) * 100
                print(f"   ✅ {i:>4d}/{len(artigos)} artigos processados ({percentual:.0f}%)")

        except Exception as e:
            artigos_errados += 1
            continue

    print(f"\n{'='*60}")
    print(f"✅ PIPELINE CC CONCLUÍDO!")
    print(f"{'='*60}")
    print(f"\n📊 ESTATÍSTICAS:")
    print(f"   • Artigos extraídos: {len(artigos)}")
    print(f"   • Artigos salvos: {artigos_salvos}")
    print(f"   • Erros: {artigos_errados}")
    print(f"   • Taxa sucesso: {(artigos_salvos/len(artigos)*100):.1f}%")
    print(f"\n📁 Local de saída:")
    print(f"   {OUTPUT_BASE}\n")

    return artigos_salvos > 0


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Pipeline CC: PDF → Markdown")
    parser.add_argument("--full", action="store_true", help="Gerar todos os artigos")
    parser.add_argument("--limit", type=int, default=10, help="Número máximo de artigos (padrão: 10)")

    args = parser.parse_args()

    limit_artigos = None if args.full else args.limit

    sucesso = pipeline_cc(limit=limit_artigos)

    sys.exit(0 if sucesso else 1)

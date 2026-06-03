#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pipeline completo: PDF → Extração → Geração Markdown

Uso:
    python main_pipeline.py                 # 10 primeiros artigos (teste)
    python main_pipeline.py --full          # 1.072 artigos (completo)
    python main_pipeline.py --limit 50      # Primeiros 50 artigos
"""

import sys
from pathlib import Path
from pdf_extractor import CPCExtractor
from markdown_generator import MarkdownGenerator
from config import PDF_PATH, OUTPUT_BASE

def pipeline_completo(limit=None):
    """Executa pipeline de extração + geração."""

    print("\n" + "="*60)
    print("🔄  PIPELINE CPC: PDF → Markdown")
    print("="*60 + "\n")

    # Passo 1: Extrai
    print("📖 ETAPA 1: Extraindo artigos do PDF...")
    extractor = CPCExtractor(str(PDF_PATH))
    artigos = extractor.extract_articles()

    if not artigos:
        print("❌ Nenhum artigo extraído! Abortar.")
        return False

    # Limita se pedido
    if limit:
        artigos = artigos[:limit]
        print(f"⚠️  Limitado a {limit} artigos para teste")

    print(f"✅ {len(artigos)} artigos prontos para processar\n")

    # Passo 2: Gera Markdown
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

            # Progresso a cada 50
            if i % 50 == 0 or i == len(artigos):
                percentual = (i / len(artigos)) * 100
                print(f"   ✅ {i:>4d}/{len(artigos)} artigos processados ({percentual:.0f}%)")

        except Exception as e:
            artigos_errados += 1
            print(f"   ⚠️  Erro ao processar Art. {art['numero']}: {e}")
            continue

    print(f"\n{'='*60}")
    print(f"✅ PIPELINE CONCLUÍDO!")
    print(f"{'='*60}")
    print(f"\n📊 ESTATÍSTICAS:")
    print(f"   • Artigos extraídos: {len(artigos)}")
    print(f"   • Artigos salvos: {artigos_salvos}")
    print(f"   • Erros: {artigos_errados}")
    print(f"   • Taxa sucesso: {(artigos_salvos/len(artigos)*100):.1f}%")
    print(f"\n📁 Local de saída:")
    print(f"   {OUTPUT_BASE}")
    print()

    return artigos_salvos > 0


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Pipeline CPC: PDF → Markdown")
    parser.add_argument("--full", action="store_true", help="Gerar todos 1.072 artigos")
    parser.add_argument("--limit", type=int, default=10, help="Número máximo de artigos (padrão: 10)")

    args = parser.parse_args()

    # Define limite
    limit_artigos = None if args.full else args.limit

    # Executa
    sucesso = pipeline_completo(limit=limit_artigos)

    # Exit code
    sys.exit(0 if sucesso else 1)

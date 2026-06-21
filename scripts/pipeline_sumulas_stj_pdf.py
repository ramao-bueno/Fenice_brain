#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pipeline Súmulas STJ via PDF — lê VerbetesSTJ.pdf → gera markdown no vault."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from extrator_pdf_sumulas_stj import extrair_sumulas_pdf, PDF_PATH
from markdown_generator_sumulas_stj import MarkdownGeneratorSumulaSTJ

OUTPUT_BASE = Path(__file__).parent.parent / "00_APEX" / "SUMULAS STJ" / "Sumulas"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    print("=" * 70)
    print("PIPELINE SÚMULAS STJ — FONTE: PDF")
    print("=" * 70)
    print()

    if not PDF_PATH.exists():
        print(f"❌ PDF não encontrado: {PDF_PATH}")
        return

    print(f"📄 Lendo PDF: {PDF_PATH.name}...")
    sumulas = extrair_sumulas_pdf(PDF_PATH)

    if not sumulas:
        print("⚠️  Nenhuma súmula extraída")
        return

    print(f"✅ Extraídas: {len(sumulas)} súmulas (STJ {sumulas[0]['numero']}–{sumulas[-1]['numero']})")
    print()
    print("📝 Gerando notas markdown...")

    OUTPUT_BASE.mkdir(parents=True, exist_ok=True)
    gen = MarkdownGeneratorSumulaSTJ(OUTPUT_BASE)
    salves = 0

    for sumula in sumulas:
        conteudo = gen.gerar_nota_sumula(sumula)
        resultado = gen.salvar_sumula(sumula, conteudo)
        if resultado:
            salves += 1

    print(f"✅ Salvas: {salves}/{len(sumulas)} notas")
    print(f"📁 Output: {OUTPUT_BASE}")
    print()
    print("=" * 70)


if __name__ == "__main__":
    main()

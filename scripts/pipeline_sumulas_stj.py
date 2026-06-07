#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pipeline completo Súmulas STJ: lê HTML SCON → gera markdown → salva no vault."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from config_sumulas_stj import OUTPUT_BASE, HTML_SOURCE
from extrator_html_sumulas_stj import extrair_sumulas_stj
from markdown_generator_sumulas_stj import MarkdownGeneratorSumulaSTJ


def processar_sumulas() -> int:
    """Processa todas as súmulas."""
    if not HTML_SOURCE.exists():
        print("❌ Arquivo HTML não encontrado!")
        print()
        print("INSTRUÇÕES para adicionar Súmulas STJ:")
        print("=" * 70)
        print()
        print("1. Abra no navegador:")
        print("   https://scon.stj.jus.br/SCON/sumulas/toc.jsp?b=SUMU")
        print()
        print("2. Salve a página (Ctrl+S ou Cmd+S):")
        print("   - Nome: _stj_sumulas_page.html")
        print("   - Local: scripts/")
        print()
        print("3. Rode novamente:")
        print("   python pipeline_sumulas_stj.py")
        print()
        print("=" * 70)
        return 0

    print(f"📄 Lendo HTML: {HTML_SOURCE.name}...")
    sumulas = extrair_sumulas_stj(HTML_SOURCE)

    if not sumulas:
        print("⚠️  nenhuma súmula extraída")
        print()
        print("Possível causa: formato HTML diferente do esperado")
        print("Verifique se salvou a página corretamente.")
        return 0

    print(f"✅ Extraído {len(sumulas)} súmulas")
    print()
    print("📝 Gerando markdown...")

    # Gera notas markdown
    gen = MarkdownGeneratorSumulaSTJ(OUTPUT_BASE)
    salves = 0

    for sumula in sumulas:
        conteudo = gen.gerar_nota_sumula(sumula)
        resultado = gen.salvar_sumula(sumula, conteudo)
        if resultado:
            salves += 1

    print(f"✅ {salves}/{len(sumulas)} súmulas salvas")
    return salves


def main():
    print("=" * 70)
    print("PIPELINE SÚMULAS STJ")
    print("=" * 70)
    print()

    # Cria pasta de output
    OUTPUT_BASE.mkdir(parents=True, exist_ok=True)

    salves = processar_sumulas()

    print()
    print("=" * 70)
    if salves > 0:
        print(f"Total de súmulas salvos: {salves}")
        print(f"Output: {OUTPUT_BASE}")
    print("=" * 70)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()

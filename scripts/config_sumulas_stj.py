"""
Config Súmulas STJ — jurisprudência consolidada do Superior Tribunal de Justiça
extraídas do HTML do SCON (Sistema de Consultas) salvo manualmente.

Composição:
- ~670 Súmulas STJ (STJ 1-670)
- Fonte: https://scon.stj.jus.br/SCON/sumulas/

Status: AGUARDANDO DADOS
Instruções: Salve o HTML do SCON conforme descrito em INDEX-Sumulas-STJ.md
"""
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
FENICE_BASE = PROJECT_ROOT / "Fenice bRain"
SUMULAS_STJ_BASE = FENICE_BASE / "03_PROCESSO_CIVIL" / "STF_SUMULAS" / "STJ"
OUTPUT_BASE = SUMULAS_STJ_BASE / "Sumulas"
HTML_SOURCE = Path(__file__).parent / "_stj_sumulas_page.html"

TAGS_PADRAO = ["sumula-stj", "jurisprudencia", "stj"]

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    print("Config Súmulas STJ carregado")
    print(f"  Output: {OUTPUT_BASE}")
    print(f"  Fonte HTML esperada: {HTML_SOURCE}")
    print()
    if HTML_SOURCE.exists():
        print("✅ HTML disponível — execute pipeline_sumulas_stj.py")
    else:
        print("⏳ HTML não encontrado — siga instruções:")
        print("   1. Acesse: https://scon.stj.jus.br/SCON/sumulas/toc.jsp?b=SUMU")
        print("   2. Salve a página: Ctrl+S")
        print(f"   3. Coloque em: {HTML_SOURCE}")
        print("   4. Execute: python pipeline_sumulas_stj.py")

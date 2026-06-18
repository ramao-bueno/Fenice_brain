"""
Config Código de Processo Civil — leis de procedimento civil
extraídas localmente dos HTMLs já salvos do Planalto.

Composição:
- L13105 (2015) — Código de Processo Civil (novo) — ~1.072 artigos
- L10259 (1990) — Código de Processo Civil (antigo) — ~506 artigos (para referência histórica)
"""
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
FENICE_BASE = PROJECT_ROOT / "Fenice bRain"
CPC_BASE = FENICE_BASE / "03_PROCESSO_CIVIL" / "CÓDIGO_PROCESSO_CIVIL"
OUTPUT_BASE = CPC_BASE / "Artigos"

LEIS_NACIONAIS = {
    "L13105": {
        "arquivo": CPC_BASE / "L13105.html",
        "nome": "Código de Processo Civil",
        "lei_numero": "13.105/2015",
        "categoria": "CODIGO_PROCESSO_CIVIL",
        "max_artigo": 1072,
        "tema": "processo-civil",
    },
    "L10259": {
        "arquivo": CPC_BASE / "L10259.html",
        "nome": "Código de Processo Civil (revogado)",
        "lei_numero": "10.259/1990",
        "categoria": "CODIGO_PROCESSO_CIVIL_ANTIGO",
        "max_artigo": 506,
        "tema": "processo-civil",
    },
}

TAGS_PADRAO = ["processo-civil", "vigente"]

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    print("Config Código de Processo Civil carregado")
    print(f"  Output: {OUTPUT_BASE}")
    total_artigos = 0
    for sigla, cfg in LEIS_NACIONAIS.items():
        total = cfg["max_artigo"]
        total_artigos += total
        status = "VIGENTE" if "13105" in sigla else "REVOGADO"
        print(f"  {sigla}: {cfg['nome']} ({cfg['lei_numero']}) — até Art. {total} [{status}]")
    print(f"  Total estimado: {total_artigos} artigos")

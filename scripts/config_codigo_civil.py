"""
Config Código Civil — leis nacionais com numeração padrão (Art. N)
extraídas localmente dos HTMLs já salvos do Planalto.

Composição:
- L10406 (2002) — Código Civil (2.046 artigos)
- D9830 (1994) — Decreto de Introdução ao CC (21 artigos)
- L13655 (2018) — Lei de Introdução às Normas do Direito Brasileiro (30 artigos)
"""
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
FENICE_BASE = PROJECT_ROOT / "01_PRIVADO" / "Codigos" / "CC"
CC_BASE = FENICE_BASE

# HTMLs baixados via scripts/baixar_fontes.py
FONTES_BASE = Path(__file__).parent / "fontes"
CC_FONTES = FONTES_BASE / "cc"

OUTPUT_BASE = FENICE_BASE

LEIS_NACIONAIS = {
    "L10406": {
        "arquivo": CC_FONTES / "L10406.html",
        "nome": "Código Civil",
        "lei_numero": "10.406/2002",
        "categoria": "CODIGO_CIVIL",
        "max_artigo": 2046,
        "tema": "direito-civil",
    },
    "D9830": {
        "arquivo": CC_FONTES / "D9830.html",
        "nome": "Decreto de Introdução ao Código Civil",
        "lei_numero": "Dec. 9.830/1994",
        "categoria": "DECRETO_INTRODUCAO",
        "max_artigo": 21,
        "tema": "direito-civil",
    },
    "L13655": {
        "arquivo": CC_FONTES / "L13655.html",
        "nome": "Lei de Introdução às Normas do Direito Brasileiro",
        "lei_numero": "13.655/2018",
        "categoria": "LEI_INTRODUCAO",
        "max_artigo": 30,
        "tema": "direito-civil",
    },
}

TAGS_PADRAO = ["codigo-civil", "vigente"]

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    print("Config Código Civil carregado")
    print(f"  Output: {OUTPUT_BASE}")
    total_artigos = 0
    for sigla, cfg in LEIS_NACIONAIS.items():
        total = cfg["max_artigo"]
        total_artigos += total
        print(f"  {sigla}: {cfg['nome']} ({cfg['lei_numero']}) — até Art. {total}")
    print(f"  Total estimado: {total_artigos} artigos")

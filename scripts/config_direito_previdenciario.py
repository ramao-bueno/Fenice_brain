"""
Config Direito Previdenciário — leis nacionais com numeração padrão (Art. N)
extraídas localmente dos HTMLs já salvos do Planalto.

As "leis gêmeas" de 1991 — custeio (8.212) e benefícios (8.213) — formam o
núcleo do Direito Previdenciário brasileiro.
"""
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
FENICE_BASE = PROJECT_ROOT / "05_ESPECIAL" / "Codigos"
DP_BASE = FENICE_BASE / "DIREITO_PREVIDENCIARIO"
OUTPUT_BASE = DP_BASE / "Artigos"

FONTES_BASE = Path(__file__).parent / "fontes"
DP_FONTES = FONTES_BASE / "especial"

LEIS_NACIONAIS = {
    "L8212": {
        "arquivo": DP_FONTES / "L8212.html",
        "nome": "Lei Orgânica da Seguridade Social (Custeio)",
        "lei_numero": "8.212/1991",
        "categoria": "CUSTEIO",
        "max_artigo": 105,
        "tema": "custeio-da-seguridade-social",
    },
    "L8213": {
        "arquivo": DP_FONTES / "L8213.html",
        "nome": "Lei dos Planos de Benefícios da Previdência Social",
        "lei_numero": "8.213/1991",
        "categoria": "BENEFICIOS",
        "max_artigo": 156,
        "tema": "beneficios-previdenciarios",
    },
}

TAGS_PADRAO = ["direito-previdenciario", "vigente"]

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    print("Config Direito Previdenciário carregado")
    print(f"  Output: {OUTPUT_BASE}")
    for sigla, cfg in LEIS_NACIONAIS.items():
        print(f"  {sigla}: {cfg['nome']} ({cfg['lei_numero']}) — até Art. {cfg['max_artigo']}")

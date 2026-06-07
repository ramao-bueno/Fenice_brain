"""
Config Código Penal — leis penais materiais
extraídas localmente dos HTMLs já salvos do Planalto.

Composição:
- DEL2848 (1940) — Código Penal (302 artigos)
- L7492 (1986) — Lei dos Crimes Contra o Sistema Financeiro
- L8072 (1990) — Lei de Crimes Hediondos
- L8137 (1990) — Lei de Crimes Contra a Ordem Tributária
- L9605 (1998) — Lei de Crimes Ambientais
- L9613 (1998) — Lei de Lavagem de Dinheiro
- L14132 (2021) — Lei de Reforma Penal
- L14155 (2021) — Lei de Reforma Penal
- L14811 (2024) — Lei de Reforma Penal
- L15384 (2024) — Lei de Reforma Penal
- L11343 (2006) — Lei de Drogas
- L12850 (2013) — Lei de Drogas (revogou L11343)
"""
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
FENICE_BASE = PROJECT_ROOT / "FENICE bRain"
CP_BASE = FENICE_BASE / "04_DIREITO_PENAL" / "CÓDIGO_PENAL"
OUTPUT_BASE = CP_BASE / "Artigos"

LEIS_NACIONAIS = {
    "DEL2848": {
        "arquivo": CP_BASE / "DEL2848.html",
        "nome": "Código Penal",
        "lei_numero": "DL 2.848/1940",
        "categoria": "CODIGO_PENAL",
        "max_artigo": 302,
        "tema": "direito-penal",
    },
    "L7492": {
        "arquivo": CP_BASE / "L7492.html",
        "nome": "Lei de Crimes Contra o Sistema Financeiro",
        "lei_numero": "7.492/1986",
        "categoria": "CRIMES_FINANCEIROS",
        "max_artigo": 20,
        "tema": "direito-penal",
    },
    "L8072": {
        "arquivo": CP_BASE / "L8072.html",
        "nome": "Lei de Crimes Hediondos",
        "lei_numero": "8.072/1990",
        "categoria": "CRIMES_HEDIONDOS",
        "max_artigo": 10,
        "tema": "direito-penal",
    },
    "L8137": {
        "arquivo": CP_BASE / "L8137.html",
        "nome": "Lei de Crimes Contra a Ordem Tributária",
        "lei_numero": "8.137/1990",
        "categoria": "CRIMES_TRIBUTARIOS",
        "max_artigo": 16,
        "tema": "direito-penal",
    },
    "L9605": {
        "arquivo": CP_BASE / "L9605.html",
        "nome": "Lei de Crimes Ambientais",
        "lei_numero": "9.605/1998",
        "categoria": "CRIMES_AMBIENTAIS",
        "max_artigo": 80,
        "tema": "direito-penal",
    },
    "L9613": {
        "arquivo": CP_BASE / "L9613.html",
        "nome": "Lei de Lavagem de Dinheiro",
        "lei_numero": "9.613/1998",
        "categoria": "LAVAGEM_DINHEIRO",
        "max_artigo": 25,
        "tema": "direito-penal",
    },
    "L14132": {
        "arquivo": CP_BASE / "L14132.html",
        "nome": "Lei de Reforma Penal",
        "lei_numero": "14.132/2021",
        "categoria": "REFORMA_PENAL",
        "max_artigo": 30,
        "tema": "direito-penal",
    },
    "L14155": {
        "arquivo": CP_BASE / "L14155.html",
        "nome": "Lei de Reforma Penal",
        "lei_numero": "14.155/2021",
        "categoria": "REFORMA_PENAL",
        "max_artigo": 15,
        "tema": "direito-penal",
    },
    "L14811": {
        "arquivo": CP_BASE / "L14811.html",
        "nome": "Lei de Reforma Penal (Segurança Pública)",
        "lei_numero": "14.811/2024",
        "categoria": "REFORMA_PENAL",
        "max_artigo": 20,
        "tema": "direito-penal",
    },
    "L15384": {
        "arquivo": CP_BASE / "L15384.html",
        "nome": "Lei de Reforma Penal (Drogas/Segurança)",
        "lei_numero": "15.384/2024",
        "categoria": "REFORMA_PENAL",
        "max_artigo": 20,
        "tema": "direito-penal",
    },
    "L11343": {
        "arquivo": CP_BASE / "Lei nº 11.343.html",
        "nome": "Lei de Drogas (revogada)",
        "lei_numero": "11.343/2006",
        "categoria": "LEI_DROGAS",
        "max_artigo": 80,
        "tema": "direito-penal",
    },
}

TAGS_PADRAO = ["direito-penal", "vigente"]

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    print("Config Código Penal carregado")
    print(f"  Output: {OUTPUT_BASE}")
    total_artigos = 0
    for sigla, cfg in LEIS_NACIONAIS.items():
        total = cfg["max_artigo"]
        total_artigos += total
        print(f"  {sigla}: {cfg['nome']} ({cfg['lei_numero']}) — até Art. {total}")
    print(f"  Total estimado: {total_artigos} artigos")

"""
Config Direito Internacional — leis nacionais com numeração padrão (Art. N)
extraídas localmente dos HTMLs já salvos do Planalto.

Tratados/decretos internacionais (numeração ARTIGO/Artigo, formatos variados)
NÃO entram aqui — são processados via skill `atomizar-juridico` (ver README
da pasta DIREITO_INTERNACIONAL).
"""
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
FENICE_BASE = PROJECT_ROOT / "FENICE bRain"
DI_BASE = FENICE_BASE / "08_DIREITOS_ESPECIALIZADOS" / "DIREITO_INTERNACIONAL"
OUTPUT_BASE = DI_BASE / "Artigos"

# Leis nacionais com padrão "Art. N" — compatíveis com o extractor por regex
LEIS_NACIONAIS = {
    "L9307": {
        "arquivo": DI_BASE / "L9307.html",
        "nome": "Lei de Arbitragem",
        "lei_numero": "9.307/1996",
        "categoria": "ARBITRAGEM",
        "max_artigo": 44,
        "tema": "arbitragem-internacional",
    },
    "L13445": {
        "arquivo": DI_BASE / "L13445.html",
        "nome": "Lei de Migração",
        "lei_numero": "13.445/2017",
        "categoria": "MIGRACAO",
        "max_artigo": 125,
        "tema": "migracao-e-nacionalidade",
    },
}

TAGS_PADRAO = ["direito-internacional", "vigente"]
PLANALTO_BASE_URL = "https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2017/lei/l13445.htm"

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    print(f"Config Direito Internacional carregado")
    print(f"  Output: {OUTPUT_BASE}")
    for sigla, cfg in LEIS_NACIONAIS.items():
        print(f"  {sigla}: {cfg['nome']} ({cfg['lei_numero']}) — até Art. {cfg['max_artigo']}")

"""
Config Direito Digital — leis nacionais com numeração padrão (Art. N)
extraídas localmente dos HTMLs já salvos do Planalto.

Leis "modificativas" (L12737 — Lei Carolina Dieckmann, L14155 — estelionato
digital) NÃO entram aqui — têm só 2-4 artigos "invólucro" que inserem tipos
penais (Art. 154-A, 171 §2º-A) no Código Penal; são processadas via skill
`atomizar-juridico` (ver README/INDEX da pasta).
"""
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
FENICE_BASE = PROJECT_ROOT / "Fenice bRain"
DD_BASE = FENICE_BASE / "08_DIREITOS_ESPECIALIZADOS" / "DIREITO_DIGITAL"
OUTPUT_BASE = DD_BASE / "Artigos"

LEIS_NACIONAIS = {
    "L12965": {
        "arquivo": DD_BASE / "L12965.html",
        "nome": "Marco Civil da Internet",
        "lei_numero": "12.965/2014",
        "categoria": "MARCO_CIVIL",
        "max_artigo": 32,
        "tema": "direitos-e-garantias-na-internet",
    },
    "L13709": {
        "arquivo": DD_BASE / "L13709.html",
        "nome": "Lei Geral de Proteção de Dados (LGPD)",
        "lei_numero": "13.709/2018",
        "categoria": "PROTECAO_DE_DADOS",
        "max_artigo": 65,
        "tema": "protecao-de-dados-pessoais",
    },
    "L9609": {
        "arquivo": DD_BASE / "L9609.html",
        "nome": "Lei do Software",
        "lei_numero": "9.609/1998",
        "categoria": "PROPRIEDADE_INTELECTUAL",
        "max_artigo": 16,
        "tema": "protecao-de-programas-de-computador",
    },
    "L9610": {
        "arquivo": DD_BASE / "L9610.html",
        "nome": "Lei de Direitos Autorais",
        "lei_numero": "9.610/1998",
        "categoria": "PROPRIEDADE_INTELECTUAL",
        "max_artigo": 115,
        "tema": "direitos-autorais",
    },
}

TAGS_PADRAO = ["direito-digital", "vigente"]

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    print("Config Direito Digital carregado")
    print(f"  Output: {OUTPUT_BASE}")
    for sigla, cfg in LEIS_NACIONAIS.items():
        print(f"  {sigla}: {cfg['nome']} ({cfg['lei_numero']}) — até Art. {cfg['max_artigo']}")

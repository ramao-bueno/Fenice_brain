from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
PDF_PATH = PROJECT_ROOT / "00_APEX" / "CONSTITUIÇÃO_FEDERAL" / "Constituição.pdf"
OUTPUT_BASE = PROJECT_ROOT / "00_APEX" / "CONSTITUIÇÃO_FEDERAL" / "Artigos"

TITULO_MAPEAMENTO = {
    "TITULO-I":    {"range": (1,   4),   "nome": "Dos Princípios Fundamentais"},
    "TITULO-II":   {"range": (5,   17),  "nome": "Dos Direitos e Garantias Fundamentais"},
    "TITULO-III":  {"range": (18,  43),  "nome": "Da Organização do Estado"},
    "TITULO-IV":   {"range": (44,  135), "nome": "Da Organização dos Poderes"},
    "TITULO-V":    {"range": (136, 144), "nome": "Da Defesa do Estado e das Instituições Democráticas"},
    "TITULO-VI":   {"range": (145, 169), "nome": "Da Tributação e do Orçamento"},
    "TITULO-VII":  {"range": (170, 192), "nome": "Da Ordem Econômica e Financeira"},
    "TITULO-VIII": {"range": (193, 232), "nome": "Da Ordem Social"},
    "TITULO-IX":   {"range": (233, 250), "nome": "Das Disposições Constitucionais Gerais"},
}

TEMA_POR_TITULO = {
    "TITULO-I":    "principios-fundamentais",
    "TITULO-II":   "direitos-fundamentais",
    "TITULO-III":  "organizacao-estado",
    "TITULO-IV":   "organizacao-poderes",
    "TITULO-V":    "defesa-estado",
    "TITULO-VI":   "tributacao",
    "TITULO-VII":  "ordem-economica",
    "TITULO-VIII": "ordem-social",
    "TITULO-IX":   "disposicoes-gerais",
}

TAGS_PADRAO = ["cf88", "constituicao", "vigente"]

LEI_NOME = "Constituição Federal de 1988"
LEI_NUMERO = "CF/88"
LEI_ANO = 1988
PLANALTO_BASE_URL = "https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm"

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    print(f"Config CF/88 carregado")
    print(f"  PDF existe: {PDF_PATH.exists()}")
    print(f"  Output: {OUTPUT_BASE}")
    print(f"  Titulos: {len(TITULO_MAPEAMENTO)}")

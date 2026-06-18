"""
Config Direito Administrativo — leis nacionais com numeração padrão (Art. N)
extraídas localmente dos HTMLs já salvos do Planalto.

Foco nas 4 leis de maior densidade de litígio/compliance: Improbidade,
Processo Administrativo Federal, Anticorrupção e Acesso à Informação.
(Estatuto dos Servidores e Nova Lei de Licitações ficam para rodada futura —
volume muito maior, ~250 e ~194 artigos respectivamente.)
"""
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
FENICE_BASE = PROJECT_ROOT / "Fenice bRain"
DA_BASE = FENICE_BASE / "07_DIREITO_ADMINISTRATIVO" / "DIREITO_ADMINISTRATIVO"
OUTPUT_BASE = DA_BASE / "Artigos"

LEIS_NACIONAIS = {
    "L8429": {
        "arquivo": DA_BASE / "L8429.html",
        "nome": "Lei de Improbidade Administrativa",
        "lei_numero": "8.429/1992",
        "categoria": "IMPROBIDADE",
        "max_artigo": 25,
        "tema": "improbidade-administrativa",
    },
    "L9784": {
        "arquivo": DA_BASE / "L9784.html",
        "nome": "Lei do Processo Administrativo Federal",
        "lei_numero": "9.784/1999",
        "categoria": "PROCESSO_ADMINISTRATIVO",
        "max_artigo": 70,
        "tema": "processo-administrativo",
    },
    "L12846": {
        "arquivo": DA_BASE / "L12846.html",
        "nome": "Lei Anticorrupção (Lei da Empresa Limpa)",
        "lei_numero": "12.846/2013",
        "categoria": "ANTICORRUPCAO",
        "max_artigo": 31,
        "tema": "responsabilizacao-de-pessoas-juridicas",
    },
    "L12527": {
        "arquivo": DA_BASE / "L12527.html",
        "nome": "Lei de Acesso à Informação (LAI)",
        "lei_numero": "12.527/2011",
        "categoria": "ACESSO_A_INFORMACAO",
        "max_artigo": 47,
        "tema": "transparencia-e-acesso-a-informacao",
    },
}

TAGS_PADRAO = ["direito-administrativo", "vigente"]

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    print("Config Direito Administrativo carregado")
    print(f"  Output: {OUTPUT_BASE}")
    for sigla, cfg in LEIS_NACIONAIS.items():
        print(f"  {sigla}: {cfg['nome']} ({cfg['lei_numero']}) — até Art. {cfg['max_artigo']}")

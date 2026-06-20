"""
Config Código de Processo Penal — leis de procedimento penal
extraídas localmente dos HTMLs já salvos do Planalto.

Composição:
- L13869 (2019) — Código de Processo Penal (possível lei de implementação/reforma)
- L13964 (2020) — Lei de reforma do CPP
- L7210 (1984) — Lei de Tortura
- L7960 (1989) — Lei de Habeas Corpus
- L9099 (1995) — Lei dos Juizados Especiais Criminais
- L11340 (2006) — Lei Maria da Penha
- L12850 (2013) — Lei de Drogas (Tráfico vs. Usuário)

Nota: CPP principal é o Decreto-Lei 3.689/1941, mas não há HTML salvo.
"""
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
FENICE_BASE = PROJECT_ROOT / "02_PENAL" / "Codigos" / "CPP"
CPP_BASE = FENICE_BASE
OUTPUT_BASE = CPP_BASE / "Artigos"

LEIS_NACIONAIS = {
    "L13869": {
        "arquivo": CPP_BASE / "L13869.html",
        "nome": "Lei de Reforma do Código de Processo Penal",
        "lei_numero": "13.869/2019",
        "categoria": "CODIGO_PROCESSO_PENAL",
        "max_artigo": 150,
        "tema": "processo-penal",
    },
    "L13964": {
        "arquivo": CPP_BASE / "L13964.html",
        "nome": "Lei de Reforma do Código de Processo Penal",
        "lei_numero": "13.964/2020",
        "categoria": "CODIGO_PROCESSO_PENAL",
        "max_artigo": 180,
        "tema": "processo-penal",
    },
    "L7210": {
        "arquivo": CPP_BASE / "L7210.html",
        "nome": "Lei contra a Tortura",
        "lei_numero": "7.210/1984",
        "categoria": "DIREITOS_HUMANOS",
        "max_artigo": 5,
        "tema": "direitos-humanos",
    },
    "L7960": {
        "arquivo": CPP_BASE / "L7960.html",
        "nome": "Lei do Habeas Corpus",
        "lei_numero": "7.960/1989",
        "categoria": "HABEAS_CORPUS",
        "max_artigo": 15,
        "tema": "processo-penal",
    },
    "L9099": {
        "arquivo": CPP_BASE / "L9099.html",
        "nome": "Lei dos Juizados Especiais Criminais",
        "lei_numero": "9.099/1995",
        "categoria": "JUIZADOS_ESPECIAIS",
        "max_artigo": 90,
        "tema": "processo-penal",
    },
    "L11340": {
        "arquivo": CPP_BASE / "Lei nº 11.340.html",
        "nome": "Lei Maria da Penha",
        "lei_numero": "11.340/2006",
        "categoria": "VIOLENCIA_DOMESTICA",
        "max_artigo": 46,
        "tema": "direitos-humanos",
    },
    "L12850": {
        "arquivo": CPP_BASE / "L12850.html",
        "nome": "Lei de Drogas (Tráfico vs. Usuário)",
        "lei_numero": "12.850/2013",
        "categoria": "LEI_DROGAS",
        "max_artigo": 50,
        "tema": "processo-penal",
    },
}

TAGS_PADRAO = ["processo-penal", "vigente"]

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    print("Config Código de Processo Penal carregado")
    print(f"  Output: {OUTPUT_BASE}")
    total_artigos = 0
    for sigla, cfg in LEIS_NACIONAIS.items():
        total = cfg["max_artigo"]
        total_artigos += total
        print(f"  {sigla}: {cfg['nome']} ({cfg['lei_numero']}) — até Art. {total}")
    print(f"  Total estimado: {total_artigos} artigos")

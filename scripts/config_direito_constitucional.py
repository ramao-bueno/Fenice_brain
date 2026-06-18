"""
Config Direito Constitucional — leis nacionais com numeração padrão (Art. N)
extraídas localmente dos HTMLs já salvos do Planalto.

O "kit completo de remédios e ações constitucionais": Mandado de Segurança,
Mandado de Injunção, Habeas Data, Ação Popular, ADI/ADC, ADPF, Súmula
Vinculante, regulamentação do plebiscito/referendo e técnica legislativa.

D678 (CADH) é duplicata do já atomizado em Direito Internacional — ignorado.
Decreto 6949 (Convenção sobre Pessoas com Deficiência) tem só 3 artigos no
texto local (decreto-wrapper) — candidato a atomização via skill no futuro.
"""
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
FENICE_BASE = PROJECT_ROOT / "Fenice bRain"
DC_BASE = FENICE_BASE / "00_ESTRUTURA_CONSTITUCIONAL" / "DIREITO_CONSTITUCIONAL"
OUTPUT_BASE = DC_BASE / "Artigos"

LEIS_NACIONAIS = {
    "L12016": {
        "arquivo": DC_BASE / "L12016.html",
        "nome": "Lei do Mandado de Segurança",
        "lei_numero": "12.016/2009",
        "categoria": "MANDADO_DE_SEGURANCA",
        "max_artigo": 29,
        "tema": "remedios-constitucionais",
    },
    "L13300": {
        "arquivo": DC_BASE / "L13300.html",
        "nome": "Lei do Mandado de Injunção",
        "lei_numero": "13.300/2016",
        "categoria": "MANDADO_DE_INJUNCAO",
        "max_artigo": 15,
        "tema": "remedios-constitucionais",
    },
    "L4717": {
        "arquivo": DC_BASE / "L4717.html",
        "nome": "Lei da Ação Popular",
        "lei_numero": "4.717/1965",
        "categoria": "ACAO_POPULAR",
        "max_artigo": 22,
        "tema": "remedios-constitucionais",
    },
    "L9507": {
        "arquivo": DC_BASE / "L9507.html",
        "nome": "Lei do Habeas Data",
        "lei_numero": "9.507/1997",
        "categoria": "HABEAS_DATA",
        "max_artigo": 23,
        "tema": "remedios-constitucionais",
    },
    "L9709": {
        "arquivo": DC_BASE / "L9709.html",
        "nome": "Lei do Plebiscito, Referendo e Iniciativa Popular",
        "lei_numero": "9.709/1998",
        "categoria": "DEMOCRACIA_DIRETA",
        "max_artigo": 15,
        "tema": "soberania-popular",
    },
    "L9868": {
        "arquivo": DC_BASE / "L9868.html",
        "nome": "Lei da ADI e ADC",
        "lei_numero": "9.868/1999",
        "categoria": "CONTROLE_CONCENTRADO",
        "max_artigo": 31,
        "tema": "controle-de-constitucionalidade",
    },
    "L9882": {
        "arquivo": DC_BASE / "L9882.html",
        "nome": "Lei da ADPF",
        "lei_numero": "9.882/1999",
        "categoria": "CONTROLE_CONCENTRADO",
        "max_artigo": 14,
        "tema": "controle-de-constitucionalidade",
    },
    "LCP95": {
        "arquivo": DC_BASE / "Lcp95.html",
        "nome": "Lei Complementar de Elaboração das Leis (técnica legislativa)",
        "lei_numero": "LC 95/1998",
        "categoria": "TECNICA_LEGISLATIVA",
        "max_artigo": 19,
        "tema": "processo-legislativo",
    },
    "L11417": {
        "arquivo": DC_BASE / "Lei nº 11.417.html",
        "nome": "Lei da Súmula Vinculante",
        "lei_numero": "11.417/2006",
        "categoria": "SUMULA_VINCULANTE",
        "max_artigo": 11,
        "tema": "uniformizacao-jurisprudencial",
    },
}

TAGS_PADRAO = ["direito-constitucional", "vigente"]

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    print("Config Direito Constitucional carregado")
    print(f"  Output: {OUTPUT_BASE}")
    for sigla, cfg in LEIS_NACIONAIS.items():
        print(f"  {sigla}: {cfg['nome']} ({cfg['lei_numero']}) — até Art. {cfg['max_artigo']}")

import os
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
PDF_PATH = r"C:\Users\oicon\OneDrive\Allah - Islamismo\Univille SFS\Stand Alone backup\BIBLIOTECA JURÍDICA\legislação\Código de Processo Civil – Lei nº 13.105-15.pdf"
OUTPUT_BASE = PROJECT_ROOT / "FENICE bRain" / "05_CÓDIGO_PROCESSO_CIVIL" / "Artigos"

# Mapeamento de Livros
LIVRO_MAPEAMENTO = {
    "LIVRO-I": {"range": (1, 102), "nome": "Normas Processuais Civis"},
    "LIVRO-II": {"range": (203, 577), "nome": "Processo de Conhecimento"},
    "LIVRO-III": {"range": (513, 780), "nome": "Processo de Execução"},
    "LIVRO-IV": {"range": (581, 702), "nome": "Procedimentos Especiais"},
    "LIVRO-V": {"range": (994, 1029), "nome": "Recursos"},
}

# Tags padrão
TAGS_PADRAO = ["cpc", "processo-civil", "vigente"]

# Metadata
LEI_NUMERO = "13.105"
LEI_ANO = 2015
LEI_NOME = "Lei 13.105/2015 (Código de Processo Civil)"

if __name__ == "__main__":
    print(f"✅ Config carregado")
    print(f"   PDF: {PDF_PATH.exists()}")
    print(f"   Output: {OUTPUT_BASE}")

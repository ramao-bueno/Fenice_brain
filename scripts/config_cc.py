import os
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
PDF_PATH = r"C:\Users\oicon\OneDrive\Allah - Islamismo\Univille SFS\BIBLIOTECA JURIDICA\Codigo Civil\L10406.pdf"
OUTPUT_BASE = PROJECT_ROOT / "FENICE bRain" / "02_DIREITO_PRIVADO" / "DIREITO_CIVIL" / "Artigos"

# Mapeamento de Livros (Código Civil tem 2.046 artigos)
LIVRO_MAPEAMENTO = {
    "LIVRO-I": {"range": (1, 232), "nome": "Parte Geral"},
    "LIVRO-II": {"range": (233, 709), "nome": "Direito das Obrigações"},
    "LIVRO-III": {"range": (710, 1256), "nome": "Direito das Coisas"},
    "LIVRO-IV": {"range": (1257, 1638), "nome": "Direito de Família"},
    "LIVRO-V": {"range": (1639, 2046), "nome": "Direito das Sucessões"},
}

# Tags padrão
TAGS_PADRAO = ["cc", "direito-civil", "vigente"]

# Metadata
LEI_NUMERO = "10.406"
LEI_ANO = 2002
LEI_NOME = "Lei 10.406/2002 (Código Civil)"

if __name__ == "__main__":
    print(f"✅ Config CC carregado")
    print(f"   PDF: {PDF_PATH.exists()}")
    print(f"   Output: {OUTPUT_BASE}")

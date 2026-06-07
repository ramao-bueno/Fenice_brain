import os
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
OUTPUT_BASE = PROJECT_ROOT / "FENICE bRain" / "08_CÓDIGO_CONSUMIDOR" / "Artigos"

# Mapeamento de Livros (CDC tem 119 artigos)
LIVRO_MAPEAMENTO = {
    "LIVRO-I": {"range": (1, 59), "nome": "Direitos do Consumidor"},
    "LIVRO-II": {"range": (60, 78), "nome": "Infrações Penais"},
    "LIVRO-III": {"range": (79, 105), "nome": "Processo Administrativo"},
    "DISPOSICOES-GERAIS": {"range": (106, 119), "nome": "Disposições Gerais"},
}

# Tags padrão
TAGS_PADRAO = ["cdc", "direito-do-consumidor", "lei-8078", "vigente"]

# Metadata
LEI_NUMERO = "8.078"
LEI_ANO = 1990
LEI_NOME = "Lei 8.078/1990 (Código do Consumidor)"

if __name__ == "__main__":
    print(f"✅ Config CDC carregado")
    print(f"   Output: {OUTPUT_BASE}")

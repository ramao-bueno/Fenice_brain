import os
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
OUTPUT_BASE = PROJECT_ROOT / "Fenice bRain" / "02_DIREITO_PRIVADO" / "CÓDIGO_CONSUMIDOR" / "Artigos"

# Mapeamento de Livros (CDC tem 119 artigos)
LIVRO_MAPEAMENTO = {
    "LIVRO-I": {"range": (1, 8), "nome": "Das Disposições Gerais"},
    "LIVRO-II": {"range": (9, 108), "nome": "Da Proteção ao Consumidor"},
    "LIVRO-III": {"range": (109, 119), "nome": "Da Defesa do Consumidor em Juízo"},
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

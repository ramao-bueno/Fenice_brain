import os
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
OUTPUT_BASE = PROJECT_ROOT / "01_PRIVADO" / "Codigos" / "CPC" / "CÓDIGO_PROCESSO_CIVIL" / "Artigos"

# Mapeamento de Livros (CPC tem 1072 artigos)
LIVRO_MAPEAMENTO = {
    "LIVRO-I": {"range": (1, 102), "nome": "Normas Processuais Civis"},
    "LIVRO-II": {"range": (103, 502), "nome": "Processo de Conhecimento"},
    "LIVRO-III": {"range": (503, 780), "nome": "Processo de Execução"},
    "LIVRO-IV": {"range": (781, 1072), "nome": "Procedimentos Especiais"},
}

# Tags padrão
TAGS_PADRAO = ["cpc", "processo-civil", "vigente"]

# Metadata
LEI_NUMERO = "13.105"
LEI_ANO = 2015
LEI_NOME = "Lei 13.105/2015 (Código de Processo Civil)"

if __name__ == "__main__":
    print(f"✅ Config CPC carregado")
    print(f"   Output: {OUTPUT_BASE}")

"""
Vercel entry point — importa o app FastAPI de scripts/api_fenice_saas.py.
O diretório scripts/ é adicionado ao sys.path para que fenice_rag e prompts
sejam encontrados com os caminhos relativos corretos.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from api_fenice_saas import app  # noqa: F401, E402

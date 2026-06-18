"""
Config STJ Scraper — Configurações para extração de HSE do STJ
"""

import os
from pathlib import Path

# ─── Paths ──────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).parent.parent
FENICE_BASE = PROJECT_ROOT / "Fenice bRain"
HSE_OUTPUT = FENICE_BASE / "03_PROCESSO_CIVIL" / "STJ_HSE"
HSE_CACHE = Path(__file__).parent / "_cache_stj_hse"

# Criar diretórios se não existirem
HSE_OUTPUT.mkdir(parents=True, exist_ok=True)
HSE_CACHE.mkdir(parents=True, exist_ok=True)

# ─── URLs STJ ────────────────────────────────────────────────
STJ_SCON_BASE = "https://www.stj.jus.br/SCON"
STJ_SCON_SEARCH = f"{STJ_SCON_BASE}/SearchBRS?baseName=VERDICTBRS"

# Parâmetros de busca
SEARCH_FILTERS = {
    "processo": "HDE",  # Homologação de Decisão Estrangeira
    "tipo_decisao": "ACRDO",  # Acórdão
    "ordem": "DESC",
    "formato": "HTML"
}

# ─── Headers HTTP ────────────────────────────────────────────
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Fenice Brain / Análise Jurídica) AppleWebKit/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Referer": STJ_SCON_BASE
}

# ─── Timeouts e Limites ─────────────────────────────────────
TIMEOUT_REQUEST = 30  # segundos
MAX_RETRIES = 3
RETRY_DELAY = 2  # segundos

# ─── Paginação ───────────────────────────────────────────────
RESULTADOS_POR_PAGINA = 20
MAX_PAGINAS = 10  # Limita a 200 decisões por run

# ─── Logging ─────────────────────────────────────────────────
LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "stj_hse_scraper.log"

# Níveis: DEBUG, INFO, WARNING, ERROR
LOG_LEVEL = "INFO"

# ─── Filtros de HSE ──────────────────────────────────────────
# Tipos de HSE a extrair
HSE_TIPOS = [
    "SENTENÇA_ESTRANGEIRA",
    "SENTENÇA_ARBITRAL",
    "LAUDO_ARBITRAL"
]

# Países de interesse (deixe vazio para todos)
PAISES_INTERESSE = [
    "Portugal", "España", "USA", "China", "Japão", "Itália",
    "França", "Alemanha", "Bélgica", "Suíça"
]

# ─── Palavras-chave para Ordem Pública ───────────────────────
PALAVRAS_ORDEM_PUBLICA = [
    "ordem pública", "direito fundamental", "violação", "inconstitucional",
    "contra os bons costumes", "direitos humanos", "direito do consumidor"
]

# ─── Padrões de Regex ────────────────────────────────────────
REGEX_PATTERNS = {
    "processo": r"HDE\s*(\d+(?:\.\d+)?)",
    "relator": r"Relator\s*[:\-\s]+([A-Za-z\s]+?)(?:;|,|$)",
    "data": r"(\d{1,2})\s+de\s+(janeiro|fevereiro|março|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro)\s+de\s+(\d{4})",
    "pais": r"(?:em|do|da|de)\s+([A-Z][a-záéíóúàâêôãõç\s]+?)(?:\.|;|,|país)",
    "resultado": r"(?:HOMOLOG|DEFER|INDEFERIR|PARCIAL).*?(?:SENTENÇA|DECISÃO)",
    "ordem_publica": r"(?:ordem\s+pública|violação|inconstitucional|direitos\s+fundamentais)"
}

# ─── Configurações de Cache ──────────────────────────────────
USE_CACHE = True
CACHE_EXPIRY_DAYS = 7  # Redownload se cache > 7 dias

# ─── Modo Debug ──────────────────────────────────────────────
DEBUG = False
SAVE_HTML_BRUTO = False  # Salva HTML bruto para debugging

if __name__ == "__main__":
    print(f"✅ Config STJ Scraper carregado")
    print(f"   HSE Output: {HSE_OUTPUT}")
    print(f"   HSE Cache: {HSE_CACHE}")
    print(f"   Log File: {LOG_FILE}")

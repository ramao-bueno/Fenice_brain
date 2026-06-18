"""
Config STF Analyzer — Configuração para análise de Súmulas Vinculantes e Temas RG
"""

import os
from pathlib import Path
from datetime import datetime

# ─── Paths ──────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).parent.parent
FENICE_BASE = PROJECT_ROOT / "Fenice bRain"

# Output paths
STF_OUTPUT_SV = FENICE_BASE / "03_PROCESSO_CIVIL" / "STF_SUMULAS" / "STF-SUMULAS-VINCULANTES"
STF_OUTPUT_RG = FENICE_BASE / "03_PROCESSO_CIVIL" / "STF_SUMULAS" / "STF-REPERCUSSAO-GERAL"
STF_CACHE = Path(__file__).parent / "_cache_stf_sumulas"
STF_EXPORTS = Path(__file__).parent / "exports"

# Criar diretórios se não existirem
STF_OUTPUT_SV.mkdir(parents=True, exist_ok=True)
STF_OUTPUT_RG.mkdir(parents=True, exist_ok=True)
STF_CACHE.mkdir(parents=True, exist_ok=True)
STF_EXPORTS.mkdir(parents=True, exist_ok=True)

# ─── URLs STF ────────────────────────────────────────────────────
# Portais oficiais (requer parsing manual ou scraping)
STF_PORTAL_SUMULAS = "https://portal.stf.jus.br/jurisprudencia/sumulaVinculante.asp"
STF_PORTAL_REPERCUSSAO = "https://portal.stf.jus.br/jurisprudencia/sumulaRepercussao.asp"
STF_PORTAL_JURISPRUDENCIA = "https://portal.stf.jus.br/jurisprudencia/"

# ─── Headers HTTP ────────────────────────────────────────────────
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Fenice Brain / Análise STF) AppleWebKit/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Referer": STF_PORTAL_JURISPRUDENCIA
}

# ─── Configurações de Análise ────────────────────────────────────
ANALISAR_MODULACAO = True  # Detectar modulação de efeitos
ANALISAR_IMPACTO_BUSINESS = True  # Estimar potencial monetário
EXTRAIR_KEYWORDS = True  # Gerar palavras-chave para RAG

# ─── Setores Jurídicos (para classificação) ──────────────────────
SETORES = [
    "Tributário",
    "Trabalhista",
    "Previdenciário",
    "Administrativo",
    "Penal",
    "Civil",
    "Processual",
    "Consumidor",
    "Direito de Família",
    "Direitos Fundamentais"
]

# ─── Impacto Financeiro (scoring) ────────────────────────────────
SCORING_IMPACTO = {
    "HIGH": {
        "setores": ["Tributário", "Previdenciário", "Trabalhista"],
        "keywords": [
            "tributo", "imposto", "ICMS", "IRPJ", "PIS", "COFINS",
            "INSS", "aposentadoria", "pensão", "contribuição",
            "indenização", "dano moral", "rescisão"
        ],
        "descricao": "Impacto alto em passivos corporativos ou arrecadação estatal"
    },
    "MEDIUM": {
        "setores": ["Civil", "Processual", "Direito de Família"],
        "keywords": [
            "obrigação", "contrato", "responsabilidade", "competência",
            "jurisdição", "herança", "alimentos", "divórcio"
        ],
        "descricao": "Impacto moderado em operações rotineiras"
    },
    "LOW": {
        "setores": ["Direitos Fundamentais"],
        "keywords": [
            "liberdade", "dignidade", "direitos políticos", "voto"
        ],
        "descricao": "Impacto baixo ou indireto em operações comerciais"
    }
}

# ─── Logging ─────────────────────────────────────────────────────
LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "stf_analyzer.log"

# Níveis: DEBUG, INFO, WARNING, ERROR
LOG_LEVEL = "INFO"

# ─── Chaves Primárias Universais ─────────────────────────────────
def gerar_chave_primaria(tipo: str, numero: str) -> str:
    """
    Gera chave primária universal no formato STF_SV_57 ou STF_TEMA_69
    Útil para lookups rápidos no banco de dados
    """
    if tipo == "SUMULA_VINCULANTE":
        # Extrai número de "SV 57"
        num = "".join(filter(str.isdigit, numero))
        return f"STF_SV_{num}"
    elif tipo == "REPERCUSSAO_GERAL":
        # Extrai número de "Tema 69"
        num = "".join(filter(str.isdigit, numero))
        return f"STF_TEMA_{num}"
    return f"STF_{numero.replace(' ', '_')}"

# ─── Templates de Saída ──────────────────────────────────────────
TEMPLATE_MARKDOWN_SV = """---
identificacao:
  tipo: {tipo}
  numero: {numero}
  processo: {processo}
  data_publicacao: {data}
  status: {status}
legal:
  artigos_crfb88: {artigos}
  leis_afetadas: {leis}
modulacao:
  houve: {modulacao_bool}
  regra: {modulacao_regra}
business:
  setor: {setor}
  impacto: {impacto}
  chave_primaria: {chave_primaria}
tags: {tags}
created: {created_date}
---

# {numero} — {tipo_format}

**Processo Paradigma:** {processo}
**Data de Publicação:** {data}
**Chave Primária:** {chave_primaria}

---

## 📋 ENUNCIADO

> {enunciado}

---

## 🎯 NÚCLEO DA TESE

{nucleo}

---

## ⚖️ ANCORAGEM LEGAL

### Dispositivos Constitucionais

{artigos_lista}

### Leis Infraconstitucionais

{leis_lista}

---

## 🔄 MODULAÇÃO DE EFEITOS

**Houve Modulação?** {modulacao_sim_nao}

{modulacao_condicional}

---

## 💼 IMPACTO BUSINESS & COMPLIANCE

**Setor Afetado:** {setor}
**Potencial de Impacto:** {impacto}

### Vulnerabilidade de Compliance

{vulnerabilidade}

---

## 🔍 PALAVRAS-CHAVE (RAG/Busca Semântica)

{keywords_lista}

---

**Análise gerada em:** {timestamp}
**Confiabilidade:** 80%
**Revisar manualmente:** {revisar}
"""

# ─── Cache ───────────────────────────────────────────────────────
USE_CACHE = True
CACHE_EXPIRY_DAYS = 30

# ─── Modo Debug ──────────────────────────────────────────────────
DEBUG = False
SAVE_TEXTO_BRUTO = False  # Salva texto bruto em _cache_stf_sumulas/

# ─── Validação ───────────────────────────────────────────────────
# Campos obrigatórios na análise
CAMPOS_OBRIGATORIOS = [
    "identificacao.tipo",
    "identificacao.numero_identificador",
    "conteudo_textual.enunciado_original",
    "ancoragem_legal.artigos_crfb88",
    "impacto_business_compliance.setor_afetado"
]

if __name__ == "__main__":
    print(f"✅ Config STF Analyzer carregado")
    print(f"   SV Output: {STF_OUTPUT_SV}")
    print(f"   RG Output: {STF_OUTPUT_RG}")
    print(f"   Cache: {STF_CACHE}")
    print(f"   Log File: {LOG_FILE}")
    print(f"\n   Exemplo de chave primária:")
    print(f"   SV 57 → {gerar_chave_primaria('SUMULA_VINCULANTE', 'SV 57')}")
    print(f"   Tema 69 → {gerar_chave_primaria('REPERCUSSAO_GERAL', 'Tema 69')}")

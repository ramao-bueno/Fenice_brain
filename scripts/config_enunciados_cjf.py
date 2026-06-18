"""
Config Enunciados CJF — interpretações e orientações do Conselho de Justiça Federal
extraídas do JSON estruturado já salvo.

Composição:
- 389 enunciados distribuídos em 21 jornadas
- Vinculados a 182 artigos/normas (principalmente CC, mas também CPC, CPP, leis especiais)
- Jornadas temáticas: Direito Civil, Administrativo, Comercial, Notarial, Ambiental, etc.
"""
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
FENICE_BASE = PROJECT_ROOT / "Fenice bRain"
ENUNCIADOS_BASE = FENICE_BASE / "00_ESTRUTURA_CONSTITUCIONAL" / "ENUNCIADOS_CJF"
OUTPUT_BASE = ENUNCIADOS_BASE / "Notas"
JSON_FILE = ENUNCIADOS_BASE / "enunciados_index.json"

JORNADAS = {
    "I Jornada de Direito Civil": "Direito Civil",
    "II Jornada de Direito Civil": "Direito Civil",
    "III Jornada de Direito Civil": "Direito Civil",
    "IV Jornada de Direito Civil": "Direito Civil",
    "V Jornada de Direito Civil": "Direito Civil",
    "VI Jornada de Direito Civil": "Direito Civil",
    "VII Jornada de Direito Civil": "Direito Civil",
    "VIII Jornada de Direito Civil": "Direito Civil",
    "IX Jornada de Direito Civil": "Direito Civil",
    "I Jornada de Direito Administrativo": "Direito Administrativo",
    "I Jornada de Direito Comercial": "Direito Comercial",
    "I Jornada de Direito Notarial e Registral": "Direito Notarial",
    "II Jornada de Prevenção e Solução Extrajudicial de Litígios": "Acesso à Justiça",
    "I Jornada Jurídica de Prevenção e Gerenciamento de Crises Ambientais": "Direito Ambiental",
    "II Jornada de Processo Eletrônico": "Processo Eletrônico",
    "Jornada de Trabalho": "Direito Laboral",
}

TAGS_PADRAO = ["enunciados-cjf", "jurisprudencia"]

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    print("Config Enunciados CJF carregado")
    print(f"  Output: {OUTPUT_BASE}")
    print(f"  JSON: {JSON_FILE}")
    print(f"  Total de jornadas: {len(JORNADAS)}")

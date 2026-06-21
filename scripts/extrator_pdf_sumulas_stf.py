#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extrator PDF — Súmulas do STF
Fonte: Enunciados_Sumulas_STF_1_a_736_Completo.pdf

Formato do PDF:
  SÚMULA {N}
  {texto} [(Superada)|(Cancelada)]
  Data de Aprovação
  Sessão Plenária de {data}
  ...
  Observação (opcional — detalha superação/cancelamento)
"""
import re
import sys
from pathlib import Path
from typing import List, Dict

import pdfplumber

PDF_PATH = Path(__file__).parent / "súmulas STF" / "Enunciados_Sumulas_STF_1_a_736_Completo.pdf"

# Início de cada súmula
RE_INICIO = re.compile(r"^SÚMULA\s+(\d+)\s*$", re.MULTILINE)

# Status inline (texto da súmula às vezes inclui esses marcadores)
RE_STATUS_INLINE = re.compile(
    r"\((Superada|Cancelada|Revogada|Alterada|Prejudicada)\)",
    re.IGNORECASE,
)

# Data de aprovação
RE_DATA_APROVACAO = re.compile(
    r"Sessão\s+Plenária\s+de\s+(\d{1,2}/\d{1,2}/\d{4})",
    re.IGNORECASE,
)

# Observação de superação
RE_OBSERVACAO_SUPERADA = re.compile(
    r"(?:foi\s+)?(?:declarada?\s+)?(?:superada?|cancelada?|revogada?)\s+no\s+julgamento",
    re.IGNORECASE,
)

# Seções que encerram o texto da súmula
SECOES_FIM = (
    "Data de Aprovação", "Fonte de Publicação", "Referência Legislativa",
    "Precedentes", "Observação", "Legislação", "Vide Súmula",
)


def _limpar(texto: str) -> str:
    texto = re.sub(r"\s+", " ", texto).strip()
    # Remove artefatos de rodapé do PDF
    texto = re.sub(r"\d+\s+Supremo\s+Tribunal\s+Federal", "", texto)
    texto = re.sub(r"Supremo\s+Tribunal\s+Federal\s+\d+", "", texto)
    return texto.strip()


def extrair_sumulas_pdf(pdf_path: Path = PDF_PATH) -> List[Dict]:
    """Extrai todas as súmulas do PDF oficial do STF."""
    # Concatena texto de todas as páginas (pula capa/sumário: primeiras 12 páginas)
    paginas = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages[12:]:  # a partir da pág 13 (índice 12) estão os textos
            t = page.extract_text()
            if t:
                paginas.append(t)
    texto_total = "\n".join(paginas)

    # Encontra posições de todas as súmulas
    inicios = list(RE_INICIO.finditer(texto_total))
    sumulas: List[Dict] = []

    for i, match in enumerate(inicios):
        numero = int(match.group(1))
        start = match.end()
        end = inicios[i + 1].start() if i + 1 < len(inicios) else len(texto_total)
        bloco = texto_total[start:end]

        # Extrai texto da súmula (até a primeira seção de metadados)
        linhas = bloco.split("\n")
        texto_linhas = []
        for linha in linhas:
            linha_stripped = linha.strip()
            if any(linha_stripped.startswith(s) for s in SECOES_FIM):
                break
            if linha_stripped:
                texto_linhas.append(linha_stripped)

        texto_sumula = _limpar(" ".join(texto_linhas))
        if not texto_sumula or len(texto_sumula) < 10:
            continue

        # Detecta status
        status = "vigente"
        m_status = RE_STATUS_INLINE.search(texto_sumula)
        if m_status:
            status = m_status.group(1).lower()
            # Remove marcador do texto principal
            texto_sumula = RE_STATUS_INLINE.sub("", texto_sumula).strip()
        elif RE_OBSERVACAO_SUPERADA.search(bloco):
            status = "superada"

        # Data de aprovação
        m_data = RE_DATA_APROVACAO.search(bloco)
        data_aprovacao = m_data.group(1) if m_data else ""

        # Referência legislativa (primeira linha após "Referência Legislativa")
        ref_match = re.search(
            r"Referência Legislativa\s*\n(.*?)(?:\n(?:Precedentes|Observação|SÚMULA)|$)",
            bloco, re.DOTALL
        )
        referencia = _limpar(ref_match.group(1)) if ref_match else ""

        sumulas.append({
            "numero": numero,
            "texto": texto_sumula,
            "status": status,
            "data_aprovacao": data_aprovacao,
            "referencia_legislativa": referencia[:500],
            "tema": "jurisprudencia-pacifica",
        })

    return sorted(sumulas, key=lambda x: x["numero"])


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sumulas = extrair_sumulas_pdf()
    total = len(sumulas)
    vigentes = sum(1 for s in sumulas if s["status"] == "vigente")
    superadas = sum(1 for s in sumulas if s["status"] != "vigente")
    print(f"Total extraído: {total} súmulas")
    print(f"  Vigentes:  {vigentes}")
    print(f"  Superadas/Canceladas: {superadas}")
    print()
    for s in sumulas[:3]:
        print(f"STF {s['numero']} [{s['status']}] ({s['data_aprovacao']})")
        print(f"  {s['texto'][:100]}...")
    print("...")
    for s in sumulas[-2:]:
        print(f"STF {s['numero']} [{s['status']}] ({s['data_aprovacao']})")
        print(f"  {s['texto'][:100]}...")

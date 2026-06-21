#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extrator PDF para Súmulas STJ — lê VerbetesSTJ.pdf do STJ."""
import re
import sys
from pathlib import Path
from typing import List, Dict

import pdfplumber

PDF_PATH = Path(__file__).parent.parent / "00_APEX" / "SUMULAS STJ" / "VerbetesSTJ.pdf"

# l SÚMULA 676\nVEJA MAIS\ntexto...(SEÇÃO, julgado em DD/MM/AAAA, DJe de DD/MM/AAAA)
RE_SUMULA = re.compile(
    r"l\s+SÚMULA\s+(\d+)\s*\n"
    r"(?:VEJA\s+MAIS\s*\n)?"
    r"(.*?)"
    r"\(([^)]*julgado\s+em[^)]*)\)",
    re.DOTALL,
)

# Metadados de julgamento: (TERCEIRA SEÇÃO, julgado em 11/12/2024, DJe de 17/12/2024)
RE_META = re.compile(
    r"^(.*?),\s*julgado\s+em\s+(\d{1,2}/\d{1,2}/\d{4}),\s*DJe\s+de\s+(\d{1,2}/\d{1,2}/\d{4})",
    re.IGNORECASE,
)


def _limpar(texto: str) -> str:
    texto = re.sub(r"\s+", " ", texto).strip()
    # Remove cabeçalho de página que aparece no meio do texto
    texto = re.sub(r"scon\.stj\.jus\.br/SCON/sumstj/\s*\d+", "", texto)
    texto = re.sub(r"Enunciados das\s+Súmulas do STJ", "", texto)
    return texto.strip()


def extrair_sumulas_pdf(pdf_path: Path = PDF_PATH) -> List[Dict]:
    """Extrai súmulas do PDF oficial do STJ."""
    # Concatena todo o texto do PDF
    texto_total = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                texto_total.append(t)
    texto = "\n".join(texto_total)

    sumulas = []
    for m in RE_SUMULA.finditer(texto):
        numero = int(m.group(1))
        texto_sumula = _limpar(m.group(2))
        meta_raw = m.group(3).strip()

        # Parseia metadados
        secao = ""
        julgado_em = ""
        dje = ""
        mm = RE_META.match(meta_raw)
        if mm:
            secao = mm.group(1).strip()
            julgado_em = mm.group(2)
            dje = mm.group(3)

        if texto_sumula and len(texto_sumula) > 10:
            sumulas.append({
                "numero": numero,
                "texto": texto_sumula,
                "tema": "jurisprudencia-pacifica",
                "secao": secao,
                "julgado_em": julgado_em,
                "dje": dje,
            })

    return sorted(sumulas, key=lambda x: x["numero"])


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sumulas = extrair_sumulas_pdf()
    print(f"Total extraído: {len(sumulas)} súmulas")
    for s in sumulas[-3:]:
        print(f"\n  STJ {s['numero']} ({s['secao']}, {s['julgado_em']}):")
        print(f"  {s['texto'][:100]}...")

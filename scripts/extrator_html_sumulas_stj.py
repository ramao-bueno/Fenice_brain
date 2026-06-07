#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extrator HTML especializado para Súmulas STJ (SCON do STJ)."""
import re
from pathlib import Path
from typing import List, Dict


def extrair_sumulas_stj(caminho_html: Path) -> List[Dict]:
    """
    Extrai súmulas de arquivo HTML do SCON (STJ).

    O HTML do SCON tem estrutura única com tabelas/divs contendo:
    - Número da súmula (STJ nº XXX)
    - Texto da súmula

    Args:
        caminho_html: Caminho para o arquivo .html do SCON

    Returns:
        Lista de dicts com {'numero': int, 'texto': str, ...}
    """
    conteudo = None
    for encoding in ["windows-1252", "iso-8859-1", "utf-8"]:
        try:
            with open(caminho_html, "r", encoding=encoding) as f:
                conteudo = f.read()
            break
        except UnicodeDecodeError:
            continue

    if not conteudo:
        return []

    sumulas = []

    # Pattern para SCON do STJ: procura por padrões como:
    # "Súmula nº 1" ou "STJ nº 1" seguido do texto
    # Há várias variações possíveis

    # Padrão 1: <a name="stj1"></a> ou similar + texto
    pattern1 = r'<a name="?stj(\d+)"?[^>]*>(.*?)(?=<a name|</body>|</html>)'
    matches1 = list(re.finditer(pattern1, conteudo, re.DOTALL | re.IGNORECASE))

    if matches1:
        for match in matches1:
            numero_str, texto_raw = match.groups()
            numero = int(numero_str)
            texto = _limpar_texto_sumula(texto_raw)
            if texto:
                sumulas.append({
                    "numero": numero,
                    "texto": texto,
                    "tema": "jurisprudencia-pacifica"
                })
    else:
        # Padrão 2: Procura por "STJ nº XXX" ou "Súmula nº XXX"
        pattern2 = r'(?:STJ|Súmula)\s+n(?:º|º|.)\s*(\d+)[^\n]*?\n\s*([^<\n]{20,500})'
        matches2 = list(re.finditer(pattern2, conteudo, re.IGNORECASE))

        for match in matches2:
            numero_str, texto_raw = match.groups()
            numero = int(numero_str)
            texto = _limpar_texto_sumula(texto_raw)
            if texto and numero <= 700:  # Súmulas STJ vão até ~670
                sumulas.append({
                    "numero": numero,
                    "texto": texto,
                    "tema": "jurisprudencia-pacifica"
                })

    return sorted(sumulas, key=lambda x: x["numero"])


def _limpar_texto_sumula(texto_raw: str) -> str:
    """Remove HTML tags e limpa whitespace."""
    # Remove tags HTML
    texto = re.sub(r"<[^>]+>", " ", texto_raw)
    # Remove múltiplos espaços/quebras
    texto = re.sub(r"\s+", " ", texto).strip()
    # Remove lixo comum do SCON
    texto = texto.replace("Conselho da Justiça Federal", "")
    texto = texto.replace("Javascript", "")
    # Trunca se muito longo
    texto = texto[:800].strip() if len(texto) > 800 else texto
    return texto


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")

    teste_html = Path("_stj_sumulas_page.html").resolve()
    if teste_html.exists():
        sumulas = extrair_sumulas_stj(teste_html)
        print(f"Extraído {len(sumulas)} súmulas de {teste_html.name}")
        for sumula in sumulas[:3]:
            print(f"  STJ {sumula['numero']}: {sumula['texto'][:60]}...")
    else:
        print(f"Arquivo não encontrado: {teste_html}")
        print("Instruções: Salve o HTML do SCON conforme descrito em config_sumulas_stj.py")

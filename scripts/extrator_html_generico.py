#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extrator HTML genérico para leis do Planalto (DC, CC, etc.)."""
import re
from pathlib import Path
from typing import List, Dict


def extrair_artigos_html(caminho_html: Path) -> List[Dict]:
    """
    Extrai artigos de arquivo HTML do Planalto (suporta múltiplos formatos).

    Args:
        caminho_html: Caminho para o arquivo .html

    Returns:
        Lista de dicts com {'numero': int, 'redacao': str, ...}
    """
    # Tenta diferentes encodings
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

    artigos = []

    # Pattern 1: <a name="artN"></a>Art. N° REDACAO...
    # Até o próximo artigo ou fim do documento
    pattern1 = r'<a name="art(\d+)"></a>Art\.\s*\d+[^<]*?\s*(.*?)(?=<a name="art\d+|</body>|</html>)'
    matches1 = list(re.finditer(pattern1, conteudo, re.DOTALL | re.IGNORECASE))

    if matches1:
        for match in matches1:
            numero_str, redacao_raw = match.groups()
            numero = int(numero_str)
            redacao = _limpar_redacao(redacao_raw)
            if redacao:
                artigos.append({
                    "numero": numero,
                    "redacao": redacao,
                    "titulo": f"Art. {numero}",
                    "categoria": "GENERICO"
                })
    else:
        # Pattern 2: Fallback — procura por "Art. N" sem tags de nome
        # Captura até o próximo "Art. M" ou fim
        pattern2 = r'Art\.\s+(\d+)[^\w]*?(.*?)(?=Art\.\s+\d+|</body>|</html>)'
        matches2 = list(re.finditer(pattern2, conteudo, re.DOTALL | re.IGNORECASE))

        for match in matches2:
            numero_str, redacao_raw = match.groups()
            try:
                numero = int(numero_str)
                redacao = _limpar_redacao(redacao_raw)
                if redacao:
                    artigos.append({
                        "numero": numero,
                        "redacao": redacao,
                        "titulo": f"Art. {numero}",
                        "categoria": "GENERICO"
                    })
            except ValueError:
                continue

    return sorted(artigos, key=lambda x: x["numero"])


def _limpar_redacao(redacao_raw: str) -> str:
    """Remove HTML tags e limpa whitespace."""
    redacao = re.sub(r"<[^>]+>", " ", redacao_raw)
    redacao = re.sub(r"\s+", " ", redacao).strip()
    # Trunca se muito longo
    redacao = redacao[:500].strip() if len(redacao) > 500 else redacao
    return redacao


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")

    # Teste
    teste_html = Path("../FENICE bRain/02_DIREITO_PRIVADO/DIREITO_CIVIL/L10406.html").resolve()
    if teste_html.exists():
        artigos = extrair_artigos_html(teste_html)
        print(f"Extraído {len(artigos)} artigos de {teste_html.name}")
        for art in artigos[:3]:
            print(f"  Art. {art['numero']}: {art['redacao'][:60]}...")
    else:
        print(f"Arquivo não encontrado: {teste_html}")

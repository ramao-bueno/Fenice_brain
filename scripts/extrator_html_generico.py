#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extrator HTML genérico para leis do Planalto (DC, CC, etc.)."""
import re
from pathlib import Path
from typing import List, Dict


def extrair_artigos_html(caminho_html: Path) -> List[Dict]:
    """
    Extrai artigos de arquivo HTML do Planalto (suporta múltiplos formatos).

    Estratégia híbrida:
    1. Procura tags <a name="artN"></a> (padrão antigo/primeiros artigos)
    2. Procura padrão "Art. N. Redação" para artigos sem tags de nome

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

    artigos_dict = {}  # Usa dict para evitar duplicatas por número

    # === ESTRATÉGIA 1: Tags <a name="artN"></a> ===
    pattern_names = r'<a name="art(\d+)"></a>'
    matches_names = list(re.finditer(pattern_names, conteudo))

    if matches_names:
        for i, match in enumerate(matches_names):
            numero_str = match.group(1)
            numero = int(numero_str)

            # Encontra posição inicial (depois da tag) e final (próxima tag ou fim)
            start_pos = match.end()
            end_pos = matches_names[i + 1].start() if i + 1 < len(matches_names) else len(conteudo)

            # Extrai conteúdo entre tags
            redacao_raw = conteudo[start_pos:end_pos]
            redacao = _limpar_redacao(redacao_raw)

            if redacao:
                artigos_dict[numero] = {
                    "numero": numero,
                    "redacao": redacao,
                    "titulo": f"Art. {numero}",
                    "categoria": "GENERICO"
                }

    # === ESTRATÉGIA 2: Fallback — padrão "Art. N. Redação" ===
    # Procura por "Art. \d+" que não esteja já em artigos_dict
    pattern2 = r'Art\.\s+(\d+)[^<]*?\.?\s+([^<]{10,500}?)(?=<[^>]*>|Art\.\s+\d+)'
    matches2 = list(re.finditer(pattern2, conteudo, re.IGNORECASE))

    for match in matches2:
        numero_str = match.group(1)
        redacao_raw = match.group(2) if len(match.groups()) > 1 else ""
        try:
            numero = int(numero_str)
            # Só adiciona se não foi capturado pela estratégia 1
            if numero not in artigos_dict:
                redacao = _limpar_redacao(redacao_raw) if redacao_raw else ""
                if redacao:
                    artigos_dict[numero] = {
                        "numero": numero,
                        "redacao": redacao,
                        "titulo": f"Art. {numero}",
                        "categoria": "GENERICO"
                    }
        except ValueError:
            continue

    artigos = list(artigos_dict.values())
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
    teste_html = Path("../Fenice bRain/02_DIREITO_PRIVADO/DIREITO_CIVIL/L10406.html").resolve()
    if teste_html.exists():
        artigos = extrair_artigos_html(teste_html)
        print(f"Extraído {len(artigos)} artigos de {teste_html.name}")
        for art in artigos[:3]:
            print(f"  Art. {art['numero']}: {art['redacao'][:60]}...")
    else:
        print(f"Arquivo não encontrado: {teste_html}")

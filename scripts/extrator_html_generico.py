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
    # Tenta UTF-8 primeiro (baixar_fontes.py salva em UTF-8)
    # Fallback para windows-1252 / iso-8859-1 para HTMLs legados
    conteudo = None
    for encoding in ["utf-8", "windows-1252", "iso-8859-1"]:
        try:
            with open(caminho_html, "r", encoding=encoding) as f:
                conteudo = f.read()
            break
        except UnicodeDecodeError:
            continue

    if not conteudo:
        return []

    # Chave: string "121" ou "121-A" — nunca int, para suportar sufixos
    artigos_dict: Dict[str, Dict] = {}

    # ── Detecta cabeçalhos de artigo no HTML ─────────────────────────────────
    # Formatos Planalto (capital "Art." — cross-refs usam lowercase "art."):
    #   Art. 1º - ...      (decretos-lei antigos: ordinal + traço)
    #   Art. 121. ...      (leis modernas: ponto)
    #   Art. 121-A. ...    (sufixo de letra: traço-LETRA-ponto)
    # Case-sensitive intencional: filtra "art. N deste Código" (cross-refs)
    PATTERN_ART = re.compile(
        r'Art\.\s+'                   # "Art. " — MAIÚSCULO obrigatório
        r'(\d+)'                      # número base
        r'(?:'
        r'(-[A-Z])\.'                 # sufixo "-A" seguido de ponto obrigatório
        r'|'
        r'(?:<[^>]*>[º°]</[^>]*>|[º°])'  # ordinal º (fora ou dentro de tags)
        r'\s*[-–—]'                   # traço de separação
        r'|'
        r'(?:<[^>]*>\s*</[^>]*>)'     # tag vazia/espaço (ex: <strong> </strong>)
        r'\s*[-–—]'                   # + traço
        r'|'
        r'\s+[-–—]'                   # espaço + traço (Art. 10 -)
        r'|'
        r'\.'                         # ponto simples
        r')',
    )
    cabecalhos = list(PATTERN_ART.finditer(conteudo))

    for i, match in enumerate(cabecalhos):
        num_base = match.group(1)
        sufixo = match.group(2).upper() if match.group(2) else ""  # "-A" já inclui o traço
        chave = f"{num_base}{sufixo}" if sufixo else num_base  # "121-A" ou "121"

        if chave in artigos_dict:
            continue

        start_pos = match.end()
        # Bloco vai até o próximo cabeçalho de artigo ou no máximo 3 KB
        end_pos = (cabecalhos[i + 1].start()
                   if i + 1 < len(cabecalhos)
                   else min(len(conteudo), start_pos + 3000))

        redacao_raw = conteudo[start_pos:end_pos]
        redacao = _limpar_redacao(redacao_raw)

        if redacao:
            artigos_dict[chave] = {
                "numero": chave,
                "redacao": redacao,
                "titulo": f"Art. {chave}",
                "categoria": "GENERICO"
            }

    artigos = list(artigos_dict.values())

    def _sort_key(a: Dict):
        m = re.match(r'^(\d+)(-[A-Z])?$', str(a["numero"]))
        if m:
            return (int(m.group(1)), m.group(2) or "")
        return (0, str(a["numero"]))

    return sorted(artigos, key=_sort_key)


def _limpar_redacao(redacao_raw: str) -> str:
    """Remove HTML tags, entidades e limpa whitespace."""
    redacao = re.sub(r"<[^>]+>", " ", redacao_raw)
    # Entidades HTML comuns
    redacao = redacao.replace("&nbsp;", " ").replace("&amp;", "&")
    redacao = redacao.replace("&lt;", "<").replace("&gt;", ">")
    redacao = redacao.replace("&quot;", '"').replace("&#39;", "'")
    redacao = re.sub(r"&[a-z]+;", " ", redacao)  # demais entidades
    redacao = re.sub(r"\s+", " ", redacao).strip()
    redacao = redacao[:3000].strip() if len(redacao) > 3000 else redacao
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

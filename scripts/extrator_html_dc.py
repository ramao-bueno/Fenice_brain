#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extrator HTML para artigos de Direito Constitucional (salvo do Planalto)."""
import re
from pathlib import Path
from typing import List, Dict
from html.parser import HTMLParser


class ArtigoExtractor(HTMLParser):
    """Parse HTML e extrai artigos com número, título e redação."""

    def __init__(self):
        super().__init__()
        self.artigos = []
        self.current_artigo = None
        self.in_artigo_span = False
        self.collecting = False
        self.buffer = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        # Detectar início de artigo: <a name="art3"></a> ou similar
        if tag == "a" and "name" in attrs_dict:
            name = attrs_dict["name"]
            if name.startswith("art"):
                # Extrai número do atributo name (ex: "art3" -> 3)
                try:
                    num = int(re.sub(r"\D", "", name.split("art")[-1]))
                    self.current_artigo = {"numero": num, "redacao": ""}
                    self.collecting = True
                except (ValueError, IndexError):
                    pass

    def handle_data(self, data):
        if self.collecting and self.current_artigo is not None:
            texto = data.strip()
            if texto and not texto.startswith("Art."):
                # Coleciona o texto após "Art. X°/Art. X."
                self.buffer.append(texto)

    def handle_endtag(self, tag):
        # Se acabou uma linha (br, p) ou nova tag de artigo, salva o artigo anterior
        if self.collecting and self.current_artigo is not None:
            # Continuação: próximo artigo detectado automaticamente
            if tag in ["p", "div"] and self.buffer:
                self.current_artigo["redacao"] = " ".join(self.buffer).strip()
                if self.current_artigo["redacao"]:
                    self.artigos.append(self.current_artigo)
                    self.current_artigo = None
                    self.buffer = []
                    self.collecting = False


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
                    "categoria": "CONSTITUCIONAL"
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
                        "categoria": "CONSTITUCIONAL"
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
    teste_html = Path("../Fenice bRain/00_ESTRUTURA_CONSTITUCIONAL/DIREITO_CONSTITUCIONAL/L12016.html").resolve()
    if teste_html.exists():
        artigos = extrair_artigos_html(teste_html)
        print(f"Extraído {len(artigos)} artigos de {teste_html.name}")
        for art in artigos[:3]:
            print(f"  Art. {art['numero']}: {art['redacao'][:60]}...")
    else:
        print(f"Arquivo não encontrado: {teste_html}")

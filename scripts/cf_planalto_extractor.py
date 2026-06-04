#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extrator CF/88 do Planalto.gov.br

Busca o texto oficial da Constituicao Federal diretamente do Planalto,
evitando problemas de codificacao do PDF local.

Uso:
    from cf_planalto_extractor import CFPlanaltoExtractor
    ext = CFPlanaltoExtractor()
    artigos = ext.extract_articles()
"""
import re
import requests
from pathlib import Path
from typing import List, Dict
from config_cf import TITULO_MAPEAMENTO

PLANALTO_URL = "https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm"

# Ordinal para numero: 1º -> 1, 2º -> 2, etc.
_ORDINAL_RE = re.compile(r"Art\.\s*(\d+)\s*[ºo°]?\s*[-–—]?\s*", re.IGNORECASE)
_ART_NUM_RE = re.compile(r"Art\.\s*(\d+)\s*[ºo°]?", re.IGNORECASE)


class CFPlanaltoExtractor:
    """Extrai artigos da CF/88 diretamente do HTML do Planalto.gov.br."""

    def __init__(self, url: str = PLANALTO_URL):
        self.url = url
        self.artigos: List[Dict] = []

    def _fetch_html(self) -> str:
        # Cache local para evitar re-download
        cache_path = Path(__file__).parent / "_cache_cf_planalto.html"
        if cache_path.exists():
            print(f"Usando cache local: {cache_path.name}")
            return cache_path.read_text(encoding="utf-8")

        print(f"Baixando CF/88 do Planalto: {self.url}")
        headers = {"User-Agent": "Mozilla/5.0 (Fenice Brain / Estudo Juridico)"}
        resp = requests.get(self.url, headers=headers, timeout=60)
        resp.raise_for_status()

        # Planalto serve em windows-1252 (ISO-8859-1 extendido)
        html_utf8 = resp.content.decode("windows-1252", errors="replace")

        # Salva cache em UTF-8
        cache_path.write_text(html_utf8, encoding="utf-8")
        print(f"  Download OK: {len(html_utf8):,} caracteres (cache salvo)")
        return html_utf8

    def _limpar_html(self, html: str) -> str:
        """Remove tags HTML e normaliza espacos."""
        # Remove tags
        limpo = re.sub(r"<[^>]+>", " ", html)
        # Remove entidades HTML comuns
        limpo = limpo.replace("&nbsp;", " ").replace("&amp;", "&")
        limpo = limpo.replace("&lt;", "<").replace("&gt;", ">")
        limpo = limpo.replace("\r\n", "\n").replace("\r", "\n")
        # Normaliza espacos multiplos
        limpo = re.sub(r"[ \t]+", " ", limpo)
        # Normaliza linhas multiplas
        limpo = re.sub(r"\n{3,}", "\n\n", limpo)
        return limpo.strip()

    def _determinar_titulo(self, numero: int) -> str:
        for sigla, config in TITULO_MAPEAMENTO.items():
            inicio, fim = config["range"]
            if inicio <= numero <= fim:
                return sigla
        return "SEM_TITULO"

    def extract_articles(self) -> List[Dict]:
        html = self._fetch_html()
        texto = self._limpar_html(html)

        # Divide o texto nos pontos onde aparecem artigos
        # Padrao: "Art. Nº" ou "Art. N" com ordinal opcional
        padrao_art = re.compile(
            r"(?:^|\n)\s*(Art\.\s*\d+\s*[ºo°]?\s*[-–—\.]?\s*.{0,200}?)(?=\n\s*Art\.\s*\d+\s*[ºo°]?|\Z)",
            re.DOTALL | re.MULTILINE
        )

        # Abordagem alternativa: split no marcador "Art. N"
        # Encontra todas as posicoes de artigos
        marcadores = list(re.finditer(
            r"(?:^|\n)\s*(Art\.\s*(\d+)\s*[ºo°]?)",
            texto, re.MULTILINE
        ))

        print(f"  Encontrados {len(marcadores)} marcadores de artigo")

        vistos = set()
        for i, match in enumerate(marcadores):
            try:
                num_str = match.group(2)
                num = int(num_str)

                if num in vistos or num > 250:
                    continue
                vistos.add(num)

                # Extrai conteudo ate o proximo artigo
                inicio = match.start()
                if i + 1 < len(marcadores):
                    fim = marcadores[i + 1].start()
                else:
                    fim = min(inicio + 5000, len(texto))

                bloco = texto[inicio:fim].strip()

                # Limpa o bloco
                bloco = re.sub(r"\n+", " ", bloco)
                bloco = re.sub(r"\s+", " ", bloco).strip()

                # Separa titulo (primeiro paragrafo) da redacao completa
                # Remove o "Art. Nº" do inicio
                sem_prefixo = re.sub(
                    r"^Art\.\s*\d+\s*[ºo°]?\s*[-–—\.]?\s*", "", bloco
                ).strip()

                # Titulo = primeiro periodo (ate ponto ou dois pontos)
                match_titulo = re.match(r"^([^.:;]{5,120}[.:;]?)", sem_prefixo)
                titulo_artigo = match_titulo.group(1).strip() if match_titulo else sem_prefixo[:100]
                titulo_artigo = titulo_artigo.rstrip(".:")

                # Redacao = primeiros 400 chars
                redacao = sem_prefixo[:400].strip()
                if len(sem_prefixo) > 400:
                    redacao += "..."

                titulo_kelsen = self._determinar_titulo(num)
                if titulo_kelsen == "SEM_TITULO":
                    continue

                self.artigos.append({
                    "numero": num,
                    "titulo": titulo_artigo[:120],
                    "redacao": redacao,
                    "livro": titulo_kelsen,  # compatibilidade com pipeline
                    "texto_completo": sem_prefixo[:2000],
                })

            except Exception:
                continue

        self.artigos.sort(key=lambda x: x["numero"])
        print(f"  {len(self.artigos)} artigos extraidos com sucesso")
        return self.artigos


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")

    ext = CFPlanaltoExtractor()
    artigos = ext.extract_articles()

    print("\nAmostra - primeiros 5 artigos:")
    for art in artigos[:5]:
        print(f"\n  Art. {art['numero']} [{art['livro']}]")
        print(f"  Titulo: {art['titulo'][:80]}")
        print(f"  Redacao: {art['redacao'][:100]}...")

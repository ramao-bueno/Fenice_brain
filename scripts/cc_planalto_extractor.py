#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extrator CC do Planalto.gov.br

Busca o texto oficial do Código Civil diretamente do Planalto,
resolvendo o problema do PDF com fontes ilegíveis.
"""
import re
import requests
from pathlib import Path
from typing import List, Dict
from config_cc import LIVRO_MAPEAMENTO

PLANALTO_URL = "https://www.planalto.gov.br/ccivil_03/leis/2002/l10406compilada.htm"
_CACHE = Path(__file__).parent / "_cache_cc_planalto.html"


class CCPlanaltoExtractor:

    def __init__(self, url: str = PLANALTO_URL):
        self.url = url
        self.artigos: List[Dict] = []

    def _fetch_html(self) -> str:
        if _CACHE.exists():
            print(f"Cache local: {_CACHE.name}")
            return _CACHE.read_text(encoding="utf-8")
        print(f"Baixando CC do Planalto: {self.url}")
        headers = {"User-Agent": "Mozilla/5.0 (Fenice Brain / Estudo Juridico)"}
        resp = requests.get(self.url, headers=headers, timeout=60)
        resp.raise_for_status()
        html = resp.content.decode("windows-1252", errors="replace")
        _CACHE.write_text(html, encoding="utf-8")
        print(f"  Download OK: {len(html):,} chars (cache salvo)")
        return html

    def _limpar_html(self, html: str) -> str:
        limpo = re.sub(r"<[^>]+>", " ", html)
        limpo = limpo.replace("&nbsp;", " ").replace("&amp;", "&")
        limpo = re.sub(r"[ \t]+", " ", limpo)
        limpo = re.sub(r"\n{3,}", "\n\n", limpo)
        return limpo.strip()

    def _determinar_livro(self, num: int) -> str:
        for sigla, config in LIVRO_MAPEAMENTO.items():
            inicio, fim = config["range"]
            if inicio <= num <= fim:
                return sigla
        return "SEM_LIVRO"

    def extract_articles(self) -> List[Dict]:
        html = self._fetch_html()
        texto = self._limpar_html(html)

        marcadores = list(re.finditer(
            r"(?:^|\n)\s*(Art\.\s*(\d+(?:\.\d+)?)\s*[ºo°]?)",
            texto, re.MULTILINE
        ))
        print(f"  Encontrados {len(marcadores)} marcadores de artigo")

        vistos = set()
        for i, match in enumerate(marcadores):
            try:
                num_str = match.group(2).replace(".", "")
                num = int(num_str)
                if num in vistos or num > 2046:
                    continue
                vistos.add(num)

                inicio = match.start()
                fim = marcadores[i + 1].start() if i + 1 < len(marcadores) else inicio + 5000
                bloco = texto[inicio:fim].strip()
                bloco = re.sub(r"\s+", " ", bloco).strip()

                sem_prefixo = re.sub(
                    r"^Art\.\s*\d+(?:\.\d+)?\s*[ºo°]?\s*[-–—\.]?\s*", "", bloco
                ).strip()

                match_titulo = re.match(r"^([^.:;]{5,120}[.:;]?)", sem_prefixo)
                titulo = match_titulo.group(1).strip().rstrip(".:") if match_titulo else sem_prefixo[:100]

                redacao = sem_prefixo[:600].strip()
                if len(sem_prefixo) > 600:
                    redacao += "..."

                livro = self._determinar_livro(num)
                if livro == "SEM_LIVRO":
                    continue

                self.artigos.append({
                    "numero": num,
                    "titulo": titulo[:120],
                    "redacao": redacao,
                    "livro": livro,
                    "texto_completo": sem_prefixo[:3000],
                })
            except Exception:
                continue

        self.artigos.sort(key=lambda x: x["numero"])
        print(f"  {len(self.artigos)} artigos extraídos")
        return self.artigos


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    ext = CCPlanaltoExtractor()
    arts = ext.extract_articles()
    print("\nAmostra — primeiros 3 artigos:")
    for a in arts[:3]:
        print(f"  Art. {a['numero']} [{a['livro']}]: {a['titulo'][:70]}")
        print(f"  Redação: {a['redacao'][:120]}...")

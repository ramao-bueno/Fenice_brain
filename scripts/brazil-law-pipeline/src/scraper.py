#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scraper — Download de HTML e extracao de links de indice do Planalto.

Baseado em planalto_pipeline.py (funcoes baixar_html e extrair_links_do_indice).
"""
import os
import re
import time
import random
from pathlib import Path
from typing import List, Optional

import requests

# ── Configuracao ──────────────────────────────────────────────────────────────

PLANALTO_BASE = "https://www.planalto.gov.br"

CACHE_DIR = Path(os.environ.get("CACHE_DIR", "/app/_cache_planalto"))

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
]

# Faixas de anos para URLs estruturadas do Planalto
_ANO_FAIXAS = [
    (1988, 1990, "_ato1988-1990"),
    (1991, 1994, "_ato1991-1994"),
    (1995, 1998, "_ato1995-1998"),
    (1999, 2002, "_ato1999-2002"),
    (2003, 2006, "_ato2003-2006"),
    (2007, 2010, "_ato2007-2010"),
    (2011, 2014, "_ato2011-2014"),
    (2015, 2018, "_ato2015-2018"),
    (2019, 2022, "_ato2019-2022"),
    (2023, 2026, "_ato2023-2026"),
    (2027, 2030, "_ato2027-2030"),
]


# ── Download ──────────────────────────────────────────────────────────────────

def baixar_html(url: str, forcar: bool = False) -> Optional[Path]:
    """Download do HTML com cache local, retry e user-agent rotation."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    nome_arquivo = re.sub(r"[^\w\-.]", "_", url.split("/")[-1]) or "index.htm"
    caminho = CACHE_DIR / nome_arquivo

    if caminho.exists() and not forcar:
        return caminho

    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
        "Referer": PLANALTO_BASE,
    }

    for tentativa in range(3):
        try:
            delay = random.uniform(1.0, 2.5) + tentativa * 1.5
            time.sleep(delay)
            resp = requests.get(url, headers=headers, timeout=20)
            resp.raise_for_status()
            resp.encoding = resp.apparent_encoding or "utf-8"

            caminho.write_text(resp.text, encoding="utf-8")
            print(f"  [OK] {nome_arquivo}")
            return caminho

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print(f"  [404] Lei nao encontrada: {url}")
                return None
            print(f"  [retry {tentativa+1}/3] {e}")
        except Exception as e:
            print(f"  [retry {tentativa+1}/3] {e}")

    print(f"  [ERRO] Falhou apos 3 tentativas: {url}")
    return None


# ── Indice por Ano ────────────────────────────────────────────────────────────

def extrair_links_do_indice(url_indice: str) -> List[str]:
    """Varre pagina de indice do Planalto e extrai links validos de leis."""
    from urllib.parse import urljoin
    from bs4 import BeautifulSoup

    caminho = baixar_html(url_indice)
    if not caminho:
        return []

    html = caminho.read_text(encoding="utf-8", errors="replace")
    soup = BeautifulSoup(html, "html.parser")

    links_validos: set = set()
    for a in soup.find_all("a", href=True):
        href = a["href"].lower()
        if ("lei" in href or "ato" in href or re.search(r"[l]\d{4,6}", href)):
            if href.endswith(".htm") or href.endswith(".html"):
                url_abs = urljoin(url_indice, a["href"])
                links_validos.add(url_abs)

    print(f"  [{len(links_validos)} links] {url_indice}")
    return sorted(links_validos)


def listar_leis_por_ano(ano: int) -> List[str]:
    """Descobre leis publicadas em um ano via indice do Planalto."""
    faixa = next((f for a, b, f in _ANO_FAIXAS if a <= ano <= b), None)
    urls_indices = []

    if faixa:
        urls_indices.append(
            f"{PLANALTO_BASE}/ccivil_03/{faixa}/{ano}/lei/leis{ano}.htm"
        )
        urls_indices.append(
            f"{PLANALTO_BASE}/ccivil_03/{faixa}/{ano}/lei/lcp/leis{ano}.htm"
        )

    if ano <= 2002:
        urls_indices.append(f"{PLANALTO_BASE}/ccivil_03/leis/quadro_lic.htm")

    todos_links: List[str] = []
    for url_idx in urls_indices:
        todos_links.extend(extrair_links_do_indice(url_idx))

    return list(set(todos_links))

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pipeline Planalto — Download + Parser Semântico de Legislação Federal

Arquitetura:
  [Portal do Planalto] → [Download com retry/user-agent] → [HTML bruto local]
      → [Parser semântico BeautifulSoup] → [texto_vigente + fragmentos_revogados]
      → [Nota Markdown no vault]

URL Structure do Planalto:
  Leis: https://www.planalto.gov.br/ccivil_03/leis/{ano}/L{numero}.htm
  Índice por ano: https://www.planalto.gov.br/ccivil_03/leis/{ano}/

CRÍTICO: Remove <s>, <strike>, <del> ANTES de extrair texto para não indexar
texto revogado como vigente.
"""
import os
import re
import sys
import time
import random
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

import requests
from bs4 import BeautifulSoup

# ── Configuração ──────────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).parent.parent
HTML_BRUTO_DIR = PROJECT_ROOT / "scripts" / "_cache_planalto"
OUTPUT_LEIS_DIR = PROJECT_ROOT / "02_LEGISLACAO" / "Leis"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
]

PLANALTO_BASE = "https://www.planalto.gov.br"

# Planalto usa blocos de 4 anos nas URLs de leis modernas
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


def _url_lei(numero: str, ano: int) -> List[str]:
    """Gera candidatos de URL para uma lei, do mais provável ao menos provável."""
    n = numero.lstrip("0")
    faixa = next((f for a, b, f in _ANO_FAIXAS if a <= ano <= b), None)
    candidatos = []
    if faixa:
        candidatos.append(f"{PLANALTO_BASE}/ccivil_03/{faixa}/{ano}/lei/l{n}.htm")
        candidatos.append(f"{PLANALTO_BASE}/ccivil_03/{faixa}/{ano}/lei/L{n}.htm")
        candidatos.append(f"{PLANALTO_BASE}/ccivil_03/{faixa}/{ano}/lei/lcp/lcp{n}.htm")
    # Fallback: leis antigas sem faixa de ano
    candidatos.append(f"{PLANALTO_BASE}/ccivil_03/leis/L{n}.htm")
    candidatos.append(f"{PLANALTO_BASE}/ccivil_03/leis/lcp/Lcp{n}.htm")
    return candidatos

# ── Download ──────────────────────────────────────────────────────────────────

def baixar_html(url: str, forcar: bool = False) -> Optional[Path]:
    """Download do HTML com cache local, retry e user-agent rotation."""
    HTML_BRUTO_DIR.mkdir(parents=True, exist_ok=True)

    nome_arquivo = re.sub(r"[^\w\-.]", "_", url.split("/")[-1]) or "index.htm"
    caminho = HTML_BRUTO_DIR / nome_arquivo

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
            print(f"  ✅ {nome_arquivo}")
            return caminho

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print(f"  ⚠️  404 — lei não encontrada: {url}")
                return None
            print(f"  ↻  Tentativa {tentativa+1}/3 — {e}")
        except Exception as e:
            print(f"  ↻  Tentativa {tentativa+1}/3 — {e}")

    print(f"  ❌ Falhou após 3 tentativas: {url}")
    return None


# ── Parser Semântico ──────────────────────────────────────────────────────────

def parsear_lei(caminho_html: Path) -> Dict:
    """
    Parser semântico que separa texto vigente de texto revogado.

    Trata as tags do Planalto:
      <s>...</s>      → texto revogado/riscado
      <strike>...</strike> → idem (formato antigo)
      <del>...</del>  → idem (padrão HTML5)
    """
    html = caminho_html.read_text(encoding="utf-8", errors="replace")
    soup = BeautifulSoup(html, "html.parser")

    titulo_tag = soup.find("title")
    titulo = titulo_tag.get_text(strip=True) if titulo_tag else caminho_html.stem

    # Extrai número e ano do título, URL ou nome do arquivo
    num_lei = _extrair_numero_lei(titulo, caminho_html.stem)
    # Tenta extrair o ano do caminho (ex: _ato2019-2022/2021/lei/l14133.htm)
    caminho_str = str(caminho_html)
    m_ano_path = re.search(r"[/\\](\d{4})[/\\]lei[/\\]", caminho_str)
    ano_lei = m_ano_path.group(1) if m_ano_path else _extrair_ano(titulo, caminho_html.stem)

    texto_vigente_blocos: List[str] = []
    fragmentos_revogados: List[str] = []

    # Varre blocos do conteúdo principal
    corpo = soup.find("body") or soup
    for elem in corpo.find_all(["p", "div", "span", "li"]):
        # Coleta texto revogado das tags de rasura
        for rasura_tag in elem.find_all(["s", "strike", "del"]):
            txt = rasura_tag.get_text(strip=True)
            if txt and len(txt) > 5:
                fragmentos_revogados.append(txt)
            rasura_tag.decompose()

        # O que sobrou é texto vigente
        txt = elem.get_text(separator=" ", strip=True)
        txt = re.sub(r"\s+", " ", txt).strip()
        if txt and len(txt) > 10:
            texto_vigente_blocos.append(txt)

    # Desduplicação mantendo ordem
    seen = set()
    vigente_unico = []
    for bloco in texto_vigente_blocos:
        if bloco not in seen:
            seen.add(bloco)
            vigente_unico.append(bloco)

    return {
        "arquivo_fonte": caminho_html.name,
        "titulo": titulo,
        "numero": num_lei,
        "ano": ano_lei,
        "texto_vigente": "\n\n".join(vigente_unico),
        "fragmentos_revogados": fragmentos_revogados,
        "url_origem": f"{PLANALTO_BASE}/ccivil_03/leis/{ano_lei}/L{num_lei}.htm",
        "ultima_atualizacao": datetime.now().strftime("%Y-%m-%d"),
    }


def _extrair_numero_lei(titulo: str, stem: str) -> str:
    for txt in [titulo, stem]:
        m = re.search(r"(\d{4,6})", txt)
        if m:
            return m.group(1)
    return stem


def _extrair_ano(titulo: str, stem: str) -> str:
    for txt in [titulo, stem]:
        m = re.search(r"(20\d{2}|19\d{2})", txt)
        if m:
            return m.group(1)
    return str(datetime.now().year)


# ── Índice por Ano ────────────────────────────────────────────────────────────

def extrair_links_do_indice(url_indice: str) -> List[str]:
    """
    Varre uma página de índice do Planalto e extrai links válidos de leis.

    Índices conhecidos:
      https://www.planalto.gov.br/ccivil_03/leis/quadro_lic.htm        (2002 a hoje)
      https://www.planalto.gov.br/ccivil_03/_ato{faixa}/{ano}/lei/leis{ano}.htm
    """
    from urllib.parse import urljoin

    caminho = baixar_html(url_indice)
    if not caminho:
        return []

    html = caminho.read_text(encoding="utf-8", errors="replace")
    soup = BeautifulSoup(html, "html.parser")

    links_validos: set = set()
    for a in soup.find_all("a", href=True):
        href = a["href"].lower()
        # Links que apontem para leis ou decretos (.htm/.html)
        if ("lei" in href or "ato" in href or re.search(r"[l]\d{4,6}", href)):
            if href.endswith(".htm") or href.endswith(".html"):
                url_abs = urljoin(url_indice, a["href"])
                links_validos.add(url_abs)

    print(f"  📋 {len(links_validos)} links encontrados em: {url_indice}")
    return sorted(links_validos)


def listar_leis_por_ano(ano: int) -> List[str]:
    """
    Descobre leis publicadas em um ano específico via índice do Planalto.

    URL de índice por ano (formato confirmado):
      https://www.planalto.gov.br/ccivil_03/_ato{faixa}/{ano}/lei/leis{ano}.htm
    """
    faixa = next((f for a, b, f in _ANO_FAIXAS if a <= ano <= b), None)
    urls_indices = []

    if faixa:
        urls_indices.append(
            f"{PLANALTO_BASE}/ccivil_03/{faixa}/{ano}/lei/leis{ano}.htm"
        )
        # Leis Complementares do mesmo ano
        urls_indices.append(
            f"{PLANALTO_BASE}/ccivil_03/{faixa}/{ano}/lei/lcp/leis{ano}.htm"
        )

    # Índice histórico geral (2002 em diante)
    if ano <= 2002:
        urls_indices.append(f"{PLANALTO_BASE}/ccivil_03/leis/quadro_lic.htm")

    todos_links: List[str] = []
    for url_idx in urls_indices:
        todos_links.extend(extrair_links_do_indice(url_idx))

    return list(set(todos_links))


# ── Gerador de Nota Markdown ──────────────────────────────────────────────────

def gerar_nota_lei(dados: Dict) -> str:
    """Gera nota Markdown atômica para uma lei federal."""
    num = dados["numero"]
    ano = dados["ano"]
    titulo = dados["titulo"]
    vigente = dados["texto_vigente"][:5000]  # trunca para nota enxuta
    revogados = dados["fragmentos_revogados"]

    n_revogados = len(revogados)
    aviso_revogados = (
        f"\n> [!WARNING] {n_revogados} fragmento(s) revogado(s) detectado(s)\n"
        f"> Texto riscado (`<s>`) removido e preservado em `fragmentos_revogados`.\n"
        if n_revogados else ""
    )

    fm = f"""---
lei: '{num}'
ano: '{ano}'
tipo: lei-federal
status: vigente
url_origem: "{dados['url_origem']}"
fragmentos_revogados: {n_revogados}
relacionados: []
tags:
  - lei-federal
  - legislacao
  - ano-{ano}
created: '{dados['ultima_atualizacao']}'
---"""

    corpo = f"""# {titulo}

**Lei Federal {num}/{ano}**
**Fonte:** [Planalto]({dados['url_origem']})
**Última atualização:** {dados['ultima_atualizacao']}
{aviso_revogados}
---

## TEXTO VIGENTE

{vigente}

---

## ARTIGOS CORRELATOS

[Outros dispositivos que se relacionam com esta lei]

---

## JURISPRUDÊNCIA

[Decisões do STF/STJ sobre esta lei]

---

## OBSERVAÇÕES

[Notas doutrinárias e impacto prático]
"""
    return f"{fm}\n\n{corpo}"


def salvar_nota(dados: Dict, output_dir: Path) -> Optional[Path]:
    """Salva a nota markdown da lei no vault."""
    output_dir.mkdir(parents=True, exist_ok=True)
    num = dados["numero"]
    ano = dados["ano"]
    nome = f"Lei-{num}-{ano}.md"
    path = output_dir / nome

    try:
        path.write_text(gerar_nota_lei(dados), encoding="utf-8")
        return path
    except Exception as e:
        print(f"  ❌ Erro ao salvar {nome}: {e}")
        return None


# ── CLI Principal ─────────────────────────────────────────────────────────────

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    print("=" * 70)
    print("PIPELINE PLANALTO — Parser Semântico de Legislação Federal")
    print("=" * 70)
    print()

    import argparse
    parser = argparse.ArgumentParser(description="Pipeline Planalto")
    parser.add_argument("--ano", type=int, help="Descobrir leis de um ano (ex: 2026)")
    parser.add_argument("--url", type=str, help="URL direta de uma lei")
    parser.add_argument("--lei", type=str, help="Número da lei (ex: 14133)")
    parser.add_argument("--lei-ano", type=str, default=str(datetime.now().year),
                        help="Ano da lei (usa com --lei)")
    parser.add_argument("--forcar", action="store_true", help="Redownload mesmo se já existe")
    args = parser.parse_args()

    if args.ano:
        print(f"📋 Descobrindo leis publicadas em {args.ano}...")
        leis = listar_leis_por_ano(args.ano)
        print(f"   {len(leis)} leis encontradas")
        for lei in leis[:5]:
            print(f"   • {lei['titulo']} → {lei['url']}")
        if len(leis) > 5:
            print(f"   ... e mais {len(leis)-5}")

    elif args.url or args.lei:
        if args.url:
            url = args.url
        else:
            candidatos = _url_lei(args.lei, int(args.lei_ano))
            url = candidatos[0]  # tenta o mais provável primeiro
        print(f"📥 Baixando: {url}")
        caminho = baixar_html(url, forcar=args.forcar)

        if caminho:
            print("🔍 Parsing semântico...")
            dados = parsear_lei(caminho)
            print(f"   Título: {dados['titulo']}")
            print(f"   Vigente: {len(dados['texto_vigente'])} chars")
            print(f"   Revogados: {len(dados['fragmentos_revogados'])} fragmentos")

            print("📝 Gerando nota...")
            path = salvar_nota(dados, OUTPUT_LEIS_DIR)
            if path:
                print(f"   ✅ Salvo: {path}")

    else:
        parser.print_help()
        print()
        print("Exemplos:")
        print("  python planalto_pipeline.py --lei 14133 --lei-ano 2021")
        print("  python planalto_pipeline.py --ano 2026")
        print("  python planalto_pipeline.py --url https://www.planalto.gov.br/ccivil_03/leis/2026/L15384.htm")

    print()
    print("=" * 70)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extrator alternativo para HTMLs Planalto que usam <div id='artN'>
(CC, L11340 e similares) e submete texto completo ao Supabase.
"""
import os, re, sys, time
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from planalto_pipeline import _load_env
from bs4 import BeautifulSoup
import requests as _req

FONTES_DIR = PROJECT_ROOT / "scripts" / "fontes"

# Arquivos que precisam de extração alternativa
LEIS = [
    ("cc/L10406.html",   "Lei Federal",  "10406", "2002", "Lei Federal 10406/2002"),
    ("cpp/L11340.html",  "Lei Federal",  "11340", "2006", "Lei Federal 11340/2006"),
]


def extrair_texto_planalto(html_path: Path) -> str:
    """
    Extractor robusto: usa get_text() no corpo completo,
    remove markup Planalto (cabeçalho, rodapé, tags de rasura),
    e filtra linhas curtas.
    """
    html = html_path.read_text(encoding="utf-8", errors="replace")
    soup = BeautifulSoup(html, "html.parser")

    # Remove elementos irrelevantes
    for tag in soup.find_all(["script", "style", "head", "nav", "header", "footer"]):
        tag.decompose()

    # Remove texto riscado (revogado)
    for tag in soup.find_all(["s", "strike", "del"]):
        tag.decompose()

    # Extrai texto completo do documento inteiro (alguns HTMLs do Planalto têm
    # o conteúdo dos artigos FORA da tag <body>, após </body></html>)
    texto = soup.get_text(separator="\n", strip=True)

    # Remove null bytes que PostgreSQL rejeita
    texto = texto.replace("\x00", "")

    # Filtra linhas com pelo menos 8 chars
    linhas = [l.strip() for l in texto.splitlines() if len(l.strip()) >= 8]

    # Remove duplicatas consecutivas
    resultado = []
    prev = None
    for l in linhas:
        if l != prev:
            resultado.append(l)
        prev = l

    return "\n".join(resultado)


def _get_conn():
    _load_env()
    sb_url = os.environ.get("SUPABASE_URL", "").rstrip("/")
    sb_key = os.environ.get("SUPABASE_SERVICE_KEY", "")
    if not sb_url or not sb_key:
        return None
    return {
        "url": sb_url,
        "headers": {
            "apikey": sb_key, "Authorization": f"Bearer {sb_key}",
            "Content-Type": "application/json",
            "Prefer": "resolution=merge-duplicates",
        },
    }


def main():
    conn = _get_conn()
    if not conn:
        print("ERRO: .env não configurado")
        sys.exit(1)

    for rel, tipo_ato, numero, ano, chave in LEIS:
        html_path = FONTES_DIR / rel.replace("/", os.sep)
        print(f"\n[>>] {chave}  ({html_path.name})")

        if not html_path.exists():
            print(f"     [SKIP] arquivo não encontrado")
            continue

        texto = extrair_texto_planalto(html_path)
        print(f"     Extraídos: {len(texto):,} chars · {texto.count(chr(10)):,} linhas")

        payload = {
            "esfera": "Federal", "tipo_ato": tipo_ato, "numero_ano": chave,
            "ementa": "", "texto_vigente": texto,
            "url_origem": f"vault://fontes/{rel}",
            "fragmentos_revogados": 0,
        }
        r = _req.post(
            f"{conn['url']}/rest/v1/legislacao_brasileira?on_conflict=numero_ano",
            json=payload, headers=conn["headers"], timeout=30,
        )
        if r.status_code in (200, 201):
            print(f"     [OK] upsert realizado")
        else:
            print(f"     [ERRO] HTTP {r.status_code}: {r.text[:200]}")

        time.sleep(0.3)

    print("\nConcluido.")


if __name__ == "__main__":
    main()

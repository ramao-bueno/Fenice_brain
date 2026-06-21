#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Monitor BDSF — Biblioteca Digital do Senado Federal
Scrapa novas publicações em https://www2.senado.leg.br/bdsf/
e gera notas no vault: 02_LEGISLACAO/BDSF/

Uso:
  python monitor_bdsf.py             # lista ultimas 20 publicacoes
  python monitor_bdsf.py --salvar    # salva notas no vault
  python monitor_bdsf.py --dias 7   # limita aos ultimos N dias
"""
import re
import sys
import time
import random
import argparse
from datetime import datetime, timedelta
from pathlib import Path

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www2.senado.leg.br/bdsf"
BROWSE_URL = f"{BASE_URL}/browse?type=dateissued&order=DESC&rpp=40&etal=0&value=&submit_browse=Atualizar"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; FeniceBot/1.0; +https://fenicejus.fenice.ia.br)",
    "Accept-Language": "pt-BR,pt;q=0.9",
}

VAULT_BDSF = Path(__file__).parent.parent / "02_LEGISLACAO" / "BDSF"


def _get(url: str, retries: int = 3) -> requests.Response | None:
    for i in range(retries):
        try:
            r = requests.get(url, headers=HEADERS, timeout=20)
            if r.status_code == 200:
                return r
            print(f"  HTTP {r.status_code}: {url}")
        except Exception as e:
            print(f"  Erro ({i+1}/{retries}): {e}")
        time.sleep(random.uniform(1.5, 3.0))
    return None


def listar_publicacoes(dias: int = 30) -> list[dict]:
    """Busca publicações recentes no BDSF."""
    r = _get(BROWSE_URL)
    if not r:
        print("Não foi possível acessar o BDSF.")
        return []

    soup = BeautifulSoup(r.text, "html.parser")
    itens = []
    limite = datetime.now() - timedelta(days=dias)

    for row in soup.select("table.miscTable tr"):
        cols = row.find_all("td")
        if len(cols) < 2:
            continue

        link_tag = cols[0].find("a")
        if not link_tag:
            continue

        titulo = link_tag.get_text(strip=True)
        href = link_tag.get("href", "")
        url = f"{BASE_URL}{href}" if href.startswith("/") else href

        data_str = cols[1].get_text(strip=True) if len(cols) > 1 else ""
        data = _parse_data(data_str)

        if data and data < limite:
            break

        itens.append({
            "titulo":    titulo,
            "url":       url,
            "data":      data_str,
            "data_obj":  data,
        })

    return itens


def _parse_data(texto: str) -> datetime | None:
    m = re.search(r"(\d{4})", texto)
    if m:
        try:
            return datetime(int(m.group(1)), 1, 1)
        except ValueError:
            pass
    return None


def gerar_nota(item: dict) -> str:
    hoje = datetime.now().strftime("%Y-%m-%d")
    titulo_slug = re.sub(r"[^a-z0-9-]", "-", item["titulo"].lower())[:60]

    fm = {
        "titulo":   item["titulo"],
        "fonte":    "BDSF — Biblioteca Digital do Senado Federal",
        "url":      item["url"],
        "data_pub": item["data"],
        "captura":  hoje,
        "tags":     ["bdsf", "senado", "legislacao", "doutrina-juridica"],
    }
    import yaml
    fm_str = yaml.dump(fm, allow_unicode=True, default_flow_style=False, sort_keys=False)

    return f"""---
{fm_str}---

# {item['titulo']}

**Fonte:** Biblioteca Digital do Senado Federal (BDSF)
**Data de publicação:** {item['data']}
**URL:** {item['url']}

---

## Resumo

[Inserir resumo após leitura do documento]

## Relevância para o Vault

[Como esta publicação se conecta com os temas estudados?]

## Links Relacionados

- [[02_LEGISLACAO/BDSF/index|Índice BDSF]]

---
_Capturado em: {hoje}_
"""


def main():
    parser = argparse.ArgumentParser(description="Monitor BDSF — Senado Federal")
    parser.add_argument("--dias", type=int, default=30, help="Janela de busca em dias")
    parser.add_argument("--salvar", action="store_true", help="Salvar notas no vault")
    args = parser.parse_args()

    sys.stdout.reconfigure(encoding="utf-8")
    print(f"Buscando publicações BDSF (últimos {args.dias} dias)...")
    itens = listar_publicacoes(dias=args.dias)

    if not itens:
        print("Nenhuma publicação encontrada.")
        return

    print(f"\n{len(itens)} publicações encontradas:\n")
    for i, item in enumerate(itens, 1):
        print(f"  {i:3}. [{item['data']}] {item['titulo'][:80]}")

    if args.salvar:
        VAULT_BDSF.mkdir(parents=True, exist_ok=True)
        salvas = 0
        for item in itens:
            slug = re.sub(r"[^a-z0-9-]", "-", item["titulo"].lower())[:60]
            path = VAULT_BDSF / f"BDSF-{item['data'][:4]}-{slug}.md"
            if not path.exists():
                path.write_text(gerar_nota(item), encoding="utf-8")
                salvas += 1
        print(f"\n{salvas} novas notas salvas em {VAULT_BDSF}")


if __name__ == "__main__":
    main()

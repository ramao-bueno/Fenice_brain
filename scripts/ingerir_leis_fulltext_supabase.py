#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Re-ingesta leis no Supabase com texto COMPLETO (sem truncamento de 5k/8k chars).
Usa HTML do cache local quando disponível; baixa do Planalto se necessário.

Uso: python scripts/ingerir_leis_fulltext_supabase.py
"""
import os
import re
import sys
import time
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
sys.stdout.reconfigure(encoding="utf-8")

from planalto_pipeline import baixar_html, parsear_lei, _load_env

# Leis: (numero, ano, tipo_ato, numero_ano_supabase, url_planalto)
LEIS = [
    # ── Já no DB, mas com texto truncado — re-ingesta completa ──────────────
    ("13105", "2015", "Lei Federal",
     "Lei Federal 13105/2015",
     "https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm"),
    ("8078",  "1990", "Lei Federal",
     "Lei Federal 8078/1990",
     "https://www.planalto.gov.br/ccivil_03/leis/l8078compilado.htm"),
    ("9307",  "1996", "Lei Federal",
     "Lei Federal 9307/1996",
     "https://www.planalto.gov.br/ccivil_03/leis/l9307.htm"),
    ("8072",  "1990", "Lei Federal",
     "Lei Federal 8072/1990",
     "https://www.planalto.gov.br/ccivil_03/leis/l8072.htm"),
    ("12850", "2013", "Lei Federal",
     "Lei Federal 12850/2013",
     "https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2013/lei/l12850.htm"),
    ("8429",  "1992", "Lei Federal",
     "Lei Federal 8429/1992",
     "https://www.planalto.gov.br/ccivil_03/leis/l8429.htm"),
    ("14230", "2021", "Lei Federal",
     "Lei Federal 14230/2021",
     "https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2021/lei/l14230.htm"),
    ("14133", "2021", "Lei Federal",
     "Lei Federal 14133/2021",
     "https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2021/lei/l14133.htm"),
    ("12016", "2009", "Lei Federal",
     "Lei Federal 12016/2009",
     "https://www.planalto.gov.br/ccivil_03/_ato2007-2010/2009/lei/l12016.htm"),
    ("9784",  "1999", "Lei Federal",
     "Lei Federal 9784/1999",
     "https://www.planalto.gov.br/ccivil_03/leis/l9784.htm"),
    ("12965", "2014", "Lei Federal",
     "Lei Federal 12965/2014",
     "https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2014/lei/l12965.htm"),
    ("13709", "2018", "Lei Federal",
     "Lei Federal 13709/2018",
     "https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm"),
    ("13146", "2015", "Lei Federal",
     "Lei Federal 13146/2015",
     "https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13146.htm"),
    ("8069",  "1990", "Lei Federal",
     "Lei Federal 8069/1990",
     "https://www.planalto.gov.br/ccivil_03/leis/l8069.htm"),
    ("9394",  "1996", "Lei Federal",
     "Lei Federal 9394/1996",
     "https://www.planalto.gov.br/ccivil_03/leis/l9394.htm"),
    # ── Novos — ainda não no DB ───────────────────────────────────────────────
    ("10406", "2002", "Lei Federal",
     "Lei Federal 10406/2002",
     "https://www.planalto.gov.br/ccivil_03/leis/2002/l10406compilada.htm"),
    ("11340", "2006", "Lei Federal",
     "Lei Federal 11340/2006",
     "https://www.planalto.gov.br/ccivil_03/_ato2003-2006/2006/lei/L11340.htm"),
    ("11343", "2006", "Lei Federal",
     "Lei Federal 11343/2006",
     "https://www.planalto.gov.br/ccivil_03/_ato2003-2006/2006/lei/L11343.htm"),
    ("8666",  "1993", "Lei Federal",
     "Lei Federal 8666/1993",
     "https://www.planalto.gov.br/ccivil_03/leis/L8666compilado.htm"),
    ("8112",  "1990", "Lei Federal",
     "Lei Federal 8112/1990",
     "https://www.planalto.gov.br/ccivil_03/leis/l8112cons.htm"),
    ("10741", "2003", "Lei Federal",
     "Lei Federal 10741/2003",
     "https://www.planalto.gov.br/ccivil_03/leis/2003/L10741.htm"),
    # ── Decretos-Lei ──────────────────────────────────────────────────────────
    ("2848",  "1940", "Decreto-Lei",
     "Decreto-Lei 2848/1940",
     "https://www.planalto.gov.br/ccivil_03/decreto-lei/del2848compilado.htm"),
    ("3689",  "1941", "Decreto-Lei",
     "Decreto-Lei 3689/1941",
     "https://www.planalto.gov.br/ccivil_03/decreto-lei/del3689compilado.htm"),
]


def _get_conn():
    _load_env()
    url = os.environ.get("SUPABASE_URL", "").rstrip("/")
    key = os.environ.get("SUPABASE_SERVICE_KEY", "")
    if not url or not key:
        return None
    return {
        "url": url,
        "headers": {
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Prefer": "resolution=merge-duplicates",
        },
    }


def upsert(conn: dict, payload: dict) -> bool:
    import requests as _req
    try:
        r = _req.post(
            f"{conn['url']}/rest/v1/legislacao_brasileira?on_conflict=numero_ano",
            json=payload,
            headers=conn["headers"],
            timeout=30,
        )
        if r.status_code in (200, 201):
            return True
        print(f"     HTTP {r.status_code}: {r.text[:300]}")
        return False
    except Exception as e:
        print(f"     Erro de rede: {e}")
        return False


def main():
    conn = _get_conn()
    if not conn:
        print("ERRO: SUPABASE_URL / SUPABASE_SERVICE_KEY não definidos no .env")
        sys.exit(1)

    print("=" * 65)
    print("INGESTÃO FULLTEXT — Texto integral das leis ao Supabase")
    print("=" * 65)

    ok = erro = 0

    for numero, ano_str, tipo_ato, chave, url in LEIS:
        print(f"\n[>>] {chave}")

        caminho_html = baixar_html(url, forcar=False)
        if not caminho_html:
            print(f"     [ERRO] HTML não encontrado em: {url}")
            erro += 1
            continue

        try:
            dados = parsear_lei(caminho_html, url_origem=url)
            texto = dados.get("texto_vigente", "")
            ementa = dados.get("ementa", "") or ""

            if not texto and not ementa:
                print(f"     [ERRO] Sem texto extraído do HTML")
                erro += 1
                continue

            payload = {
                "esfera":               "Federal",
                "tipo_ato":             tipo_ato,
                "numero_ano":           chave,
                "ementa":               ementa,
                "texto_vigente":        texto,
                "url_origem":           url,
                "fragmentos_revogados": len(dados.get("fragmentos_revogados", [])),
            }

            if upsert(conn, payload):
                print(f"     [OK] {len(texto):,} chars · {len(texto.split(chr(10))):,} linhas")
                ok += 1
            else:
                erro += 1

        except Exception as e:
            print(f"     [ERRO] {e}")
            erro += 1

        time.sleep(0.8)

    print()
    print("=" * 65)
    print(f"Concluído: {ok} inseridos/atualizados | {erro} erros")
    print()
    print("Próximo passo:")
    print("  Recarrega o site (Ctrl+F5) e testa CPC Art. 235 → deve aparecer.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ingesta TODOS os HTMLs locais de scripts/fontes/ → Supabase (texto integral).
Uso: python scripts/ingerir_fontes_locais.py
"""
import os
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
sys.stdout.reconfigure(encoding="utf-8")

from planalto_pipeline import parsear_lei, _load_env

FONTES_DIR = PROJECT_ROOT / "scripts" / "fontes"

# Mapeamento explícito: caminho relativo → (tipo_ato, numero, ano)
MAPA = {
    # ── Código Civil ────────────────────────────────────────────────────────
    "cc/L10406.html":          ("Lei Federal",       "10406", "2002"),
    "cc/L13655.html":          ("Lei Federal",       "13655", "2018"),
    "cc/L4657.html":           ("Lei Federal",       "4657",  "1942"),
    # ── CDC ─────────────────────────────────────────────────────────────────
    "cdc/L8078.html":          ("Lei Federal",       "8078",  "1990"),
    # ── Constitucional / CF ─────────────────────────────────────────────────
    "cf/CF88.html":            ("Constituição",      "CF88",  "1988"),
    "cf/L11417.html":          ("Lei Federal",       "11417", "2006"),
    "cf/L12016.html":          ("Lei Federal",       "12016", "2009"),
    "cf/L13300.html":          ("Lei Federal",       "13300", "2016"),
    "cf/L4717.html":           ("Lei Federal",       "4717",  "1965"),
    "cf/L9507.html":           ("Lei Federal",       "9507",  "1997"),
    "cf/L9709.html":           ("Lei Federal",       "9709",  "1998"),
    "cf/L9868.html":           ("Lei Federal",       "9868",  "1999"),
    "cf/L9882.html":           ("Lei Federal",       "9882",  "1999"),
    "cf/LCP95.html":           ("Lei Complementar",  "95",    "1998"),
    # ── Penal ───────────────────────────────────────────────────────────────
    "cp/DEL2848.html":         ("Decreto-Lei",       "2848",  "1940"),
    "cp/L11343.html":          ("Lei Federal",       "11343", "2006"),
    "cp/L12850.html":          ("Lei Federal",       "12850", "2013"),
    "cp/L14132.html":          ("Lei Federal",       "14132", "2021"),
    "cp/L14155.html":          ("Lei Federal",       "14155", "2021"),
    "cp/L14811.html":          ("Lei Federal",       "14811", "2024"),
    "cp/L7492.html":           ("Lei Federal",       "7492",  "1986"),
    "cp/L8072.html":           ("Lei Federal",       "8072",  "1990"),
    "cp/L8137.html":           ("Lei Federal",       "8137",  "1990"),
    "cp/L9605.html":           ("Lei Federal",       "9605",  "1998"),
    "cp/L9613.html":           ("Lei Federal",       "9613",  "1998"),
    # ── CPC ─────────────────────────────────────────────────────────────────
    "cpc/L13105.html":         ("Lei Federal",       "13105", "2015"),
    # ── Processo Penal / Execução ────────────────────────────────────────────
    "cpp/DEL3689.html":        ("Decreto-Lei",       "3689",  "1941"),
    "cpp/L11340.html":         ("Lei Federal",       "11340", "2006"),
    "cpp/L13869.html":         ("Lei Federal",       "13869", "2019"),
    "cpp/L13964.html":         ("Lei Federal",       "13964", "2019"),
    "cpp/L7210.html":          ("Lei Federal",       "7210",  "1984"),
    "cpp/L7960.html":          ("Lei Federal",       "7960",  "1989"),
    "cpp/L9099.html":          ("Lei Federal",       "9099",  "1995"),
    # ── Especial / Previdência / Autoral ────────────────────────────────────
    "especial/L8212.html":     ("Lei Federal",       "8212",  "1991"),
    "especial/L8213.html":     ("Lei Federal",       "8213",  "1991"),
    "especial/L9609.html":     ("Lei Federal",       "9609",  "1998"),
    "especial/L9610.html":     ("Lei Federal",       "9610",  "1998"),
    # ── Internacional ───────────────────────────────────────────────────────
    "internacional/D592.html":    ("Decreto",        "592",   "1992"),
    "internacional/D6949.html":   ("Decreto",        "6949",  "2009"),
    "internacional/D7030.html":   ("Decreto",        "7030",  "2009"),
    "internacional/L13445.html":  ("Lei Federal",    "13445", "2017"),
    "internacional/L9307.html":   ("Lei Federal",    "9307",  "1996"),
    # ── Público ─────────────────────────────────────────────────────────────
    "publico/L12527.html":     ("Lei Federal",       "12527", "2011"),
    "publico/L8112.html":      ("Lei Federal",       "8112",  "1990"),
    "publico/L8429.html":      ("Lei Federal",       "8429",  "1992"),
    "publico/L9784.html":      ("Lei Federal",       "9784",  "1999"),
}


def _get_conn():
    _load_env()
    sb_url = os.environ.get("SUPABASE_URL", "").rstrip("/")
    sb_key  = os.environ.get("SUPABASE_SERVICE_KEY", "")
    if not sb_url or not sb_key:
        return None
    return {
        "url": sb_url,
        "headers": {
            "apikey": sb_key,
            "Authorization": f"Bearer {sb_key}",
            "Content-Type": "application/json",
            "Prefer": "resolution=merge-duplicates",
        },
    }


def upsert(conn, payload):
    import requests as _req
    r = _req.post(
        f"{conn['url']}/rest/v1/legislacao_brasileira?on_conflict=numero_ano",
        json=payload,
        headers=conn["headers"],
        timeout=30,
    )
    return r.status_code in (200, 201), r.status_code, r.text[:200]


def main():
    conn = _get_conn()
    if not conn:
        print("ERRO: SUPABASE_URL / SUPABASE_SERVICE_KEY não definidos no .env")
        sys.exit(1)

    print("=" * 68)
    print("INGESTÃO FONTES LOCAIS — texto integral → Supabase")
    print("=" * 68)

    ok = erro = 0

    for rel_path, (tipo_ato, numero, ano) in MAPA.items():
        html_path = FONTES_DIR / rel_path.replace("/", os.sep)
        if tipo_ato == "Constituição":
            chave = f"Constituição Federal {ano}"
        elif tipo_ato == "Lei Complementar":
            chave = f"Lei Complementar {numero}/{ano}"
        elif tipo_ato == "Decreto":
            chave = f"Decreto {numero}/{ano}"
        else:
            chave = f"{tipo_ato} {numero}/{ano}"

        print(f"\n[>>] {chave}")

        if not html_path.exists():
            print(f"     [SKIP] arquivo não encontrado: {html_path.name}")
            continue

        try:
            dados = parsear_lei(html_path, url_origem=str(html_path))
            texto  = dados.get("texto_vigente", "")
            ementa = dados.get("ementa", "") or ""

            payload = {
                "esfera":               "Federal",
                "tipo_ato":             tipo_ato,
                "numero_ano":           chave,
                "ementa":               ementa,
                "texto_vigente":        texto,
                "url_origem":           f"vault://fontes/{rel_path}",
                "fragmentos_revogados": len(dados.get("fragmentos_revogados", [])),
            }

            ok_flag, status, msg = upsert(conn, payload)
            if ok_flag:
                print(f"     [OK] {len(texto):,} chars")
                ok += 1
            else:
                print(f"     [ERRO] HTTP {status}: {msg}")
                erro += 1

        except Exception as e:
            print(f"     [ERRO] {e}")
            erro += 1

        time.sleep(0.3)

    print()
    print("=" * 68)
    print(f"Concluído: {ok} ok | {erro} erros")
    print()
    print("Proximos passos:")
    print("  1. Atualizar dbKeys no landing.html para as novas leis")
    print("  2. Deploy → vercel --prod")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
import os, time
from pathlib import Path
from planalto_pipeline import baixar_html, parsear_lei, _load_env

_load_env()
sb_url = os.environ.get("SUPABASE_URL", "").rstrip("/")
sb_key = os.environ.get("SUPABASE_SERVICE_KEY", "")
hdrs = {
    "apikey": sb_key, "Authorization": f"Bearer {sb_key}",
    "Content-Type": "application/json",
    "Prefer": "resolution=merge-duplicates",
}

import requests as _req

LEIS = [
    ("10406", "2002", "Lei Federal", "Lei Federal 10406/2002",
     "https://www.planalto.gov.br/ccivil_03/leis/2002/L10406.htm"),
    ("8666",  "1993", "Lei Federal", "Lei Federal 8666/1993",
     "https://www.planalto.gov.br/ccivil_03/leis/l8666cons.htm"),
]

for numero, ano, tipo, chave, url in LEIS:
    print(f"[>>] {chave}")
    p = baixar_html(url, forcar=True)
    if not p:
        print(f"     [ERRO] 404")
        continue
    d = parsear_lei(p, url_origem=url)
    texto = d.get("texto_vigente", "")
    payload = {
        "esfera": "Federal", "tipo_ato": tipo, "numero_ano": chave,
        "ementa": d.get("ementa", ""),
        "texto_vigente": texto,
        "url_origem": url,
        "fragmentos_revogados": len(d.get("fragmentos_revogados", [])),
    }
    r = _req.post(
        f"{sb_url}/rest/v1/legislacao_brasileira?on_conflict=numero_ano",
        json=payload, headers=hdrs, timeout=30,
    )
    if r.status_code in (200, 201):
        print(f"     [OK] {len(texto):,} chars")
    else:
        print(f"     [ERRO] HTTP {r.status_code}: {r.text[:200]}")
    time.sleep(0.5)

print("Concluido.")

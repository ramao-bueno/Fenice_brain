#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Popula a tabela `artigos` a partir de `legislacao_brasileira.texto_vigente`.
Cada artigo vira uma linha indexada por (lei, numero).

Uso: python scripts/indexar_artigos.py
"""
import os, re, sys, time
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from planalto_pipeline import _load_env
import requests as _req

_load_env()
SB_URL = os.environ.get("SUPABASE_URL", "").rstrip("/")
SB_KEY = os.environ.get("SUPABASE_SERVICE_KEY", "")

HDRS_READ = {
    "apikey": SB_KEY, "Authorization": f"Bearer {SB_KEY}",
}
HDRS_WRITE = {
    **HDRS_READ,
    "Content-Type": "application/json",
    "Prefer": "resolution=merge-duplicates",
}


def listar_leis():
    """Retorna todas as leis com texto_vigente não vazio."""
    leis = []
    offset = 0
    limite = 100
    while True:
        r = _req.get(
            f"{SB_URL}/rest/v1/legislacao_brasileira",
            headers=HDRS_READ,
            params={
                "select": "numero_ano,texto_vigente",
                "texto_vigente": "neq.",
                "order": "numero_ano",
                "limit": str(limite),
                "offset": str(offset),
            },
            timeout=30,
        )
        r.raise_for_status()
        chunk = r.json()
        if not chunk:
            break
        leis.extend(chunk)
        offset += len(chunk)
        if len(chunk) < limite:
            break
    return leis


def parsear_artigos(numero_ano: str, texto: str) -> list[dict]:
    """Divide texto em artigos pelo início de linha 'Art. N'."""
    artigos = []
    atual_num = None
    atual_linhas = []

    for linha in texto.splitlines():
        m = re.match(r'^Art\.?\s*(\d+)', linha, re.IGNORECASE)
        if m:
            if atual_num is not None:
                artigos.append({
                    "lei":    numero_ano,
                    "numero": atual_num,
                    "texto":  "\n".join(atual_linhas).strip(),
                })
            atual_num = int(m.group(1))
            atual_linhas = [linha]
        elif atual_num is not None:
            atual_linhas.append(linha)

    if atual_num is not None and atual_linhas:
        artigos.append({
            "lei":    numero_ano,
            "numero": atual_num,
            "texto":  "\n".join(atual_linhas).strip(),
        })

    return artigos


def upsert_batch(batch: list[dict]) -> bool:
    r = _req.post(
        f"{SB_URL}/rest/v1/artigos?on_conflict=lei,numero",
        json=batch,
        headers=HDRS_WRITE,
        timeout=60,
    )
    if r.status_code not in (200, 201):
        print(f"     [ERRO] HTTP {r.status_code}: {r.text[:200]}")
        return False
    return True


def main():
    if not SB_URL or not SB_KEY:
        print("ERRO: SUPABASE_URL / SUPABASE_SERVICE_KEY não definidos no .env")
        sys.exit(1)

    print("=" * 65)
    print("INDEXAÇÃO DE ARTIGOS → tabela `artigos`")
    print("=" * 65)

    leis = listar_leis()
    print(f"Leis com texto: {len(leis)}")

    total_arts = 0
    total_leis_ok = 0

    for lei in leis:
        chave = lei["numero_ano"]
        texto = lei.get("texto_vigente") or ""
        if not texto.strip():
            continue

        artigos = parsear_artigos(chave, texto)
        if not artigos:
            print(f"  [SKIP] {chave} — nenhum artigo encontrado")
            continue

        # Deduplica: mantém apenas o primeiro artigo de cada número
        vistos: set = set()
        artigos_unicos = []
        for a in artigos:
            if a["numero"] not in vistos:
                vistos.add(a["numero"])
                artigos_unicos.append(a)
        artigos = artigos_unicos

        print(f"  [>>] {chave} → {len(artigos)} artigos", end="", flush=True)

        # upsert em lotes de 200
        ok = True
        for i in range(0, len(artigos), 200):
            lote = artigos[i:i+200]
            if not upsert_batch(lote):
                ok = False
                break

        if ok:
            print(f" ✓")
            total_arts += len(artigos)
            total_leis_ok += 1
        else:
            print(f" ERRO")

        time.sleep(0.2)

    print()
    print("=" * 65)
    print(f"Concluído: {total_leis_ok} leis · {total_arts:,} artigos indexados")


if __name__ == "__main__":
    main()

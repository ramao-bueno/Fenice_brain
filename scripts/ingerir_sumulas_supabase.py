#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ingestão de Súmulas STJ e STF → Supabase (tabela legislacao_brasileira).
Uso: python scripts/ingerir_sumulas_supabase.py
"""

import os
import re
import sys
from pathlib import Path

import yaml
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

VAULT = Path(__file__).parent.parent

MODULOS = [
    {
        "pasta":    VAULT / "00_APEX" / "SUMULAS STJ" / "Sumulas",
        "tipo_ato": "Súmula STJ",
        "prefixo":  "stj",
    },
    {
        "pasta":    VAULT / "00_APEX" / "SUMULAS STF" / "Sumulas",
        "tipo_ato": "Súmula STF",
        "prefixo":  "stf",
    },
]

RE_TEXTO = re.compile(
    r"## TEXTO DA S[UÚ]MULA\s*\n+((?:>.*\n?)+)",
    re.IGNORECASE,
)


def extrair_texto_sumula(conteudo: str) -> str:
    m = RE_TEXTO.search(conteudo)
    if not m:
        return ""
    linhas = m.group(1).strip().splitlines()
    return " ".join(l.lstrip("> ").strip() for l in linhas if l.strip()).strip()


def parse_md(path: Path) -> dict | None:
    raw = path.read_text(encoding="utf-8")

    # --- frontmatter ---
    if not raw.startswith("---"):
        return None
    fim = raw.index("---", 3)
    fm = yaml.safe_load(raw[3:fim]) or {}

    numero   = str(fm.get("sumula", "")).strip()
    tribunal = str(fm.get("tribunal", "")).strip().upper()
    status   = str(fm.get("status", "vigente")).strip().lower()
    data_apr = fm.get("data_aprovacao") or fm.get("julgado_em") or None

    if not numero or not tribunal:
        return None

    tipo_ato  = f"Súmula {tribunal}"
    numero_ano = f"Súmula {tribunal} {numero.zfill(3)}"
    ementa     = extrair_texto_sumula(raw)
    url_origem = f"vault://{tribunal.lower()}/sumula-{numero.zfill(4)}"

    data_str = None
    if data_apr:
        partes = str(data_apr).split("/")
        if len(partes) == 3:
            try:
                data_str = f"{partes[2]}-{partes[1]}-{partes[0]}"
            except Exception:
                pass

    return {
        "esfera":       "Federal",
        "tipo_ato":     tipo_ato,
        "numero_ano":   numero_ano,
        "ementa":       ementa or None,
        "texto_vigente": ementa or "",
        "url_origem":   url_origem,
        "data_assinatura": data_str,
        "fragmentos_revogados": 1 if "revogad" in status else 0,
    }


def main():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_SERVICE_KEY")
    if not url or not key:
        print("ERRO: SUPABASE_URL ou SUPABASE_SERVICE_KEY não definidos no .env")
        sys.exit(1)

    sb = create_client(url, key)

    total_ok  = 0
    total_err = 0

    for mod in MODULOS:
        pasta = mod["pasta"]
        if not pasta.exists():
            print(f"[AVISO] Pasta não encontrada: {pasta}")
            continue

        arquivos = sorted(pasta.glob("*.md"))
        print(f"\n{mod['tipo_ato']}: {len(arquivos)} arquivos em {pasta.name}/")

        batch = []
        for f in arquivos:
            rec = parse_md(f)
            if rec:
                batch.append(rec)
            else:
                print(f"  [SKIP] {f.name}")

        # upsert em lotes de 200
        for i in range(0, len(batch), 200):
            chunk = batch[i:i+200]
            try:
                sb.table("legislacao_brasileira").upsert(
                    chunk,
                    on_conflict="numero_ano"
                ).execute()
                total_ok += len(chunk)
                print(f"  [OK] {i+len(chunk)}/{len(batch)} inseridos")
            except Exception as e:
                total_err += len(chunk)
                print(f"  [ERRO] lote {i}-{i+len(chunk)}: {e}")

    print(f"\n{'='*50}")
    print(f"Concluído: {total_ok} registros inseridos, {total_err} erros.")


if __name__ == "__main__":
    main()

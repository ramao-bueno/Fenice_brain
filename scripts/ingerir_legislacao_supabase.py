#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ingestao de 02_LEGISLACAO/Leis/*.md -> Supabase (legislacao_brasileira).
Uso: python scripts/ingerir_legislacao_supabase.py
"""

import os
import re
import sys
from pathlib import Path

import yaml
from dotenv import load_dotenv
from supabase import create_client

VAULT = Path(__file__).parent.parent
load_dotenv(VAULT / ".env")

PASTA_LEIS = VAULT / "02_LEGISLACAO" / "Leis"

RE_TEXTO = re.compile(r"## TEXTO VIGENTE\s*\n+([\s\S]+?)(?=\n## |\Z)", re.IGNORECASE)


def extrair_texto(conteudo: str) -> str:
    m = RE_TEXTO.search(conteudo)
    if not m:
        return ""
    texto = m.group(1).strip()
    # remove callouts Obsidian
    texto = re.sub(r"> \[!.*?\].*?\n(> .*?\n)*", "", texto)
    texto = re.sub(r"^> ", "", texto, flags=re.MULTILINE)
    return texto[:8000].strip()


def parse_md(path: Path) -> dict | None:
    raw = path.read_text(encoding="utf-8")
    if not raw.startswith("---"):
        return None
    fim = raw.index("---", 3)
    fm = yaml.safe_load(raw[3:fim]) or {}

    lei  = str(fm.get("lei", "")).strip()
    ano  = str(fm.get("ano", "")).strip()
    tipo = str(fm.get("tipo", "lei-federal")).strip()
    url  = str(fm.get("url_origem", "")).strip()

    if not lei or not ano:
        return None

    tipo_map = {
        "lei-federal":    "Lei Federal",
        "decreto":        "Decreto",
        "decreto-lei":    "Decreto-Lei",
        "lei-complementar": "Lei Complementar",
        "medida-provisoria": "Medida Provisória",
    }
    tipo_ato  = tipo_map.get(tipo, "Lei Federal")
    numero_ano = f"{tipo_ato} {lei}/{ano}"
    ementa     = str(fm.get("ementa", "")).strip() or None
    frags      = int(fm.get("fragmentos_revogados", 0) or 0)
    texto      = extrair_texto(raw)

    return {
        "esfera":               "Federal",
        "tipo_ato":             tipo_ato,
        "numero_ano":           numero_ano,
        "ementa":               ementa,
        "texto_vigente":        texto or ementa or "",
        "url_origem":           url or f"vault://lei/{lei}-{ano}",
        "fragmentos_revogados": frags,
    }


def main():
    url_sb = os.environ.get("SUPABASE_URL")
    key_sb = os.environ.get("SUPABASE_SERVICE_KEY")
    if not url_sb or not key_sb:
        print("ERRO: SUPABASE_URL ou SUPABASE_SERVICE_KEY nao definidos no .env")
        sys.exit(1)

    sb = create_client(url_sb, key_sb)

    arquivos = sorted(PASTA_LEIS.glob("*.md"))
    print(f"Legislacao: {len(arquivos)} arquivos em {PASTA_LEIS.name}/")

    batch = []
    for f in arquivos:
        rec = parse_md(f)
        if rec:
            batch.append(rec)
        else:
            print(f"  [SKIP] {f.name}")

    if not batch:
        print("Nenhum registro para inserir.")
        return

    total_ok = 0
    total_err = 0
    for i in range(0, len(batch), 200):
        chunk = batch[i:i+200]
        try:
            sb.table("legislacao_brasileira").upsert(
                chunk, on_conflict="numero_ano"
            ).execute()
            total_ok += len(chunk)
            print(f"  [OK] {i+len(chunk)}/{len(batch)} inseridos/atualizados")
        except Exception as e:
            total_err += len(chunk)
            print(f"  [ERRO] lote {i}-{i+len(chunk)}: {e}")

    print(f"\n{'='*50}")
    print(f"Concluido: {total_ok} registros, {total_err} erros.")


if __name__ == "__main__":
    main()

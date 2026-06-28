#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Indexa Súmulas STF e STJ na tabela `artigos` do Supabase.
Lê as notas Obsidian de 00_APEX/SUMULAS STF|STJ/Sumulas/*.md

Uso:
    python scripts/indexar_sumulas.py           # indexa tudo
    python scripts/indexar_sumulas.py STF       # só STF
    python scripts/indexar_sumulas.py STJ       # só STJ
    python scripts/indexar_sumulas.py --dry     # só conta, não envia
"""
import os, re, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from planalto_pipeline import _load_env
import requests as _req

_load_env()
SB_URL = os.environ.get("SUPABASE_URL", "").rstrip("/")
SB_KEY = os.environ.get("SUPABASE_SERVICE_KEY", "")
HDRS = {
    "apikey": SB_KEY,
    "Authorization": f"Bearer {SB_KEY}",
    "Content-Type": "application/json",
    "Prefer": "resolution=merge-duplicates",
}

FONTES = {
    "STF": (PROJECT_ROOT / "00_APEX" / "SUMULAS STF" / "Sumulas", "Súmula STF"),
    "STJ": (PROJECT_ROOT / "00_APEX" / "SUMULAS STJ" / "Sumulas", "Súmula STJ"),
}


def _extrair_frontmatter(texto: str) -> dict:
    m = re.match(r"^---\s*\n(.*?)\n---", texto, re.DOTALL)
    if not m:
        return {}
    fm = {}
    for linha in m.group(1).splitlines():
        if ":" in linha:
            k, _, v = linha.partition(":")
            fm[k.strip()] = v.strip().strip("'\"")
    return fm


def _extrair_texto_sumula(conteudo: str) -> str:
    # Busca bloco após "## TEXTO DA SUMULA" ou "## TEXTO DA SÚMULA"
    m = re.search(
        r"##\s+TEXTO\s+DA\s+S[UÚ]MULA\s*\n+(.+?)(?:\n---|\n##|\Z)",
        conteudo, re.DOTALL | re.IGNORECASE
    )
    if not m:
        return ""
    bloco = m.group(1)
    # Extrai linhas de blockquote (> texto)
    linhas = []
    for linha in bloco.splitlines():
        linha = linha.strip()
        if linha.startswith(">"):
            linhas.append(linha.lstrip("> ").strip())
    texto = " ".join(linhas).strip()
    return texto


def _processar_pasta(pasta: Path, lei_chave: str) -> list[dict]:
    artigos = []
    ignorados = 0

    for md in sorted(pasta.glob("*.md")):
        if md.name.startswith("_"):
            continue

        try:
            conteudo = md.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            print(f"  [ERRO leitura] {md.name}: {e}")
            continue

        fm = _extrair_frontmatter(conteudo)
        status = fm.get("status", "vigente").lower()
        if status not in ("vigente", ""):
            ignorados += 1
            continue

        num_str = fm.get("sumula", "")
        if not num_str:
            m = re.search(r"(\d+)", md.stem)
            num_str = m.group(1) if m else "0"

        try:
            num = int(num_str)
        except ValueError:
            continue

        texto = _extrair_texto_sumula(conteudo)
        if not texto:
            print(f"  [AVISO] {md.name}: texto vazio")
            continue

        artigos.append({"lei": lei_chave, "numero": num, "texto": texto})

    if ignorados:
        print(f"  {ignorados} superadas/canceladas ignoradas")

    artigos.sort(key=lambda x: x["numero"])
    return artigos


def _upsert(artigos: list[dict]) -> int:
    enviados = 0
    for i in range(0, len(artigos), 100):
        lote = artigos[i:i + 100]
        r = _req.post(
            f"{SB_URL}/rest/v1/artigos?on_conflict=lei,numero",
            json=lote, headers=HDRS, timeout=60,
        )
        if r.status_code not in (200, 201):
            print(f"  [ERRO lote {i//100+1}] HTTP {r.status_code}: {r.text[:120]}")
        else:
            enviados += len(lote)
        time.sleep(0.1)
    return enviados


def main():
    if not SB_URL or not SB_KEY:
        print("ERRO: SUPABASE_URL / SUPABASE_SERVICE_KEY não definidos no .env")
        sys.exit(1)

    dry = "--dry" in sys.argv
    filtro = next((a.upper() for a in sys.argv[1:] if a not in ("--dry",)), None)

    total = 0
    for tribunal, (pasta, lei_chave) in FONTES.items():
        if filtro and filtro != tribunal:
            continue

        print(f"\n{'='*60}")
        print(f"Súmulas {tribunal} → lei='{lei_chave}'")
        print(f"Pasta: {pasta}")
        print(f"{'='*60}")

        if not pasta.exists():
            print("  [ERRO] Pasta não encontrada")
            continue

        artigos = _processar_pasta(pasta, lei_chave)
        print(f"  {len(artigos)} súmulas vigentes extraídas")

        if dry:
            if artigos:
                print(f"  Exemplo: #{artigos[0]['numero']} — {artigos[0]['texto'][:80]}…")
            continue

        enviados = _upsert(artigos)
        print(f"  ✓ {enviados} enviadas ao Supabase")
        total += enviados
        time.sleep(0.3)

    if not dry:
        print(f"\n{'='*60}")
        print(f"CONCLUÍDO: {total} súmulas indexadas no total")
        print(f"{'='*60}")


if __name__ == "__main__":
    main()

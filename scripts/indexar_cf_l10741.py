#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Indexa CF/88 (completa) e Estatuto do Idoso L10741/2003 na tabela `artigos`.

Uso:
    python scripts/indexar_cf_l10741.py
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


def _limpar_html(html: str) -> str:
    """Remove tags, revogados e normaliza espaços."""
    html = re.sub(r"<s\b[^>]*>.*?</s>", " ", html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r"<del\b[^>]*>.*?</del>", " ", html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r"<(?:div|p|br|h[1-6]|li|tr|td|th|section|article)\b[^>]*>",
                  "\n", html, flags=re.IGNORECASE)
    texto = re.sub(r"<[^>]+>", " ", html)
    texto = texto.replace("&nbsp;", " ").replace("&amp;", "&")
    texto = texto.replace("&lt;", "<").replace("&gt;", ">")
    texto = texto.replace("&quot;", '"').replace("&#39;", "'")
    texto = re.sub(r"&[a-z#0-9]+;", " ", texto)
    texto = re.sub(r"[ \t]+", " ", texto)
    texto = re.sub(r"\n{3,}", "\n\n", texto)
    return texto.strip()


def _extrair_artigos(texto: str, lei_chave: str, max_art: int) -> list[dict]:
    """Divide texto por marcadores 'Art. N' e retorna lista de dicts para Supabase."""
    marcadores = list(re.finditer(
        r"(?:^|\n)\s*Art\.\s*(\d+)\s*[ºo°]?",
        texto, re.MULTILINE
    ))
    print(f"  {len(marcadores)} marcadores de artigo detectados")

    vistos: set[int] = set()
    artigos = []

    for i, m in enumerate(marcadores):
        num = int(m.group(1))
        if num in vistos or num > max_art:
            continue
        vistos.add(num)

        inicio = m.start()
        fim = marcadores[i + 1].start() if i + 1 < len(marcadores) else len(texto)
        bloco = texto[inicio:fim].strip()
        bloco = re.sub(r"\s+", " ", bloco).strip()

        # Remove "Art. N[º]" do início
        corpo = re.sub(r"^Art\.\s*\d+\s*[ºo°]?\s*[-–—.]?\s*", "", bloco).strip()

        artigos.append({"lei": lei_chave, "numero": num, "texto": corpo})

    artigos.sort(key=lambda x: x["numero"])
    return artigos


def _upsert(artigos: list[dict]) -> int:
    enviados = 0
    for i in range(0, len(artigos), 100):
        lote = artigos[i:i + 100]
        r = _req.post(
            f"{SB_URL}/rest/v1/artigos?on_conflict=lei,numero",
            json=lote,
            headers=HDRS,
            timeout=60,
        )
        if r.status_code not in (200, 201):
            print(f"  [ERRO] lote {i//100+1}: HTTP {r.status_code}: {r.text[:200]}")
        else:
            enviados += len(lote)
        time.sleep(0.1)
    return enviados


def _baixar_html(urls: list[str], cache: Path, encoding="windows-1252") -> str | None:
    if cache.exists():
        print(f"  Cache local: {cache.name}")
        return cache.read_text(encoding="utf-8", errors="replace")

    for url in urls:
        try:
            print(f"  Baixando: {url}")
            r = _req.get(url, headers={"User-Agent": "Mozilla/5.0 (Fenice Brain / Estudo Juridico)"}, timeout=90)
            if r.status_code == 200:
                html = r.content.decode(encoding, errors="replace")
                cache.write_text(html, encoding="utf-8")
                print(f"  OK — {len(html):,} chars (cache salvo)")
                return html
        except Exception as e:
            print(f"  Falha em {url}: {e}")
    return None


# ── CF/88 ──────────────────────────────────────────────────────────────────────

def indexar_cf88() -> int:
    print("\n" + "=" * 60)
    print("CF/88 → tabela artigos (completa)")
    print("=" * 60)

    cache = PROJECT_ROOT / "scripts" / "_cache_cf_planalto.html"
    html = _baixar_html(
        ["https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm"],
        cache,
    )
    if not html:
        print("[ERRO] Não foi possível baixar a CF/88")
        return 0

    texto = _limpar_html(html)
    artigos = _extrair_artigos(texto, "Constituição Federal 1988", max_art=250)
    print(f"  {len(artigos)} artigos extraídos")

    enviados = _upsert(artigos)
    print(f"  ✓ {enviados} artigos no Supabase")
    return enviados


# ── L10741 ─────────────────────────────────────────────────────────────────────

def indexar_l10741() -> int:
    print("\n" + "=" * 60)
    print("Lei 10741/2003 (Estatuto do Idoso) → tabela artigos")
    print("=" * 60)

    # Fontes locais (vault + OneDrive) — consultadas antes do Planalto
    FONTES_LOCAIS = [
        PROJECT_ROOT / "08_ENSINO" / "Uniasselvi" / "Biblioteca" / "L10741 - nova lei do idoso.html",
        Path(r"E:\Users\oicon\OneDrive\Allah - Islamismo\Ramão\Uniasselvi\cursos livres\Biblioteca\L10741 - nova lei do idoso.html"),
    ]

    html = None
    for fonte in FONTES_LOCAIS:
        if fonte.exists():
            print(f"  Fonte local: {fonte}")
            try:
                html = fonte.read_text(encoding="utf-8", errors="replace")
                print(f"  Lido: {len(html):,} chars")
                # Copia para o vault se não estiver lá ainda
                vault_dest = PROJECT_ROOT / "08_ENSINO" / "Uniasselvi" / "Biblioteca" / "L10741 - nova lei do idoso.html"
                if not vault_dest.exists():
                    vault_dest.write_text(html, encoding="utf-8")
                    print(f"  Copiado para vault: {vault_dest.name}")
                break
            except Exception as e:
                print(f"  Erro ao ler {fonte.name}: {e}")

    if not html:
        cache_dir = PROJECT_ROOT / "scripts" / "_cache_planalto"
        cache_dir.mkdir(parents=True, exist_ok=True)
        cache = cache_dir / "l10741.htm"
        html = _baixar_html(
            [
                "https://www.planalto.gov.br/ccivil_03/_ato2003-2006/2003/lei/l10741.htm",
                "https://www.planalto.gov.br/ccivil_03/_ato2003-2006/2003/lei/L10741.htm",
            ],
            cache,
        )
    if not html:
        print("[ERRO] Não foi possível baixar a Lei 10741/2003")
        return 0

    texto = _limpar_html(html)
    artigos = _extrair_artigos(texto, "Lei Federal 10741/2003", max_art=120)
    print(f"  {len(artigos)} artigos extraídos")

    enviados = _upsert(artigos)
    print(f"  ✓ {enviados} artigos no Supabase")
    return enviados


if __name__ == "__main__":
    if not SB_URL or not SB_KEY:
        print("ERRO: SUPABASE_URL / SUPABASE_SERVICE_KEY não definidos no .env")
        sys.exit(1)

    total = indexar_cf88() + indexar_l10741()

    print("\n" + "=" * 60)
    print(f"CONCLUÍDO: {total} artigos indexados no total")
    print("=" * 60)

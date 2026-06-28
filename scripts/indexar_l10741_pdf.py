#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extrai e indexa Lei 10.741/2003 (Estatuto do Idoso) de PDF de duas colunas.

Uso:
    python scripts/indexar_l10741_pdf.py           # indexa no Supabase
    python scripts/indexar_l10741_pdf.py --dry     # só mostra extração
    python scripts/indexar_l10741_pdf.py --html    # salva HTML no vault
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

PDF_PATH = PROJECT_ROOT / "09_FENICE_BRAIN" / "Livro-II-Crimes-Pessoas" / "estatuto_idoso_7ed.pdf"
LEI_CHAVE = "Lei Federal 10741/2003"
MAX_ART = 118


def _extrair_texto_pdf(pdf_path: Path) -> str:
    try:
        import pdfplumber
    except ImportError:
        print("[ERRO] pdfplumber não instalado: pip install pdfplumber")
        sys.exit(1)

    paginas = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        print(f"  PDF: {len(pdf.pages)} páginas")
        for page in pdf.pages:
            w = page.width
            # Extrai coluna esquerda depois direita (layout de 2 colunas)
            left  = page.within_bbox((0,    0, w * 0.50, page.height)).extract_text() or ""
            right = page.within_bbox((w * 0.50, 0, w,   page.height)).extract_text() or ""
            paginas.append(left + "\n" + right)

    return "\n".join(paginas)


def _limpar_texto(texto: str) -> str:
    # Reconecta hifenações de fim de linha: "funda-\nmentais" → "fundamentais"
    texto = re.sub(r"-\n(\w)", r"\1", texto)
    texto = re.sub(r"[ \t]+", " ", texto)
    texto = re.sub(r"\n{3,}", "\n\n", texto)
    # U+FFFD (replacement char) gerado pelo pdfplumber em "10.741" → normaliza
    texto = texto.replace("�", ".").replace("\x00", ".")
    return texto.strip()


def _isolar_lei_10741(texto: str) -> str:
    """Recorta o corpo da Lei 10.741, pulando o sumário inicial."""
    # Âncora confiável: cabeçalho sancionatório logo antes do Art. 1º
    inicio = re.search(
        r"Fa[çc]o saber que o Congresso Nacional decreta e eu\s+sanciono",
        texto, re.IGNORECASE
    )
    if not inicio:
        # fallback: primeira ocorrência de "Art. 1º É instituído o Estatuto"
        inicio = re.search(r"Art\.\s*1[ºo°]\s+É instituído o Estatuto", texto, re.IGNORECASE)
    if not inicio:
        print("  [AVISO] Marcador de início não encontrado — usando texto completo")
        return texto

    resto = texto[inicio.start():]

    # Fim: próxima lei numerada diferente de 10741, ou Política Nacional, ou Convenção
    fim = re.search(
        r"\nLEI\s+N[ºo°][º\s]*\d{4,5}[.\s/]\d{3,4}(?![\s\d]*741)"
        r"|\nPOLÍTICA\s+NACIONAL"
        r"|\nLEI\s+ORGÂNICA"
        r"|\nCONVENÇÃO\s+INTERA"
        r"|\nPLANO\s+DE\s+AÇÃO",
        resto[500:], re.IGNORECASE
    )
    trecho = resto[:500 + fim.start()] if fim else resto
    print(f"  Isolamento: {len(trecho):,} chars (de {len(texto):,} totais)")
    return trecho


def _extrair_artigos(texto: str) -> list[dict]:
    marcadores = list(re.finditer(
        r"(?:^|\n)\s*Art\.\s*(\d+)[ºo°]?",
        texto, re.MULTILINE
    ))
    print(f"  {len(marcadores)} marcadores de artigo detectados")

    vistos: set[int] = set()
    artigos = []

    for i, m in enumerate(marcadores):
        num = int(m.group(1))
        if num in vistos or num > MAX_ART:
            continue
        vistos.add(num)

        inicio = m.start()
        fim = marcadores[i + 1].start() if i + 1 < len(marcadores) else len(texto)
        bloco = re.sub(r"\s+", " ", texto[inicio:fim]).strip()
        corpo = re.sub(r"^Art\.\s*\d+\s*[ºo°]?\s*[-–—.]?\s*", "", bloco).strip()
        artigos.append({"lei": LEI_CHAVE, "numero": num, "texto": corpo})

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


def _salvar_html(artigos: list[dict], dest: Path):
    linhas = [
        "<!DOCTYPE html>",
        '<html lang="pt-BR"><head><meta charset="UTF-8">',
        "<title>Lei nº 10.741/2003 — Estatuto do Idoso</title>",
        "<style>body{font-family:Arial,sans-serif;max-width:800px;margin:20px auto;padding:0 20px}",
        ".artigo{text-indent:20px;text-align:justify;margin-bottom:12px}</style></head><body>",
        "<h1>LEI Nº 10.741, DE 1º DE OUTUBRO DE 2003</h1>",
        "<h2>Estatuto do Idoso</h2>",
    ]
    for a in artigos:
        linhas.append(f'<div class="artigo"><strong>Art. {a["numero"]}º</strong> {a["texto"]}</div>')
    linhas.append("</body></html>")
    dest.write_text("\n".join(linhas), encoding="utf-8")
    print(f"  HTML salvo: {dest}")


def main():
    dry   = "--dry"  in sys.argv
    html  = "--html" in sys.argv

    print(f"\n{'='*60}")
    print("L10741 — Estatuto do Idoso (PDF → Supabase)")
    print(f"{'='*60}")

    if not PDF_PATH.exists():
        print(f"[ERRO] PDF não encontrado: {PDF_PATH}")
        sys.exit(1)

    print(f"  Fonte: {PDF_PATH.name}")
    texto_bruto = _extrair_texto_pdf(PDF_PATH)
    texto = _limpar_texto(texto_bruto)
    texto = _isolar_lei_10741(texto)

    artigos = _extrair_artigos(texto)
    print(f"  {len(artigos)} artigos extraídos (esperado: ~118)")

    if artigos:
        print(f"  Exemplo Art.1: {artigos[0]['texto'][:80]}…")
        print(f"  Último: Art.{artigos[-1]['numero']}")

    if html:
        dest = PROJECT_ROOT / "08_ENSINO" / "Uniasselvi" / "Biblioteca" / "L10741.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        _salvar_html(artigos, dest)

    if dry:
        return

    if not SB_URL or not SB_KEY:
        print("[ERRO] SUPABASE_URL / SUPABASE_SERVICE_KEY não definidos")
        sys.exit(1)

    enviados = _upsert(artigos)
    print(f"  ✓ {enviados} artigos enviados ao Supabase")

    print(f"\n{'='*60}")
    print(f"CONCLUÍDO — lei: '{LEI_CHAVE}'")
    print(f"{'='*60}")
    print("\nPróximo passo: atualizar landing.html e vercel deploy --prod")


if __name__ == "__main__":
    main()

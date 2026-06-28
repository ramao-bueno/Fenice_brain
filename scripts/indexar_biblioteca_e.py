#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Indexador batch da Biblioteca Jurídica HTML (HD Externo E:)
→ tabela `artigos` no Supabase

Lê todos os HTMLs mapeados, extrai artigos e faz upsert.

Uso:
    python scripts/indexar_biblioteca_e.py           # indexa tudo
    python scripts/indexar_biblioteca_e.py --dry     # só mostra o mapa
    python scripts/indexar_biblioteca_e.py DEL5452   # só essa lei
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

BIBLIOTECA = Path(r"E:\Users\oicon\OneDrive\Allah - Islamismo\Stand Alone Legaltech\biblioteca jurídica HTML")

# ── Mapeamento: nome-base-do-arquivo → (lei_key_supabase, max_art)
# max_art: limite superior para evitar capturar artigos de outra lei no mesmo HTML
MAPA: dict[str, tuple[str, int]] = {
    # 01_CODIGO_CIVIL
    "D9830":               ("Decreto 9830/2019",           30),
    "L10406":              ("Lei Federal 10406/2002",     2200),   # CC
    "L13655":              ("Lei Federal 13655/2018",       30),   # LINDB nova

    # 02_CODIGO_PENAL
    "DEL2848":             ("Decreto-Lei 2848/1940",       370),   # CP
    "L12850":              ("Lei Federal 12850/2013",       30),
    "L14132":              ("Lei Federal 14132/2021",       10),
    "L14155":              ("Lei Federal 14155/2021",       10),
    "L14811":              ("Lei Federal 14811/2024",       20),
    "L15384":              ("Lei Federal 15384/2025",       20),
    "L7492":               ("Lei Federal 7492/1986",        35),
    "L8072":               ("Lei Federal 8072/1990",        20),
    "L8137":               ("Lei Federal 8137/1990",        25),
    "L9605":               ("Lei Federal 9605/1998",        85),
    "L9613":               ("Lei Federal 9613/1998",        25),

    # 03_CODIGO_PROCESSO_CIVIL
    "L10259":              ("Lei Federal 10259/2001",       25),
    "L13105":              ("Lei Federal 13105/2015",     1100),   # CPC

    # 04_CODIGO_PROCESSO_PENAL
    "L13869":              ("Lei Federal 13869/2019",       50),
    "L13964":              ("Lei Federal 13964/2019",       30),
    "L7210":               ("Lei Federal 7210/1984",       215),   # LEP
    "L7960":               ("Lei Federal 7960/1989",        10),
    "L9099":               ("Lei Federal 9099/1995",       100),

    # 06_DIREITO_TRABALHO
    "DEL5452":             ("Decreto-Lei 5452/1943",       930),   # CLT
    "L10101":              ("Lei Federal 10101/2000",       20),
    "L13467":              ("Lei Federal 13467/2017",       10),
    "L14442":              ("Lei Federal 14442/2022",       10),
    "L6019":               ("Lei Federal 6019/1974",        25),
    "L7418":               ("Lei Federal 7418/1985",        10),
    "L8036consol":         ("Lei Federal 8036/1990",        35),   # FGTS

    # 07_DIREITO_CONSUMIDOR
    "L8078":               ("Lei Federal 8078/1990",       120),   # CDC

    # 08_DIREITO_ADMINISTRATIVO
    "Del4657":             ("Decreto-Lei 4657/1942",        35),   # LINDB
    "L12527":              ("Lei Federal 12527/2011",       50),   # LAI
    "L12846":              ("Lei Federal 12846/2013",       35),   # Anticorrupção
    "L13303":              ("Lei Federal 13303/2016",      110),   # Estatuto estatais
    "L14133":              ("Lei Federal 14133/2021",      200),   # Nova licitação
    "L4320":               ("Lei Federal 4320/1964",       120),   # Finanças públicas
    "L6404consol":         ("Lei Federal 6404/1976",       310),   # S.A.
    "L8112consol":         ("Lei Federal 8112/1990",       250),   # Servidores federais
    "L8429":               ("Lei Federal 8429/1992",        25),
    "L8987consol":         ("Lei Federal 8987/1995",        45),   # Concessões
    "L9784":               ("Lei Federal 9784/1999",        75),

    # 09_DIREITO_DIGITAL_LGPD
    "L12737":              ("Lei Federal 12737/2012",       10),
    "L12965":              ("Lei Federal 12965/2014",       35),   # MCI
    "L13709":              ("Lei Federal 13709/2018",       70),   # LGPD
    "L13709compilado":     None,                                    # duplicata
    "L9609":               ("Lei Federal 9609/1998",        20),
    "L9610":               ("Lei Federal 9610/1998",       120),

    # 10_DIREITO_INTERNACIONAL
    "D0350":               ("Decreto 350/1991",             10),
    "D4311":               ("Decreto 4311/2002",            60),
    "D4388":               ("Decreto 4388/2002",           135),   # TPI
    "D678":                ("Decreto 678/1992",             40),   # CADH
    "L13445":              ("Lei Federal 13445/2017",      130),   # Migração
    "L9307":               ("Lei Federal 9307/1996",        45),   # Arbitragem

    # 12_LEGISLACAO_ESPECIAL (nome exato do arquivo sem .html)
    "Base Legislação da Presidência da República - Lei nº 5.869 de 11 de janeiro de 1973":
                           None,                                    # índice geral
    "D12153":              ("Decreto 12153/2024",           20),
    "Decreto nº 6949":     ("Decreto 6949/2009",            90),
    "Decreto nº 7030":     ("Decreto 7030/2009",            15),
    "Decreto nº 7962":     ("Decreto 7962/2013",            20),
    "Decreto nº 8327":     ("Decreto 8327/2014",            20),
    "Decreto nº 8771":     ("Decreto 8771/2016",            45),
    "Direito Internacional Aplicado ao Brasil _ FENICE JustechPlatform":
                           None,                                    # conteúdo fenice
    "L12016":              ("Lei Federal 12016/2009",       30),
    "L12153":              ("Lei Federal 12153/2009",       35),
    "L13140":              ("Lei Federal 13140/2015",       65),   # Mediação
    "L13300":              ("Lei Federal 13300/2016",       18),
    "L13853":              ("Lei Federal 13853/2019",       10),
    "L15352":              ("Lei Federal 15352/2025",       30),
    "L15382":              ("Lei Federal 15382/2025",       30),
    "L15383":              ("Lei Federal 15383/2025",       30),
    "l15410":              ("Lei Federal 15410/2025",       30),
    "l15411":              ("Lei Federal 15411/2025",       30),
    "l15412":              ("Lei Federal 15412/2025",       30),
    "L4717":               ("Lei Federal 4717/1965",        25),
    "L8212 - Consolidada": ("Lei Federal 8212/1991",       100),
    "L8213consol":         ("Lei Federal 8213/1991",       150),
    "L9507":               ("Lei Federal 9507/1997",        25),
    "L9709":               ("Lei Federal 9709/1998",        20),
    "L9868":               ("Lei Federal 9868/1999",        35),
    "L9882":               ("Lei Federal 9882/1999",        18),
    "Lcp 150":             ("Lei Complementar 150/2015",    45),
    "Lcp101":              ("Lei Complementar 101/2000",    80),   # LRF
    "Lcp95":               ("Lei Complementar 95/1998",     20),
    "Lei nº 11.079":       ("Lei Federal 11079/2004",       45),   # PPP
    "Lei nº 11.201":       ("Lei Federal 11201/2005",       30),
    "Lei nº 11.340":       ("Lei Federal 11340/2006",       55),   # Maria da Penha
    "Lei nº 11.343":       ("Lei Federal 11343/2006",       80),   # Drogas
    "Lei nº 11.417":       ("Lei Federal 11417/2006",       15),
    "Lei nº 11.419":       ("Lei Federal 11419/2006",       25),
    "Pesquisa Legislação da Presidência da República":
                           None,                                    # índice geral
}


# ── Funções ────────────────────────────────────────────────────────────────────

def _limpar_html(html: str) -> str:
    html = re.sub(r"<s\b[^>]*>.*?</s>", " ", html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r"<del\b[^>]*>.*?</del>", " ", html, flags=re.DOTALL | re.IGNORECASE)
    # Tags de bloco → newline (garante que "Art." fique no início da linha)
    html = re.sub(r"<(?:div|p|br|h[1-6]|li|tr|td|th|section|article)\b[^>]*>",
                  "\n", html, flags=re.IGNORECASE)
    texto = re.sub(r"<[^>]+>", " ", html)
    for ent, rep in [("&nbsp;"," "),("&amp;","&"),("&lt;","<"),("&gt;",">"),
                     ("&quot;",'"'),("&#39;","'")]:
        texto = texto.replace(ent, rep)
    texto = re.sub(r"&[a-z#0-9]+;", " ", texto)
    texto = re.sub(r"[ \t]+", " ", texto)
    texto = re.sub(r"\n{3,}", "\n\n", texto)
    return texto.strip()


def _extrair_artigos(texto: str, lei_chave: str, max_art: int) -> list[dict]:
    marcadores = list(re.finditer(
        r"(?:^|\n)\s*Art\.\s*(\d+)\s*[ºo°]?",
        texto, re.MULTILINE
    ))
    vistos: set[int] = set()
    artigos = []
    for i, m in enumerate(marcadores):
        num = int(m.group(1))
        if num in vistos or num > max_art:
            continue
        vistos.add(num)
        inicio = m.start()
        fim = marcadores[i + 1].start() if i + 1 < len(marcadores) else len(texto)
        bloco = re.sub(r"\s+", " ", texto[inicio:fim]).strip()
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
            json=lote, headers=HDRS, timeout=60,
        )
        if r.status_code not in (200, 201):
            print(f"  [ERRO lote {i//100+1}] HTTP {r.status_code}: {r.text[:120]}")
        else:
            enviados += len(lote)
        time.sleep(0.1)
    return enviados


def indexar_arquivo(path: Path, lei_chave: str, max_art: int) -> int:
    try:
        raw = path.read_bytes()
        # Tenta UTF-8 → UTF-16 (BOM automático) → windows-1252
        try:
            html = raw.decode("utf-8")
        except UnicodeDecodeError:
            try:
                html = raw.decode("utf-16")   # detecta BOM FF FE / FE FF
            except UnicodeDecodeError:
                html = raw.decode("windows-1252", errors="replace")
    except Exception as e:
        print(f"  [ERRO leitura] {e}")
        return 0

    texto = _limpar_html(html)
    artigos = _extrair_artigos(texto, lei_chave, max_art)
    if not artigos:
        print(f"  [AVISO] Nenhum artigo extraído")
        return 0

    enviados = _upsert(artigos)
    return enviados


def descobrir_todos() -> list[tuple[Path, str, int]]:
    """Retorna lista de (path, lei_chave, max_art) para todos os HTMLs da biblioteca."""
    encontrados = []
    for html_path in sorted(BIBLIOTECA.rglob("*.html")):
        stem = html_path.stem
        if stem not in MAPA:
            print(f"  [SEM MAPA] {html_path.relative_to(BIBLIOTECA)}")
            continue
        config = MAPA[stem]
        if config is None:
            continue  # explicitamente ignorado
        lei_chave, max_art = config
        encontrados.append((html_path, lei_chave, max_art))
    return encontrados


def main():
    if not SB_URL or not SB_KEY:
        print("ERRO: SUPABASE_URL / SUPABASE_SERVICE_KEY não definidos no .env")
        sys.exit(1)

    # Filtro por argumento (ex: DEL5452 ou parte do nome)
    filtro = None
    dry_run = False
    for arg in sys.argv[1:]:
        if arg == "--dry":
            dry_run = True
        else:
            filtro = arg.upper()

    entradas = descobrir_todos()
    if filtro:
        entradas = [e for e in entradas if filtro in e[0].stem.upper() or filtro in e[1].upper()]

    print(f"\n{'='*65}")
    print(f"BIBLIOTECA JURÍDICA HTML → artigos Supabase")
    print(f"{'='*65}")
    print(f"Arquivos a processar: {len(entradas)}")
    if dry_run:
        for path, lei, max_art in entradas:
            print(f"  {path.stem:40s} → {lei} (max {max_art})")
        return

    total_arts = 0
    total_leis = 0
    erros = 0

    for path, lei_chave, max_art in entradas:
        print(f"\n[>>] {path.stem}")
        print(f"     lei: {lei_chave}  |  max: {max_art}")
        n = indexar_arquivo(path, lei_chave, max_art)
        if n > 0:
            print(f"     ✓ {n} artigos → Supabase")
            total_arts += n
            total_leis += 1
        else:
            erros += 1
        time.sleep(0.3)

    print(f"\n{'='*65}")
    print(f"CONCLUÍDO: {total_leis} leis · {total_arts:,} artigos indexados · {erros} erros")
    print(f"{'='*65}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GIGO Gate — Fenice bRain LLM Wiki
Valida qualidade de fontes antes da ingestão no LLM Wiki.

Uso:
    python check_source.py --autor "Kelsen" --tipo primaria \
        --titulo "Teoria Pura do Direito" --modulo jurisconsultos \
        --cobertura canonica --url "arquivo.pdf"

Saída: JSON com status (aceito/rejeitado) e motivos detalhados.
Atualiza o log.md do módulo automaticamente se --commit passado.

Inspirado no padrão LLM Wiki de Andrej Karpathy e na taxonomia
de qualidade de dados do Westlaw/LexisNexis.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Constantes de qualidade
# ---------------------------------------------------------------------------

TIPOS_ACEITOS = {"primaria", "comentario", "compilacao", "sumula", "legislacao"}
TIPOS_REJEITADOS = {"cursinho", "blog", "videoaula", "podcast", "wikipedia_doutrina", "anonimo"}

MODULOS = {
    "jurisconsultos": Path(__file__).parent.parent.parent / "06_JURISCONSULTOS",
    "filosofia":      Path(__file__).parent.parent.parent / "07_FILOSOFIA",
}

KEYWORDS_LIXO = [
    "resumo de cursinho", "apostila oab", "flashcard", "resumo para prova",
    "material de concurso", "resumão", "frases famosas", "citações motivacionais",
    "transcrição", "podcast", "videoaula", "aula gravada",
]


# ---------------------------------------------------------------------------
# Limpeza de texto (padrão LegalDataPipeline — Gemini/Fenice)
# ---------------------------------------------------------------------------

RE_PROCESSO = re.compile(r"\b\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}\b")
RE_VALORES  = re.compile(r"(?:R\$\s*)(?:\d{1,3}(?:\.\d{3})*|\d+)(?:,\d{2})?")
RE_ISBN     = re.compile(r"978[-\s]?\d[-\s]?\d{3}[-\s]?\d{5}[-\s]?\d|ISBN[-:\s]+[\d\-X]{10,17}")
RE_DOI      = re.compile(r"10\.\d{4,9}/[-._;()/:A-Z0-9]+", re.IGNORECASE)
RE_HTML_TAG = re.compile(r"<[^>]+>")


def clean_html(raw: str) -> str:
    """Remove tags HTML e normaliza espaçamentos."""
    clean = RE_HTML_TAG.sub(" ", raw)
    return " ".join(clean.split())


def extract_legal_metadata(text: str) -> dict[str, Any]:
    """Extrai metadados estruturados de texto jurídico bruto."""
    processo = RE_PROCESSO.search(text)
    valores  = RE_VALORES.findall(text)
    isbn     = RE_ISBN.search(text)
    doi      = RE_DOI.search(text)

    valor_float = 0.0
    if valores:
        try:
            val = valores[0].replace("R$", "").replace(".", "").replace(",", ".").strip()
            valor_float = float(val)
        except ValueError:
            pass

    return {
        "numero_processo": processo.group(0) if processo else None,
        "isbn":            isbn.group(0) if isbn else None,
        "doi":             doi.group(0) if doi else None,
        "valor_causa":     valor_float if valor_float else None,
        "tem_referencia_formal": bool(isbn or doi or processo),
    }


# ---------------------------------------------------------------------------
# Validação GIGO
# ---------------------------------------------------------------------------

class GIGOResult:
    def __init__(self) -> None:
        self.aceito   = True
        self.motivos: list[str] = []
        self.avisos:  list[str] = []

    def rejeitar(self, motivo: str) -> None:
        self.aceito = False
        self.motivos.append(motivo)

    def avisar(self, aviso: str) -> None:
        self.avisos.append(aviso)

    def to_dict(self) -> dict[str, Any]:
        return {
            "status":  "aceito" if self.aceito else "rejeitado",
            "motivos": self.motivos,
            "avisos":  self.avisos,
        }


def validar(
    autor: str,
    tipo: str,
    titulo: str,
    modulo: str,
    cobertura: str = "parcial",
    url: str = "",
    texto_amostra: str = "",
) -> GIGOResult:
    """
    Valida uma fonte contra os critérios de qualidade do Fenice bRain.

    Critérios implementados (baseados no protocolo GIGO do LLM Wiki):
    1. Autoria verificável
    2. Tipo de fonte declarado
    3. Sem marcadores de lixo no texto-amostra
    4. Módulo reconhecido
    5. Referência formal (ISBN/DOI/processo) preferível
    """
    result = GIGOResult()

    # 1 — Autoria
    if not autor or len(autor.strip()) < 3:
        result.rejeitar("Autoria ausente ou genérica. Informar nome completo e filiação.")

    # 2 — Tipo de fonte
    tipo_norm = tipo.lower().strip()
    if tipo_norm in TIPOS_REJEITADOS:
        result.rejeitar(f"Tipo de fonte rejeitado: '{tipo}'. Ver tiers aceitos na skill pesquisa-juridica-elite.")
    elif tipo_norm not in TIPOS_ACEITOS:
        result.rejeitar(f"Tipo desconhecido: '{tipo}'. Use: {', '.join(sorted(TIPOS_ACEITOS))}.")

    # 3 — Keywords de lixo
    amostra_lower = texto_amostra.lower()
    encontrados = [kw for kw in KEYWORDS_LIXO if kw in amostra_lower]
    if encontrados:
        result.rejeitar(f"Texto contém marcadores de fonte baixa qualidade: {encontrados}")

    # 4 — Módulo válido
    if modulo not in MODULOS:
        result.rejeitar(f"Módulo '{modulo}' não reconhecido. Use: {', '.join(MODULOS)}")

    # 5 — Referência formal
    meta = extract_legal_metadata(texto_amostra)
    if not meta["tem_referencia_formal"] and tipo_norm in {"primaria", "comentario"}:
        result.avisar("Nenhum ISBN/DOI/processo detectado no texto-amostra. Confirmar manualmente.")

    # 6 — Cobertura
    if cobertura not in {"canonica", "parcial"}:
        result.avisar(f"Cobertura '{cobertura}' não reconhecida. Use 'canonica' ou 'parcial'.")

    return result


# ---------------------------------------------------------------------------
# Atualização do log.md
# ---------------------------------------------------------------------------

LOG_HEADER = """\
# Log de Ingestão — {modulo_titulo}

| Data | Fonte | Tipo | Cobertura | Páginas atualizadas | Status |
|------|-------|------|-----------|---------------------|--------|
"""

LOG_ROW = "| {data} | {titulo} — {autor} | {tipo} | {cobertura} | (pendente) | {status_emoji} {status} |\n"


def _status_emoji(aceito: bool) -> str:
    return "✅" if aceito else "❌"


def atualizar_log(modulo: str, titulo: str, autor: str, tipo: str, cobertura: str, result: GIGOResult) -> None:
    modulo_path = MODULOS[modulo]
    log_path    = modulo_path / "log.md"

    if not log_path.exists():
        modulo_titulo = modulo.upper().replace("_", " ")
        log_path.write_text(LOG_HEADER.format(modulo_titulo=modulo_titulo), encoding="utf-8")

    row = LOG_ROW.format(
        data          = date.today().isoformat(),
        titulo        = titulo,
        autor         = autor,
        tipo          = tipo,
        cobertura     = cobertura,
        status_emoji  = _status_emoji(result.aceito),
        status        = "aceito" if result.aceito else "rejeitado",
    )

    current = log_path.read_text(encoding="utf-8")
    if row.strip() not in current:
        log_path.write_text(current + row, encoding="utf-8")
        print(f"[log] Entrada adicionada em {log_path}", file=sys.stderr)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="GIGO Gate — valida fonte para o LLM Wiki Fenice bRain"
    )
    parser.add_argument("--autor",       required=True, help="Autor da obra (nome completo)")
    parser.add_argument("--tipo",        required=True, help="Tipo: primaria, comentario, compilacao, sumula, legislacao")
    parser.add_argument("--titulo",      required=True, help="Título da obra ou artigo")
    parser.add_argument("--modulo",      required=True, help="jurisconsultos | filosofia")
    parser.add_argument("--cobertura",   default="parcial", help="canonica | parcial (default: parcial)")
    parser.add_argument("--url",         default="", help="URL ou caminho do arquivo (opcional)")
    parser.add_argument("--amostra",     default="", help="Trecho de texto para análise de qualidade")
    parser.add_argument("--commit",      action="store_true", help="Atualizar log.md automaticamente")
    args = parser.parse_args()

    result = validar(
        autor          = args.autor,
        tipo           = args.tipo,
        titulo         = args.titulo,
        modulo         = args.modulo,
        cobertura      = args.cobertura,
        url            = args.url,
        texto_amostra  = args.amostra,
    )

    output = {
        "fonte": {
            "titulo":   args.titulo,
            "autor":    args.autor,
            "tipo":     args.tipo,
            "modulo":   args.modulo,
            "cobertura": args.cobertura,
            "url":      args.url,
        },
        **result.to_dict(),
    }
    print(json.dumps(output, indent=2, ensure_ascii=False))

    if args.commit:
        atualizar_log(
            modulo    = args.modulo,
            titulo    = args.titulo,
            autor     = args.autor,
            tipo      = args.tipo,
            cobertura = args.cobertura,
            result    = result,
        )

    sys.exit(0 if result.aceito else 1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fenice Ingestor — Vault Obsidian → Supabase pgvector
Uso: python scripts/fenice_ingestor.py [--dry-run] [--pasta 00_APEX]
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path
from datetime import date

# Garante UTF-8 no stdout mesmo em terminais Windows (cp1252)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from supabase import create_client, Client

# ---------------------------------------------------------------------------
# Configuração
# ---------------------------------------------------------------------------

VAULT_ROOT = Path(__file__).parent.parent  # C:\Fenice_bRain

# Pastas que contêm artigos jurídicos — exclui scripts/, docs/, api/, etc.
PASTAS_JURIDICAS = [
    "00_APEX", "01_PRIVADO", "02_LEGISLACAO", "02_PENAL",
    "03_PROCESSO_CIVIL", "03_PUBLICO", "04_TRABALHO",
    "05_ESPECIAL", "06_JURISCONSULTOS", "07_FILOSOFIA",
    "08_ENSINO", "09_FENICE_BRAIN",
]

# Mapeamento tag → codigo (ordem importa: mais específico primeiro)
TAG_TO_CODIGO: dict[str, str] = {
    "cf88": "CF",  "constitucional": "CF",
    "cpc":  "CPC", "processo-civil": "CPC",
    "cc":   "CC",  "civil": "CC",
    "cp":   "CP",  "penal": "CP",
    "cpp":  "CPP", "processo-penal": "CPP",
    "clt":  "CLT", "trabalhista": "CLT",
    "cdc":  "CDC",
    "lei-federal": "LEI", "lei": "LEI",
}

# Mapeamento pasta raiz → codigo (fallback se tags não resolverem)
PASTA_TO_CODIGO: dict[str, str] = {
    "00_APEX": "CF",
    "02_PENAL": "CP",
    "03_PROCESSO_CIVIL": "CPC",
    "04_TRABALHO": "CLT",
    "01_PRIVADO": "CC",
    "03_PUBLICO": "ADMIN",
    "05_ESPECIAL": "ESP",
}

# ---------------------------------------------------------------------------
# Modelo de embedding
# ---------------------------------------------------------------------------

def _carregar_modelo() -> SentenceTransformer:
    print("Carregando multilingual-e5-large (1024 dims) na CPU...")
    return SentenceTransformer("intfloat/multilingual-e5-large", device="cpu")


def gerar_embedding(model: SentenceTransformer, texto: str, is_passage: bool = True) -> list[float]:
    """Prefixo obrigatório do modelo E5: 'passage:' para chunks, 'query:' para consultas."""
    prefixo = "passage: " if is_passage else "query: "
    return model.encode(prefixo + texto, normalize_embeddings=True).tolist()

# ---------------------------------------------------------------------------
# Parser de frontmatter
# ---------------------------------------------------------------------------

def _parse_yaml_simples(bloco: str) -> dict:
    """Parse minimalista de YAML sem dependência pesada."""
    meta: dict = {}
    lista_atual: str | None = None

    for linha in bloco.splitlines():
        if not linha.strip() or linha.strip().startswith("#"):
            continue

        # Item de lista YAML (  - valor)
        if re.match(r"^\s+-\s+", linha):
            if lista_atual:
                meta.setdefault(lista_atual, [])
                meta[lista_atual].append(linha.strip().lstrip("- ").strip().strip('"').strip("'"))
            continue

        if ":" not in linha:
            lista_atual = None
            continue

        chave, _, valor = linha.partition(":")
        chave = chave.strip().lower()
        valor = valor.strip().strip('"').strip("'")

        if not valor:
            # Provavelmente início de lista
            lista_atual = chave
            meta[chave] = []
        else:
            lista_atual = None
            meta[chave] = valor

    return meta


def extrair_nota(caminho: Path) -> tuple[dict | None, str | None]:
    """
    Lê uma nota .md e retorna (meta, conteudo_limpo).
    Retorna (None, None) se não for um artigo válido.
    """
    try:
        texto = caminho.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return None, None

    # Frontmatter obrigatório
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", texto, re.DOTALL)
    if not match:
        return None, None

    meta = _parse_yaml_simples(match.group(1))
    corpo = match.group(2).strip()

    # Só processa notas que tenham o campo "artigo:" — descarta leis inteiras, notas diárias, etc.
    if not meta.get("artigo"):
        return None, None

    return meta, corpo


def derivar_codigo(meta: dict, caminho: Path) -> str:
    """Deriva o código do documento (CF, CC, CPC...) a partir das tags ou pasta."""
    tags = meta.get("tags", [])
    if isinstance(tags, str):
        tags = [tags]

    for tag in tags:
        tag_lower = tag.lower().strip()
        if tag_lower in TAG_TO_CODIGO:
            return TAG_TO_CODIGO[tag_lower]

    # Fallback: pasta raiz
    pasta_raiz = caminho.relative_to(VAULT_ROOT).parts[0] if caminho.is_relative_to(VAULT_ROOT) else ""
    return PASTA_TO_CODIGO.get(pasta_raiz, "GERAL")


def limpar_texto(texto: str) -> str:
    """Remove marcações Obsidian e normaliza espaçamento para o embedding."""
    texto = re.sub(r"\[\[(.*?)\]\]", r"\1", texto)     # [[link]] → link
    texto = re.sub(r"!\[\[.*?\]\]", "", texto)           # embeds de imagem
    texto = re.sub(r">\s*\[!.*?\].*?\n", "", texto)      # callouts Obsidian
    texto = re.sub(r"#+ ", "", texto)                    # headings markdown
    texto = re.sub(r"[\r\n]+", " ", texto)
    texto = re.sub(r"\s+", " ", texto)
    return texto.strip()

# ---------------------------------------------------------------------------
# Pipeline principal
# ---------------------------------------------------------------------------

def coletar_arquivos(pasta_filtro: str | None = None) -> list[Path]:
    pastas = [pasta_filtro] if pasta_filtro else PASTAS_JURIDICAS
    arquivos: list[Path] = []
    for pasta in pastas:
        pasta_path = VAULT_ROOT / pasta
        if pasta_path.exists():
            arquivos.extend(pasta_path.rglob("*.md"))
    return arquivos


def executar_ingestao(dry_run: bool = False, pasta_filtro: str | None = None) -> None:
    load_dotenv(VAULT_ROOT / ".env")

    sb_url = os.environ.get("SUPABASE_URL", "")
    sb_key = os.environ.get("SUPABASE_SERVICE_KEY", "")

    if not sb_url or not sb_key:
        print("❌ SUPABASE_URL ou SUPABASE_SERVICE_KEY não configurados no .env")
        sys.exit(1)

    supabase: Client = create_client(sb_url, sb_key)
    model = _carregar_modelo()

    arquivos = coletar_arquivos(pasta_filtro)
    print(f"\nEncontrados {len(arquivos)} arquivos .md nas pastas jurídicas.")

    sucessos = erros = ignorados = 0

    for idx, caminho in enumerate(arquivos, 1):
        meta, corpo = extrair_nota(caminho)

        if not meta:
            ignorados += 1
            continue

        artigo = str(meta["artigo"]).strip()
        codigo = derivar_codigo(meta, caminho)
        titulo = str(meta.get("titulo") or meta.get("nomen") or f"{codigo} {artigo}").strip()
        vigente = str(meta.get("status", "vigente")).lower() not in ("revogado", "false", "0")
        conteudo_limpo = limpar_texto(corpo)

        if not conteudo_limpo:
            ignorados += 1
            continue

        print(f"[{idx}/{len(arquivos)}] {codigo} {artigo} — {titulo[:50]}")

        if dry_run:
            sucessos += 1
            continue

        try:
            # 1. Upsert documento base — .select() obrigatório para obter o ID
            res_doc = (
                supabase.table("documentos_juridicos")
                .upsert(
                    {
                        "codigo":    codigo,
                        "artigo":    artigo,
                        "titulo":    titulo,
                        "conteudo":  corpo,
                        "fonte":     "vault",
                        "vigente":   vigente,
                        "data_ref":  date.today().isoformat(),
                    },
                    on_conflict="codigo,artigo,fonte",
                )
                .select()
                .execute()
            )

            if not res_doc.data:
                print(f"  ⚠️  Upsert sem retorno — verifique a constraint unique(codigo, artigo, fonte)")
                erros += 1
                continue

            documento_id = res_doc.data[0]["id"]

            # 2. Gera embedding (prefixo "passage:" obrigatório para E5)
            vetor = gerar_embedding(model, conteudo_limpo, is_passage=True)

            # 3. Substitui chunk anterior e insere novo
            supabase.table("documentos_chunks").delete().eq("documento_id", documento_id).execute()
            supabase.table("documentos_chunks").insert(
                {
                    "documento_id": documento_id,
                    "chunk_index":  0,
                    "conteudo":     conteudo_limpo,
                    "embedding":    vetor,
                }
            ).execute()

            sucessos += 1

        except Exception as exc:
            print(f"  ❌ {caminho.name}: {exc}")
            erros += 1

    print(f"\n{'[DRY RUN] ' if dry_run else ''}Pipeline concluído.")
    print(f"  ✅ Sucesso:  {sucessos}")
    print(f"  ❌ Erros:    {erros}")
    print(f"  ⏭  Ignorados: {ignorados}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fenice Ingestor — vault → Supabase pgvector")
    parser.add_argument("--dry-run", action="store_true", help="Simula sem gravar no Supabase")
    parser.add_argument("--pasta",   type=str, default=None, help="Processa apenas uma pasta (ex: 00_APEX)")
    args = parser.parse_args()

    executar_ingestao(dry_run=args.dry_run, pasta_filtro=args.pasta)

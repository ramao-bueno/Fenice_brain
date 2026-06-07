#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pipeline completo CPC: extrai HTML → gera markdown → salva no vault."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from config_codigo_processo_civil import LEIS_NACIONAIS, OUTPUT_BASE
from extrator_html_generico import extrair_artigos_html
from markdown_generator_cpc import MarkdownGeneratorCPC


def processar_lei(sigla: str, cfg: dict) -> int:
    """Processa uma lei: extrai artigos, gera notas, salva."""
    arquivo_html = cfg["arquivo"]

    if not arquivo_html.exists():
        print(f"❌ {sigla}: arquivo não encontrado — {arquivo_html}")
        return 0

    print(f"📄 {sigla} ({cfg['lei_numero']})...", end=" ", flush=True)

    # Extrai artigos do HTML
    artigos = extrair_artigos_html(arquivo_html)
    if not artigos:
        print("⚠️  nenhum artigo extraído")
        return 0

    # Gera notas markdown
    gen = MarkdownGeneratorCPC(OUTPUT_BASE)
    salves = 0

    for artigo in artigos:
        artigo["categoria"] = cfg.get("categoria", "PROCESSO_CIVIL")
        conteudo = gen.gerar_nota_artigo(artigo, cfg, sigla)
        resultado = gen.salvar_artigo(artigo, conteudo, sigla)
        if resultado:
            salves += 1

    print(f"✅ {salves}/{len(artigos)} artigos salvos")
    return salves


def main():
    print("=" * 70)
    print("PIPELINE CÓDIGO DE PROCESSO CIVIL")
    print("=" * 70)
    print()

    # Cria pasta de output
    OUTPUT_BASE.mkdir(parents=True, exist_ok=True)

    total_salve = 0

    for sigla, cfg in LEIS_NACIONAIS.items():
        salves = processar_lei(sigla, cfg)
        total_salve += salves

    print()
    print("=" * 70)
    print(f"Total de artigos salvos: {total_salve}")
    print(f"Output: {OUTPUT_BASE}")
    print("=" * 70)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()

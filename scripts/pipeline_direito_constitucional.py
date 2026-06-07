#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pipeline completo: extrai HTML → gera markdown → salva no vault."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from pathlib import Path
from config_direito_constitucional import LEIS_NACIONAIS, OUTPUT_BASE
from extrator_html_dc import extrair_artigos_html
from markdown_generator_dc import MarkdownGeneratorDC


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
    gen = MarkdownGeneratorDC(OUTPUT_BASE)
    salves = 0

    for artigo in artigos:
        artigo["categoria"] = cfg.get("categoria", "DIREITO_CONSTITUCIONAL")
        conteudo = gen.gerar_nota_artigo(artigo, cfg, sigla)
        resultado = gen.salvar_artigo(artigo, conteudo, sigla)
        if resultado:
            salves += 1

    print(f"✅ {salves}/{len(artigos)} artigos salvos")
    return salves


def main():
    print("=" * 70)
    print("PIPELINE DIREITO CONSTITUCIONAL")
    print("=" * 70)
    print()

    # Cria pasta de output
    OUTPUT_BASE.mkdir(parents=True, exist_ok=True)

    total_salve = 0

    for sigla, cfg in LEIS_NACIONAIS.items():
        # Ignora D678 (duplicata de CADH)
        if sigla == "D678":
            print(f"⏭️  {sigla}: pulado (duplicata de Direito Internacional)")
            continue

        # Ignora Decreto 6949 por enquanto (só 3 artigos, candidato a skill later)
        if sigla == "D6949":
            print(f"⏭️  {sigla}: pulado (futuro)")
            continue

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

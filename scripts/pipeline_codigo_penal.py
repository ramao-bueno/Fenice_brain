#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pipeline completo CP: extrai HTML → gera markdown → salva no vault."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from config_codigo_penal import LEIS_NACIONAIS, OUTPUT_BASE
from extrator_html_generico import extrair_artigos_html
from markdown_generator_cp import MarkdownGeneratorCP


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

    # Monta lookup prev/next pela ordem real da lei (inclui sufixos como 121-A)
    nums = [str(a["numero"]) for a in artigos]
    prev_next = {
        nums[i]: (nums[i - 1] if i > 0 else None,
                  nums[i + 1] if i < len(nums) - 1 else None)
        for i in range(len(nums))
    }

    # Gera notas markdown
    gen = MarkdownGeneratorCP(OUTPUT_BASE)
    salves = 0

    for artigo in artigos:
        artigo["categoria"] = cfg.get("categoria", "DIREITO_PENAL")
        num_str = str(artigo["numero"])
        artigo["prev_num"], artigo["next_num"] = prev_next[num_str]
        conteudo = gen.gerar_nota_artigo(artigo, cfg, sigla)
        resultado = gen.salvar_artigo(artigo, conteudo, sigla)
        if resultado:
            salves += 1

    print(f"✅ {salves}/{len(artigos)} artigos salvos")
    return salves


def main():
    print("=" * 70)
    print("PIPELINE CÓDIGO PENAL")
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

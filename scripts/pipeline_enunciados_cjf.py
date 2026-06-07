#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pipeline completo Enunciados CJF: lê JSON → gera markdown → salva no vault."""
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from config_enunciados_cjf import ENUNCIADOS_BASE, OUTPUT_BASE, JSON_FILE
from markdown_generator_enunciados_cjf import MarkdownGeneratorEnunciadosCJF


def carregar_enunciados(json_path: Path) -> list:
    """Carrega todos os enunciados do JSON."""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Erro ao ler JSON: {e}")
        return []

    enunciados = []
    for norma_key, enum_list in data.items():
        for enum in enum_list:
            enunciados.append(enum)

    return sorted(enunciados, key=lambda x: x['num'])


def processar_enunciados() -> int:
    """Processa todos os enunciados."""
    enunciados = carregar_enunciados(JSON_FILE)

    if not enunciados:
        print("⚠️  nenhum enunciado carregado")
        return 0

    print(f"📄 Processando {len(enunciados)} enunciados...")

    # Gera notas markdown
    gen = MarkdownGeneratorEnunciadosCJF(OUTPUT_BASE)
    salves = 0

    for enunciado in enunciados:
        conteudo = gen.gerar_nota_enunciado(enunciado)
        resultado = gen.salvar_enunciado(enunciado, conteudo)
        if resultado:
            salves += 1

    print(f"✅ {salves}/{len(enunciados)} enunciados salvos")
    return salves


def main():
    print("=" * 70)
    print("PIPELINE ENUNCIADOS CJF")
    print("=" * 70)
    print()

    # Cria pasta de output
    OUTPUT_BASE.mkdir(parents=True, exist_ok=True)

    salves = processar_enunciados()

    print()
    print("=" * 70)
    print(f"Total de enunciados salvos: {salves}")
    print(f"Output: {OUTPUT_BASE}")
    print("=" * 70)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()

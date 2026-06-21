#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Atualizar Legislacao — Script de Atualizacao Semanal do Vault

Verifica leis novas no Planalto para um dado ano, compara com as notas ja
existentes em 02_LEGISLACAO/Leis/ e salva apenas as leis ineditas.

Uso:
  python atualizar_legislacao.py [--ano 2026]
"""
import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

# Garante que importacoes do mesmo diretorio funcionem
sys.path.insert(0, str(Path(__file__).parent))

from planalto_pipeline import (
    listar_leis_por_ano,
    baixar_html,
    parsear_lei,
    salvar_nota,
    _db_conn,
    OUTPUT_LEIS_DIR,
)


def _nota_existente(numero: str, ano: str, output_dir: Path) -> bool:
    """Verifica se ja existe nota markdown para a lei (numero/ano) no vault."""
    # Padrao de nome: Lei-{numero}-{ano}.md
    candidatos = [
        output_dir / f"Lei-{numero}-{ano}.md",
        output_dir / f"Lei-{numero.lstrip('0')}-{ano}.md",
    ]
    return any(p.exists() for p in candidatos)


def _numero_de_url(url: str) -> str:
    """Extrai o numero da lei a partir de uma URL do Planalto."""
    m = re.search(r"[lL](\d{4,6})\.htm", url)
    return m.group(1) if m else ""


def _ano_de_url(url: str, fallback_ano: int) -> str:
    """Extrai o ano da lei a partir de uma URL do Planalto."""
    m = re.search(r"/(\d{4})/lei/", url)
    return m.group(1) if m else str(fallback_ano)


def main():
    sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Atualiza notas de legislacao federal no vault Fenice bRain"
    )
    parser.add_argument(
        "--ano",
        type=int,
        default=datetime.now().year,
        help="Ano das leis a verificar (padrao: ano corrente)",
    )
    args = parser.parse_args()
    ano = args.ano

    output_dir = OUTPUT_LEIS_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print(f"ATUALIZAR LEGISLACAO — Ano: {ano}")
    print(f"Vault: {output_dir}")
    print("=" * 70)

    conn = _db_conn()
    if conn:
        print("🗄️  Supabase: conectado — leis serão persistidas no banco")
    else:
        print("⚠️  Supabase: desativado (configure DB_* no .env)")

    # 1. Lista leis disponíveis no Planalto para o ano
    print(f"\n[1/3] Listando leis de {ano} no Planalto...")
    urls = listar_leis_por_ano(ano)
    print(f"      {len(urls)} URLs encontradas")

    if not urls:
        print("      Nenhuma URL encontrada. Encerrando.")
        return

    # 2. Filtra apenas as leis novas (sem nota no vault)
    novas: list = []
    ja_existentes: int = 0

    print(f"\n[2/3] Verificando notas existentes em {output_dir}...")
    for url in urls:
        numero = _numero_de_url(url)
        ano_lei = _ano_de_url(url, ano)
        if numero and _nota_existente(numero, ano_lei, output_dir):
            ja_existentes += 1
        else:
            novas.append(url)

    print(f"      Ja existentes  : {ja_existentes}")
    print(f"      Novas para baixar: {len(novas)}")

    # 3. Baixa, parseia e salva apenas as leis novas
    print(f"\n[3/3] Processando {len(novas)} lei(s) nova(s)...")
    salvas = 0
    erros = 0

    for i, url in enumerate(novas, 1):
        print(f"\n  [{i}/{len(novas)}] {url}")
        caminho = baixar_html(url)
        if not caminho:
            print("      [ERRO] Download falhou")
            erros += 1
            continue

        try:
            dados = parsear_lei(caminho, url_origem=url)
            path = salvar_nota(dados, output_dir, conn=conn)
            if path:
                print(f"      [OK] Salvo: {path.name}")
                salvas += 1
            else:
                erros += 1
        except Exception as e:
            print(f"      [ERRO] {e}")
            erros += 1

    if conn:
        conn.close()

    # Relatorio final
    print("\n" + "=" * 70)
    print("RELATORIO FINAL")
    print(f"  Total de URLs no indice : {len(urls)}")
    print(f"  Ja existentes no vault  : {ja_existentes}")
    print(f"  Novas salvas            : {salvas}")
    print(f"  Erros                   : {erros}")
    print("=" * 70)


if __name__ == "__main__":
    main()

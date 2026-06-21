#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Orquestrador diario — Brazil Law Pipeline

Varre o indice de leis do ano corrente (ou PIPELINE_ANO),
baixa cada lei, parseia e persiste via upsert no PostgreSQL.

Variaveis de ambiente:
  DB_HOST       = localhost
  DB_NAME       = fenice_brain
  DB_USER       = postgres
  DB_PASS       = senha
  DB_PORT       = 5432
  PIPELINE_ANO  = 2026   (ano a processar)
"""
import os
import sys
from datetime import datetime

from src.scraper import listar_leis_por_ano, baixar_html
from src.parser_law import parsear_lei
from src.database import PlanaltoDB


def main():
    ano = int(os.environ.get("PIPELINE_ANO", datetime.now().year))

    print("=" * 70)
    print(f"BRAZIL LAW PIPELINE — Atualizacao diaria | Ano: {ano}")
    print("=" * 70)

    # 1. Conecta ao banco
    db = PlanaltoDB()
    if not db.conectar():
        print("[ERRO] Nao foi possivel conectar ao banco. Abortando.")
        sys.exit(1)

    # 2. Descobre leis do ano
    print(f"\n[1/3] Listando leis de {ano}...")
    urls = listar_leis_por_ano(ano)
    print(f"      {len(urls)} URLs encontradas")

    if not urls:
        print("      Nenhuma lei encontrada. Encerrando.")
        db.fechar()
        return

    # 3. Processa cada lei
    print(f"\n[2/3] Processando leis...")
    ok = 0
    erros = 0

    for i, url in enumerate(urls, 1):
        print(f"\n  [{i}/{len(urls)}] {url}")

        caminho = baixar_html(url)
        if not caminho:
            erros += 1
            continue

        try:
            dados = parsear_lei(caminho)
            sucesso = db.upsert_lei(dados)
            if sucesso:
                print(f"      Upsert OK — Lei {dados['numero']}/{dados['ano']}")
                ok += 1
            else:
                erros += 1
        except Exception as e:
            print(f"      [ERRO] Falha ao processar {url}: {e}")
            erros += 1

    db.fechar()

    # 4. Relatorio
    print("\n" + "=" * 70)
    print(f"[3/3] RELATORIO")
    print(f"      Total processadas : {len(urls)}")
    print(f"      Upsert com sucesso : {ok}")
    print(f"      Erros              : {erros}")
    print("=" * 70)


if __name__ == "__main__":
    main()

"""Confere os JSON curados (data/*.json) contra as planilhas .xlsx.

Os JSON sao a fonte de verdade da UI. Este script NAO gera os JSON: ele
le as planilhas anuais limpas (2021-2025) e confere se a contagem de
audiencias bate com data/audiencias_anuais.json. Serve de prova de que os
numeros publicados tem lastro nos dados originais.

Uso:
    pip install -r scripts/requirements.txt
    python scripts/gerar_dados.py

Exit 0 = tudo confere; Exit 1 = ha divergencia a investigar.
"""
import json
import sys
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parents[1]   # .../violencia-mulher-sfs
PLANILHAS = BASE.parent                       # .../Nova pasta (onde estao os .xlsx)
DATA = BASE / "data"

ARQUIVOS_ANUAIS = {
    2021: "2021.xlsx",
    2022: "2022.xlsx",
    2023: "2023.xlsx",
    2024: "2024.xlsx",
    2025: "2025.xlsx",
}


def carregar_json(nome):
    return json.loads((DATA / nome).read_text(encoding="utf-8"))


def contar_audiencias(xlsx):
    """Conta linhas de dados na primeira aba, ignorando cabecalho e linhas vazias."""
    df = pd.read_excel(PLANILHAS / xlsx, sheet_name=0)
    df = df.dropna(how="all")
    return int(df.shape[0])


def main():
    esperado = {a["ano"]: a["total"] for a in carregar_json("audiencias_anuais.json")}
    divergencias = []
    print(f"{'Ano':<6}{'Planilha':<12}{'JSON':<8}{'Status'}")
    print("-" * 34)
    for ano, arq in ARQUIVOS_ANUAIS.items():
        try:
            obtido = contar_audiencias(arq)
        except Exception as e:  # noqa: BLE001
            print(f"{ano:<6}{'ERRO':<12}{esperado[ano]:<8}{e}")
            divergencias.append(ano)
            continue
        ok = obtido == esperado[ano]
        print(f"{ano:<6}{obtido:<12}{esperado[ano]:<8}{'OK' if ok else 'DIVERGE'}")
        if not ok:
            divergencias.append(ano)

    print("-" * 34)
    if divergencias:
        print(f"Divergencias em: {divergencias}")
        print("Investigar antes de publicar (ex.: 2024 tem tabela dinamica embutida).")
        sys.exit(1)
    print("OK: todos os totais anuais batem com data/audiencias_anuais.json")
    sys.exit(0)


if __name__ == "__main__":
    main()

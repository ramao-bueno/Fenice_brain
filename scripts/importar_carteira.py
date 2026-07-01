"""Importa a carteira Farmer do Ramão para o Supabase fenice_tim_contatos.

Uso: python importar_carteira.py carteira.csv
CSV com colunas: nome, telefone, email, assunto
Estágio inicial: pos_venda (base existente = Farmer).
"""
import csv
import os
import sys

import httpx


def normalizar_telefone(bruto: str) -> str:
    dig = "".join(c for c in (bruto or "") if c.isdigit())
    if len(dig) == 11:
        dig = "55" + dig
    return dig


def linha_para_contato(linha: dict) -> dict:
    return {
        "numero": normalizar_telefone(linha.get("telefone", "")),
        "nome": (linha.get("nome") or "").strip(),
        "area": (linha.get("assunto") or "").strip() or "juridico",
        "estagio": "pos_venda",
        "dados": {"email": (linha.get("email") or "").strip().lower()},
    }


def carregar_csv(caminho: str) -> list:
    with open(caminho, encoding="utf-8-sig", newline="") as f:
        return [linha_para_contato(l) for l in csv.DictReader(f)]


def enviar_supabase(contatos: list, sb_url: str, sb_key: str) -> int:
    hdrs = {
        "apikey": sb_key,
        "Authorization": f"Bearer {sb_key}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal,resolution=merge-duplicates",
    }
    with httpx.Client(timeout=30) as c:
        r = c.post(
            f"{sb_url.rstrip('/')}/rest/v1/fenice_tim_contatos",
            params={"on_conflict": "numero"},
            headers=hdrs,
            json=contatos,
        )
    r.raise_for_status()
    return len(contatos)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python importar_carteira.py carteira.csv")
        sys.exit(1)
    contatos = carregar_csv(sys.argv[1])
    total = enviar_supabase(
        contatos,
        os.environ["SUPABASE_URL"],
        os.environ["SUPABASE_SERVICE_KEY"],
    )
    print(f"✅ {total} contatos Farmer importados.")

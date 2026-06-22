#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch download das principais leis do ordenamento brasileiro via Planalto.
Uso: python scripts/ingerir_batch_planalto.py
"""

import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from planalto_pipeline import baixar_html, parsear_lei, salvar_nota

OUTPUT_DIR = PROJECT_ROOT / "02_LEGISLACAO" / "Leis"

# Leis fundamentais do ordenamento brasileiro
LEIS = [
    # Códigos fundamentais
    ("10406", "2002", "Código Civil"),
    ("13105", "2015", "Código de Processo Civil"),
    ("8078",  "1990", "Código de Defesa do Consumidor"),
    ("8069",  "1990", "Estatuto da Criança e do Adolescente"),
    ("9394",  "1996", "Lei de Diretrizes e Bases da Educação"),
    ("9099",  "1995", "Juizados Especiais Cíveis e Criminais"),
    ("9503",  "1997", "Código de Trânsito Brasileiro"),
    ("8666",  "1993", "Licitações e Contratos (antiga)"),
    ("6404",  "1976", "Lei das Sociedades Anônimas"),
    ("8112",  "1990", "Regime Jurídico dos Servidores Federais"),
    ("9784",  "1999", "Processo Administrativo Federal"),
    ("7347",  "1985", "Ação Civil Pública"),
    ("4717",  "1965", "Ação Popular"),
    ("12016", "2009", "Mandado de Segurança"),
    ("9307",  "1996", "Arbitragem"),
    ("13869", "2019", "Abuso de Autoridade"),
    ("8429",  "1992", "Improbidade Administrativa (original)"),
    ("14230", "2021", "Improbidade Administrativa (nova)"),
    ("14133", "2021", "Licitações e Contratos (nova)"),
    ("13709", "2018", "LGPD — Proteção de Dados"),
    ("12965", "2014", "Marco Civil da Internet"),
    ("9610",  "1998", "Direitos Autorais"),
    ("9279",  "1996", "Propriedade Industrial"),
    ("10741", "2003", "Estatuto do Idoso"),
    ("13146", "2015", "Estatuto da Pessoa com Deficiência"),
    ("11343", "2006", "Lei de Drogas"),
    ("9455",  "1997", "Lei de Tortura"),
    ("7716",  "1989", "Crimes de Racismo"),
    ("11340", "2006", "Lei Maria da Penha"),
    ("8072",  "1990", "Crimes Hediondos"),
    ("9099",  "1995", "Juizados Especiais"),
    ("13257", "2016", "Marco Legal da Primeira Infância"),
    ("10150", "2000", "Transferência de Veículos"),
    ("12403", "2011", "Medidas Cautelares no CPP"),
    ("12850", "2013", "Organizações Criminosas"),
]

BASE = "https://www.planalto.gov.br/ccivil_03"

ANO_FAIXAS = [
    (1940, 1964, "leis"),
    (1965, 1987, "leis"),
    (1988, 1990, "_ato1988-1990"),
    (1991, 1994, "_ato1991-1994"),
    (1995, 1998, "_ato1995-1998"),
    (1999, 2002, "_ato1999-2002"),
    (2003, 2006, "_ato2003-2006"),
    (2007, 2010, "_ato2007-2010"),
    (2011, 2014, "_ato2011-2014"),
    (2015, 2018, "_ato2015-2018"),
    (2019, 2022, "_ato2019-2022"),
    (2023, 2026, "_ato2023-2026"),
]


def url_para_lei(numero: str, ano: int) -> list[str]:
    n = numero.zfill(5)
    candidatos = []
    for (a, b, faixa) in ANO_FAIXAS:
        if a <= ano <= b:
            if faixa.startswith("_ato"):
                candidatos.append(f"{BASE}/{faixa}/{ano}/lei/l{numero}.htm")
                candidatos.append(f"{BASE}/{faixa}/{ano}/lei/L{n}.htm")
            else:
                candidatos.append(f"{BASE}/leis/L{n}.htm")
                candidatos.append(f"{BASE}/leis/l{numero}.htm")
    # fallback histórico
    candidatos.append(f"{BASE}/leis/L{n}.htm")
    candidatos.append(f"{BASE}/leis/l{numero}.htm")
    return candidatos


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ok = 0
    skip = 0
    erro = 0

    print("=" * 65)
    print("BATCH PLANALTO — Principais Leis do Ordenamento Brasileiro")
    print("=" * 65)

    for numero, ano_str, nome in LEIS:
        saida = OUTPUT_DIR / f"Lei-{numero}-{ano_str}.md"
        if saida.exists():
            print(f"[SKIP] {nome} ({numero}/{ano_str}) — ja existe")
            skip += 1
            continue

        print(f"\n[>>] {nome} — Lei {numero}/{ano_str}")
        ano = int(ano_str)
        candidatos = url_para_lei(numero, ano)
        caminho_html = None
        url_ok = None

        for url in candidatos:
            caminho_html = baixar_html(url, forcar=False)
            if caminho_html:
                url_ok = url
                break

        if not caminho_html:
            print(f"     [ERRO] Nao encontrada em {len(candidatos)} URLs tentadas")
            erro += 1
            continue

        try:
            dados = parsear_lei(caminho_html, url_origem=url_ok)
            path = salvar_nota(dados, OUTPUT_DIR, conn=None)
            if path:
                chars = len(dados.get("texto_vigente", ""))
                frags = len(dados.get("fragmentos_revogados", []))
                print(f"     [OK] {path.name} — {chars} chars, {frags} revogados")
                ok += 1
            else:
                erro += 1
        except Exception as e:
            print(f"     [ERRO] Parse falhou: {e}")
            erro += 1

        time.sleep(1.5)  # respeitar rate limit do Planalto

    print()
    print("=" * 65)
    print(f"Concluido: {ok} novas | {skip} ja existiam | {erro} erros")
    print(f"Arquivos em: {OUTPUT_DIR}")
    print()
    print("Proximos passos:")
    print("  python scripts/ingerir_legislacao_supabase.py")


if __name__ == "__main__":
    main()

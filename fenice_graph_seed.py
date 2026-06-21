#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fenice bRain — Seed Data do Knowledge Graph Jurídico

Insere os nós iniciais do grafo (jurisconsultos, filósofos, códigos) e
cria arestas de exemplo que ligam pensadores às normas que influenciaram.

Pré-requisito:
  1. psql -d fenice_brain -f scripts/fenice_graph_schema.sql
  2. Variáveis de ambiente configuradas no .env:
       DB_HOST, DB_NAME, DB_USER, DB_PASS, DB_PORT

Uso:
  python scripts/fenice_graph_seed.py [--limpar]

  --limpar  : apaga todos os dados das tabelas antes de reinserir (útil para reset)
"""
import os
import sys
from pathlib import Path
from typing import List, Tuple, Optional

import psycopg2
import psycopg2.extras

# ── Config ─────────────────────────────────────────────────────────────────────

def _cfg() -> dict:
    """Lê credenciais do .env ou variáveis de ambiente."""
    env_file = Path(__file__).parent.parent / ".env"
    if env_file.exists():
        for linha in env_file.read_text(encoding="utf-8").splitlines():
            if "=" in linha and not linha.strip().startswith("#"):
                k, _, v = linha.partition("=")
                os.environ.setdefault(k.strip(), v.strip())
    return {
        "host":     os.environ.get("DB_HOST", "localhost"),
        "dbname":   os.environ.get("DB_NAME", "fenice_brain"),
        "user":     os.environ.get("DB_USER", "postgres"),
        "password": os.environ.get("DB_PASS", ""),
        "port":     int(os.environ.get("DB_PORT", "5432")),
    }


# ── Dados seed ─────────────────────────────────────────────────────────────────

# Nós: (tipo, identificador, titulo, descricao, url_origem)
NOS: List[Tuple] = [
    # ── Filósofos e Jurisconsultos ─────────────────────────────────────────────
    (
        "filosofo", "Beccaria",
        "Cesare Beccaria (1738-1794)",
        "Iluminista italiano; obra 'Dos Delitos e das Penas' (1764) fundamentou o "
        "princípio da legalidade penal, humanização das penas e proporcionalidade.",
        "https://pt.wikipedia.org/wiki/Cesare_Beccaria",
    ),
    (
        "filosofo", "Kelsen",
        "Hans Kelsen (1881-1973)",
        "Jurista austríaco; criador do positivismo normativista e da Teoria Pura do "
        "Direito; projetou o controle concentrado de constitucionalidade.",
        "https://pt.wikipedia.org/wiki/Hans_Kelsen",
    ),
    (
        "filosofo", "Miguel Reale",
        "Miguel Reale (1910-2006)",
        "Filósofo e jurista brasileiro; criador da Teoria Tridimensional do Direito "
        "(fato, valor, norma); coordenou a elaboração do Código Civil de 2002.",
        "https://pt.wikipedia.org/wiki/Miguel_Reale",
    ),
    (
        "filosofo", "Pontes de Miranda",
        "Francisco Cavalcanti Pontes de Miranda (1892-1979)",
        "Jurista e polímata brasileiro; obra monumental em direito civil e processual; "
        "teoria dos fatos jurídicos (suporte fático / incidência / eficácia).",
        "https://pt.wikipedia.org/wiki/Pontes_de_Miranda",
    ),
    (
        "filosofo", "Clóvis Beviláqua",
        "Clóvis Beviláqua (1859-1944)",
        "Jurista e codificador do Código Civil de 1916; professor da Faculdade de "
        "Direito do Recife; obra em direito de família e sucessões.",
        "https://pt.wikipedia.org/wiki/Cl%C3%B3vis_Bevil%C3%A1qua",
    ),
    (
        "filosofo", "Jeremy Bentham",
        "Jeremy Bentham (1748-1832)",
        "Filósofo inglês; fundador do utilitarismo; influenciou o direito penal "
        "moderno com a teoria da prevenção das penas e o Panóptico.",
        "https://pt.wikipedia.org/wiki/Jeremy_Bentham",
    ),
    (
        "filosofo", "John Locke",
        "John Locke (1632-1704)",
        "Filósofo inglês; teoria do contrato social e dos direitos naturais "
        "(vida, liberdade, propriedade); base do constitucionalismo liberal.",
        "https://pt.wikipedia.org/wiki/John_Locke",
    ),
    (
        "filosofo", "Montesquieu",
        "Montesquieu (1689-1755)",
        "Filósofo e jurista francês; 'Do Espírito das Leis' (1748); formulou a "
        "teoria da separação dos poderes (Executivo, Legislativo, Judiciário).",
        "https://pt.wikipedia.org/wiki/Montesquieu",
    ),
    (
        "filosofo", "Rousseau",
        "Jean-Jacques Rousseau (1712-1778)",
        "Filósofo suíço; teoria do contrato social e vontade geral; influência direta "
        "no constitucionalismo democrático e na soberania popular.",
        "https://pt.wikipedia.org/wiki/Jean-Jacques_Rousseau",
    ),
    (
        "filosofo", "Norberto Bobbio",
        "Norberto Bobbio (1909-2004)",
        "Filósofo do direito e da política italiano; obras sobre positivismo jurídico, "
        "democracia e direitos humanos; influência no neoconstitucionalismo.",
        "https://pt.wikipedia.org/wiki/Norberto_Bobbio",
    ),
    (
        "filosofo", "Ronald Dworkin",
        "Ronald Dworkin (1931-2013)",
        "Filósofo do direito norte-americano; crítico do positivismo; teoria dos "
        "princípios como direito ('Levando os Direitos a Sério', 'O Império do Direito').",
        "https://pt.wikipedia.org/wiki/Ronald_Dworkin",
    ),
    (
        "filosofo", "Robert Alexy",
        "Robert Alexy (1945-)",
        "Filósofo do direito alemão; teoria dos direitos fundamentais como princípios; "
        "método da ponderação e proporcionalidade; influência no STF.",
        "https://pt.wikipedia.org/wiki/Robert_Alexy",
    ),

    # ── Conceitos Jurídicos ────────────────────────────────────────────────────
    (
        "conceito", "Positivismo Juridico",
        "Positivismo Jurídico",
        "Corrente que identifica o direito com a norma posta pelo Estado, separando "
        "direito e moral. Kelsen é seu maior expoente no século XX.",
        None,
    ),
    (
        "conceito", "Utilitarismo",
        "Utilitarismo",
        "Corrente filosófica que avalia ações pela utilidade (maior felicidade para "
        "o maior número). Bentham e Mill são os principais expoentes.",
        None,
    ),
    (
        "conceito", "Separacao dos Poderes",
        "Separação dos Poderes",
        "Princípio constitucional que divide o poder estatal em Executivo, Legislativo "
        "e Judiciário independentes e harmônicos (CF/88, art. 2º).",
        None,
    ),
    (
        "conceito", "Proporcionalidade",
        "Proporcionalidade",
        "Princípio que exige adequação, necessidade e proporcionalidade em sentido "
        "estrito na restrição de direitos fundamentais. Consagrado pelo STF.",
        None,
    ),
    (
        "conceito", "Teoria Tridimensional do Direito",
        "Teoria Tridimensional do Direito",
        "Concepção de Miguel Reale: o fenômeno jurídico integra fato (sociológico), "
        "valor (filosófico) e norma (científico-jurídica) de forma inseparável.",
        None,
    ),

    # ── Leis / Códigos ─────────────────────────────────────────────────────────
    (
        "lei", "Lei 10406/2002",
        "Código Civil Brasileiro",
        "Institui o Código Civil. Revogou o CC/1916 (Lei 3.071/1916). "
        "Coordenado por Miguel Reale; vigência a partir de 11/01/2003.",
        "https://www.planalto.gov.br/ccivil_03/leis/2002/l10406compilada.htm",
    ),
    (
        "lei", "Decreto-Lei 2848/1940",
        "Código Penal Brasileiro",
        "Código Penal Federal. Inspirado nas correntes positivista e clássica do "
        "direito penal; influência de Beccaria e da Escola Positiva italiana.",
        "https://www.planalto.gov.br/ccivil_03/decreto-lei/del2848compilado.htm",
    ),
    (
        "lei", "Lei 13105/2015",
        "Código de Processo Civil",
        "Novo CPC; revogou o CPC/1973 (Lei 5.869/1973). Ênfase em princípios "
        "constitucionais, cooperação processual e precedentes vinculantes.",
        "https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm",
    ),
    (
        "lei", "CF/88",
        "Constituição Federal de 1988",
        "Constituição da República Federativa do Brasil. 'Constituição Cidadã'. "
        "Fundamento de validade de todo o ordenamento jurídico brasileiro.",
        "https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm",
    ),
    (
        "lei", "Lei 8078/1990",
        "Código de Defesa do Consumidor",
        "CDC; estabelece normas de proteção e defesa do consumidor. "
        "Marco na constitucionalização do direito privado.",
        "https://www.planalto.gov.br/ccivil_03/leis/l8078compilado.htm",
    ),
    (
        "lei", "Lei 14133/2021",
        "Lei de Licitações e Contratos Administrativos",
        "Nova Lei de Licitações; revogou a Lei 8.666/1993, Lei 10.520/2002 e "
        "parte do RDC. Vigência plena a partir de 1º/04/2023.",
        "https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2021/lei/l14133.htm",
    ),

    # ── Artigos-chave ──────────────────────────────────────────────────────────
    (
        "artigo", "Art. 5 CF",
        "Art. 5º da CF/88 — Direitos e Garantias Fundamentais",
        "Rol de direitos e garantias fundamentais: vida, liberdade, igualdade, "
        "segurança e propriedade; legalidade, contraditório, ampla defesa, etc.",
        "https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm#art5",
    ),
    (
        "artigo", "Art. 2 CF",
        "Art. 2º da CF/88 — Separação dos Poderes",
        "São Poderes da União, independentes e harmônicos entre si, o Legislativo, "
        "o Executivo e o Judiciário.",
        "https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm#art2",
    ),
    (
        "artigo", "Art. 927 CC",
        "Art. 927 do Código Civil — Responsabilidade Civil Objetiva",
        "Aquele que, por ato ilícito (arts. 186 e 187), causar dano a outrem, "
        "fica obrigado a repará-lo. Parágrafo único: responsabilidade objetiva.",
        "https://www.planalto.gov.br/ccivil_03/leis/2002/l10406compilada.htm#art927",
    ),
    (
        "artigo", "Art. 186 CC",
        "Art. 186 do Código Civil — Ato Ilícito",
        "Aquele que, por ação ou omissão voluntária, negligência ou imprudência, "
        "violar direito e causar dano a outrem, comete ato ilícito.",
        "https://www.planalto.gov.br/ccivil_03/leis/2002/l10406compilada.htm#art186",
    ),
    (
        "artigo", "Art. 1 CP",
        "Art. 1º do Código Penal — Princípio da Legalidade",
        "Não há crime sem lei anterior que o defina. Não há pena sem prévia "
        "cominação legal. (nullum crimen, nulla poena sine lege)",
        "https://www.planalto.gov.br/ccivil_03/decreto-lei/del2848compilado.htm#art1",
    ),
]

# Arestas: (identificador_origem, identificador_destino, tipo_relacao, peso, fonte)
ARESTAS: List[Tuple] = [
    # Beccaria → influenciou fundamentos do Art. 1º CP (princípio da legalidade)
    ("Beccaria",   "Art. 1 CP",      "influenciado_por", 1.0, "curadoria"),
    # Beccaria → influenciou Art. 5 CF (garantias penais)
    ("Beccaria",   "Art. 5 CF",      "influenciado_por", 0.9, "curadoria"),
    # Beccaria → fundamenta o Utilitarismo penal (compartilha bases iluministas)
    ("Beccaria",   "Utilitarismo",   "derivado_de",      0.7, "curadoria"),
    # Bentham → criou o Utilitarismo
    ("Jeremy Bentham", "Utilitarismo", "derivado_de",    1.0, "curadoria"),
    # Utilitarismo → influenciou Código Penal
    ("Utilitarismo", "Decreto-Lei 2848/1940", "influenciado_por", 0.8, "curadoria"),

    # Kelsen → criou Positivismo Jurídico
    ("Kelsen",     "Positivismo Juridico", "derivado_de", 1.0, "curadoria"),
    # Kelsen → fundamentou controle concentrado de constitucionalidade (STF)
    ("Kelsen",     "CF/88",          "fundamentado_em",  0.8, "curadoria"),
    # Bobbio → derivado do Positivismo Jurídico
    ("Norberto Bobbio", "Positivismo Juridico", "derivado_de", 0.9, "curadoria"),

    # Dworkin e Alexy → críticos do positivismo → teoria dos princípios
    ("Ronald Dworkin", "Positivismo Juridico", "contraria",   1.0, "curadoria"),
    ("Robert Alexy",   "Proporcionalidade",    "derivado_de", 1.0, "curadoria"),
    # Proporcionalidade → consagrada na CF/88 (implicitamente no Art. 5)
    ("Proporcionalidade", "Art. 5 CF", "fundamentado_em", 0.9, "curadoria"),

    # Montesquieu → Separação dos Poderes
    ("Montesquieu",  "Separacao dos Poderes", "derivado_de", 1.0, "curadoria"),
    # Separação dos Poderes → Art. 2 CF
    ("Separacao dos Poderes", "Art. 2 CF", "fundamentado_em", 1.0, "curadoria"),

    # Locke e Rousseau → Art. 5 CF (direitos naturais / soberania popular)
    ("John Locke",  "Art. 5 CF", "influenciado_por", 0.8, "curadoria"),
    ("Rousseau",    "Art. 5 CF", "influenciado_por", 0.7, "curadoria"),

    # Miguel Reale → Teoria Tridimensional → CC/2002
    ("Miguel Reale", "Teoria Tridimensional do Direito", "derivado_de", 1.0, "curadoria"),
    ("Teoria Tridimensional do Direito", "Lei 10406/2002", "fundamentado_em", 0.9, "curadoria"),

    # Clóvis Beviláqua → CC/1916 predecessor → migração conceitual ao CC/2002
    ("Clóvis Beviláqua", "Lei 10406/2002", "influenciado_por", 0.6, "curadoria"),

    # Pontes de Miranda → influenciou teoria dos fatos jurídicos no CC
    ("Pontes de Miranda", "Lei 10406/2002", "influenciado_por", 0.8, "curadoria"),
    ("Pontes de Miranda", "Art. 186 CC",    "influenciado_por", 0.7, "curadoria"),

    # Artigos do CC se relacionam entre si
    ("Art. 927 CC",  "Art. 186 CC",    "fundamentado_em",  1.0, "curadoria"),
    ("Art. 927 CC",  "Lei 10406/2002", "regulamentado_por", 1.0, "curadoria"),
    ("Art. 186 CC",  "Lei 10406/2002", "regulamentado_por", 1.0, "curadoria"),
    ("Art. 1 CP",    "Decreto-Lei 2848/1940", "regulamentado_por", 1.0, "curadoria"),
    ("Art. 5 CF",    "CF/88",          "regulamentado_por", 1.0, "curadoria"),
    ("Art. 2 CF",    "CF/88",          "regulamentado_por", 1.0, "curadoria"),
]


# ── Persistência ───────────────────────────────────────────────────────────────

INSERT_NO = """
INSERT INTO grafo_nos (tipo, identificador, titulo, descricao, url_origem)
VALUES (%(tipo)s, %(identificador)s, %(titulo)s, %(descricao)s, %(url_origem)s)
ON CONFLICT (identificador) DO UPDATE SET
    titulo    = EXCLUDED.titulo,
    descricao = EXCLUDED.descricao,
    url_origem = COALESCE(EXCLUDED.url_origem, grafo_nos.url_origem);
"""

INSERT_ARESTA = """
INSERT INTO grafo_arestas (no_origem_id, no_destino_id, tipo_relacao, peso, fonte)
VALUES (
    (SELECT id FROM grafo_nos WHERE identificador = %(origem)s),
    (SELECT id FROM grafo_nos WHERE identificador = %(destino)s),
    %(tipo_relacao)s,
    %(peso)s,
    %(fonte)s
)
ON CONFLICT (no_origem_id, no_destino_id, tipo_relacao) DO UPDATE SET
    peso  = EXCLUDED.peso,
    fonte = EXCLUDED.fonte;
"""


def run_seed(limpar: bool = False) -> None:
    sys.stdout.reconfigure(encoding="utf-8")

    conn = psycopg2.connect(**_cfg())
    print(f"  Conectado: {_cfg()['dbname']}@{_cfg()['host']}")

    with conn:
        with conn.cursor() as cur:
            if limpar:
                print("  Limpando tabelas...")
                cur.execute("DELETE FROM grafo_arestas;")
                cur.execute("DELETE FROM grafo_nos;")
                print("  Tabelas esvaziadas.")

            # Insere nós
            print(f"\n  Inserindo {len(NOS)} nos...")
            for no in NOS:
                tipo, identificador, titulo, descricao, url_origem = no
                cur.execute(INSERT_NO, {
                    "tipo": tipo,
                    "identificador": identificador,
                    "titulo": titulo,
                    "descricao": descricao,
                    "url_origem": url_origem,
                })
            print(f"  {len(NOS)} nos inseridos/atualizados.")

            # Insere arestas
            print(f"\n  Inserindo {len(ARESTAS)} arestas...")
            erros = 0
            for aresta in ARESTAS:
                origem, destino, tipo_rel, peso, fonte = aresta
                try:
                    cur.execute(INSERT_ARESTA, {
                        "origem": origem,
                        "destino": destino,
                        "tipo_relacao": tipo_rel,
                        "peso": peso,
                        "fonte": fonte,
                    })
                except psycopg2.Error as e:
                    print(f"  Aviso — aresta ignorada ({origem} -> {destino}): {e}")
                    erros += 1
                    conn.rollback()

            print(f"  {len(ARESTAS) - erros} arestas inseridas/atualizadas ({erros} ignoradas).")

    conn.close()
    print("\n  Seed concluido.")


# ── CLI ────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    limpar = "--limpar" in sys.argv
    if limpar:
        print("AVISO: modo --limpar apagara todos os dados das tabelas grafo_*.")
        confirma = input("Continuar? (s/N): ").strip().lower()
        if confirma != "s":
            print("Abortado.")
            sys.exit(0)

    run_seed(limpar=limpar)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Camada de persistencia — Planalto Pipeline -> PostgreSQL

Configuracao via variaveis de ambiente:
  DB_HOST  = localhost (ou nome do servico no docker-compose)
  DB_NAME  = fenice_brain
  DB_USER  = postgres
  DB_PASS  = sua_senha
  DB_PORT  = 5432
"""
import os
import psycopg2
import psycopg2.extras
from typing import Dict, Optional


# ── Configuracao ──────────────────────────────────────────────────────────────

def _cfg() -> Dict:
    """Le credenciais de variaveis de ambiente."""
    return {
        "host":     os.environ.get("DB_HOST", "localhost"),
        "dbname":   os.environ.get("DB_NAME", "fenice_brain"),
        "user":     os.environ.get("DB_USER", "postgres"),
        "password": os.environ.get("DB_PASS", ""),
        "port":     int(os.environ.get("DB_PORT", "5432")),
    }


# ── SQL ───────────────────────────────────────────────────────────────────────

UPSERT_SQL = """
INSERT INTO legislacao_brasileira (
    esfera, tipo_ato, numero_ano, ementa,
    texto_vigente, texto_original_html, fragmentos_revogados,
    url_origem, data_assinatura
) VALUES (
    %(esfera)s, %(tipo_ato)s, %(numero_ano)s, %(ementa)s,
    %(texto_vigente)s, %(texto_original_html)s, %(fragmentos_revogados)s,
    %(url_origem)s, %(data_assinatura)s
)
ON CONFLICT (url_origem) DO UPDATE SET
    texto_vigente        = EXCLUDED.texto_vigente,
    texto_original_html  = EXCLUDED.texto_original_html,
    fragmentos_revogados = EXCLUDED.fragmentos_revogados,
    ementa               = EXCLUDED.ementa,
    data_captura         = CURRENT_TIMESTAMP;
"""

BUSCA_SQL = """
SELECT
    numero_ano,
    tipo_ato,
    ementa,
    ts_headline('portuguese', texto_vigente,
        to_tsquery('portuguese', %(query_ts)s),
        'MaxFragments=3,FragmentDelimiter=" ... "'
    ) AS trecho_relevante,
    ts_rank(busca_idx, to_tsquery('portuguese', %(query_ts)s)) AS relevancia
FROM legislacao_brasileira
WHERE busca_idx @@ to_tsquery('portuguese', %(query_ts)s)
ORDER BY relevancia DESC
LIMIT %(limite)s;
"""


# ── Classe PlanaltoDB ─────────────────────────────────────────────────────────

class PlanaltoDB:
    """Conexao e operacoes de persistencia para legislacao no PostgreSQL."""

    def __init__(self):
        self.conn: Optional[psycopg2.extensions.connection] = None

    def conectar(self) -> bool:
        cfg = _cfg()
        try:
            self.conn = psycopg2.connect(**cfg)
            print(f"  [OK] PostgreSQL: {cfg['dbname']}@{cfg['host']}")
            return True
        except psycopg2.Error as e:
            print(f"  [ERRO] Falha ao conectar ao banco: {e}")
            return False

    def upsert_lei(self, dados: Dict) -> bool:
        """Insere ou atualiza uma lei (upsert por url_origem)."""
        payload = {
            "esfera":               dados.get("esfera", "Federal"),
            "tipo_ato":             dados.get("tipo_ato", "Lei Ordinaria"),
            "numero_ano":           f"Lei {dados['numero']}/{dados['ano']}",
            "ementa":               dados.get("ementa") or dados.get("titulo", ""),
            "texto_vigente":        dados.get("texto_vigente", ""),
            "texto_original_html":  dados.get("html_bruto", ""),
            "fragmentos_revogados": len(dados.get("fragmentos_revogados", [])),
            "url_origem":           dados.get("url_origem", ""),
            "data_assinatura":      None,
        }
        try:
            with self.conn.cursor() as cur:
                cur.execute(UPSERT_SQL, payload)
            self.conn.commit()
            return True
        except psycopg2.Error as e:
            self.conn.rollback()
            print(f"  [ERRO] Upsert falhou ({payload['numero_ano']}): {e}")
            return False

    def buscar(self, termos: str, limite: int = 10):
        """Full-text search em portugues. Separa termos com ' & '."""
        query_ts = " & ".join(termos.split())
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(BUSCA_SQL, {"query_ts": query_ts, "limite": limite})
            return cur.fetchall()

    def fechar(self):
        if self.conn:
            self.conn.close()

    def __enter__(self):
        self.conectar()
        return self

    def __exit__(self, *_):
        self.fechar()

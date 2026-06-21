#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Camada de persistência — Planalto Pipeline → PostgreSQL / Supabase

Configuração via variáveis de ambiente (.env):
  DB_HOST     = localhost (ou host.supabase.co)
  DB_NAME     = fenice_brain (ou postgres no Supabase)
  DB_USER     = postgres
  DB_PASS     = sua_senha
  DB_PORT     = 5432

Schema SQL necessário (criar uma vez):
  Ver: planalto_schema.sql
"""
import os
import datetime
import psycopg2
import psycopg2.extras
from pathlib import Path
from typing import Dict, Optional

# ── Configuração via env ──────────────────────────────────────────────────────

def _cfg() -> Dict:
    """Lê credenciais do .env ou variáveis de ambiente."""
    env_file = Path(__file__).parent.parent / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.strip().startswith("#"):
                k, _, v = line.partition("=")
                os.environ.setdefault(k.strip(), v.strip())

    return {
        "host":     os.environ.get("DB_HOST", "localhost"),
        "dbname":   os.environ.get("DB_NAME", "fenice_brain"),
        "user":     os.environ.get("DB_USER", "postgres"),
        "password": os.environ.get("DB_PASS", ""),
        "port":     int(os.environ.get("DB_PORT", "5432")),
    }


# ── Schema SQL ────────────────────────────────────────────────────────────────

SCHEMA_SQL = """
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Tenta criar pgvector (opcional — para busca semântica futura)
-- CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS legislacao_brasileira (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    esfera              VARCHAR(20)  NOT NULL DEFAULT 'Federal',
    tipo_ato            VARCHAR(50)  NOT NULL,
    numero_ano          VARCHAR(30)  UNIQUE NOT NULL,
    ementa              TEXT,
    texto_vigente       TEXT         NOT NULL,
    texto_original_html TEXT,
    fragmentos_revogados INTEGER     NOT NULL DEFAULT 0,
    url_origem          TEXT         UNIQUE NOT NULL,
    data_assinatura     DATE,
    data_captura        TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    -- Full-Text Search em português (gerado automaticamente)
    busca_idx           tsvector GENERATED ALWAYS AS (
        to_tsvector('portuguese',
            coalesce(numero_ano, '') || ' ' ||
            coalesce(ementa, '') || ' ' ||
            coalesce(texto_vigente, '')
        )
    ) STORED
);

CREATE INDEX IF NOT EXISTS idx_legislacao_busca ON legislacao_brasileira USING gin(busca_idx);
CREATE INDEX IF NOT EXISTS idx_legislacao_tipo   ON legislacao_brasileira(tipo_ato);
CREATE INDEX IF NOT EXISTS idx_legislacao_esfera ON legislacao_brasileira(esfera);
"""

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


# ── Conexão ───────────────────────────────────────────────────────────────────

class PlanaltoDB:
    def __init__(self):
        self.conn: Optional[psycopg2.extensions.connection] = None

    def conectar(self) -> bool:
        try:
            self.conn = psycopg2.connect(**_cfg())
            print(f"  ✅ PostgreSQL: {_cfg()['dbname']}@{_cfg()['host']}")
            return True
        except psycopg2.Error as e:
            print(f"  ❌ Erro ao conectar: {e}")
            return False

    def inicializar_schema(self):
        """Cria tabela e índices se não existirem."""
        with self.conn.cursor() as cur:
            cur.execute(SCHEMA_SQL)
        self.conn.commit()
        print("  ✅ Schema OK")

    def upsert_lei(self, dados: Dict) -> bool:
        """Insere ou atualiza uma lei (Upsert por url_origem)."""
        payload = {
            "esfera":               dados.get("esfera", "Federal"),
            "tipo_ato":             dados.get("tipo_ato", "Lei Ordinária"),
            "numero_ano":           f"Lei {dados['numero']}/{dados['ano']}",
            "ementa":               dados.get("titulo", ""),
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
            print(f"  ❌ Upsert falhou ({payload['numero_ano']}): {e}")
            return False

    def buscar(self, termos: str, limite: int = 10):
        """Full-text search em português. Separa termos com ' & '."""
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


# ── CLI de teste ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")

    with PlanaltoDB() as db:
        if not db.conn:
            print("⚠️  Sem conexão. Configure .env com DB_HOST, DB_NAME, DB_USER, DB_PASS")
            sys.exit(1)

        db.inicializar_schema()

        # Teste de busca
        termos = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "licitacao contrato"
        print(f"\n🔍 Buscando: '{termos}'")
        resultados = db.buscar(termos, limite=5)
        for r in resultados:
            print(f"\n  📄 {r['numero_ano']} — {r['tipo_ato']}")
            print(f"     {r['ementa'][:80]}...")
            print(f"     Relevância: {r['relevancia']:.4f}")
            print(f"     Trecho: {r['trecho_relevante'][:200]}...")

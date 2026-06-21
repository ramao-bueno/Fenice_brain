-- Fenice bRain — Schema PostgreSQL para Legislacao Brasileira
-- Execute uma vez: psql -d fenice_brain -f planalto_schema.sql
-- Compativel com Supabase (PostgreSQL 15+)

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
-- CREATE EXTENSION IF NOT EXISTS vector;   -- descomente para busca semantica futura

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

    busca_idx tsvector GENERATED ALWAYS AS (
        to_tsvector('portuguese',
            coalesce(numero_ano, '') || ' ' ||
            coalesce(ementa, '') || ' ' ||
            coalesce(texto_vigente, '')
        )
    ) STORED
);

CREATE INDEX IF NOT EXISTS idx_legislacao_busca  ON legislacao_brasileira USING gin(busca_idx);
CREATE INDEX IF NOT EXISTS idx_legislacao_tipo    ON legislacao_brasileira(tipo_ato);
CREATE INDEX IF NOT EXISTS idx_legislacao_esfera  ON legislacao_brasileira(esfera);
CREATE INDEX IF NOT EXISTS idx_legislacao_captura ON legislacao_brasileira(data_captura DESC);

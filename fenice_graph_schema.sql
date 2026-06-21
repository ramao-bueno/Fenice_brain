-- Fenice bRain — Schema PostgreSQL: Knowledge Graph Jurídico
-- Execute: psql -d fenice_brain -f fenice_graph_schema.sql
-- Compatível com Supabase (PostgreSQL 15+)
-- Depende de: planalto_schema.sql (uuid-ossp já carregado)

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ── Nós do Grafo ──────────────────────────────────────────────────────────────
-- Cada conceito/entidade jurídica ou filosófica é um nó.
-- Tipos suportados: 'lei', 'artigo', 'sumula', 'filosofo', 'conceito', 'doutrina'

CREATE TABLE IF NOT EXISTS grafo_nos (
    id            UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tipo          VARCHAR(30)  NOT NULL,
    -- Tipos: 'lei', 'artigo', 'sumula', 'filosofo', 'conceito', 'doutrina'
    identificador VARCHAR(100) UNIQUE NOT NULL,
    -- Exemplos: 'Lei 15384/2026', 'Art. 5 CF', 'Beccaria', 'Utilitarismo'
    titulo        TEXT,
    descricao     TEXT,
    url_origem    TEXT,
    criado_em     TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_nos_tipo          ON grafo_nos(tipo);
CREATE INDEX IF NOT EXISTS idx_nos_identificador ON grafo_nos(identificador);

-- ── Arestas do Grafo ──────────────────────────────────────────────────────────
-- Relações direcionadas entre nós.
-- Tipos de relação suportados:
--   'influenciado_por'    — doutrina/filósofo influenciou norma ou conceito
--   'revogado_por'        — dispositivo revogado por lei posterior
--   'regulamentado_por'   — artigo regulamentado por decreto/instrução
--   'fundamentado_em'     — decisão fundamentada em princípio/doutrina
--   'contraria'           — posição contrária a outro dispositivo ou entendimento
--   'complementa'         — complementa ou amplia outro dispositivo
--   'interpreta'          — jurisprudência/doutrina interpreta dispositivo
--   'aplica'              — julgado aplica dispositivo ao caso concreto
--   'derivado_de'         — conceito derivado de corrente doutrinária

CREATE TABLE IF NOT EXISTS grafo_arestas (
    id             UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    no_origem_id   UUID NOT NULL REFERENCES grafo_nos(id) ON DELETE CASCADE,
    no_destino_id  UUID NOT NULL REFERENCES grafo_nos(id) ON DELETE CASCADE,
    tipo_relacao   VARCHAR(50) NOT NULL,
    peso           FLOAT DEFAULT 1.0,   -- relevância da conexão (para ranking no grafo)
    fonte          TEXT,                -- de onde veio essa conexão (pipeline, curadoria manual)
    criado_em      TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(no_origem_id, no_destino_id, tipo_relacao)
);

CREATE INDEX IF NOT EXISTS idx_arestas_origem  ON grafo_arestas(no_origem_id);
CREATE INDEX IF NOT EXISTS idx_arestas_destino ON grafo_arestas(no_destino_id);
CREATE INDEX IF NOT EXISTS idx_arestas_tipo    ON grafo_arestas(tipo_relacao);

-- ── Views de Conveniência ─────────────────────────────────────────────────────

-- Vizinhos de um nó (por identificador)
-- Uso: SELECT * FROM v_vizinhos_grafo WHERE origem = 'Beccaria';
CREATE OR REPLACE VIEW v_vizinhos_grafo AS
SELECT
    o.identificador  AS origem,
    o.tipo           AS tipo_origem,
    a.tipo_relacao,
    a.peso,
    d.identificador  AS destino,
    d.tipo           AS tipo_destino,
    a.fonte
FROM grafo_arestas a
JOIN grafo_nos o ON a.no_origem_id  = o.id
JOIN grafo_nos d ON a.no_destino_id = d.id;

-- Exemplos de queries:
-- Quem influenciou o Art. 5 CF?
--   SELECT * FROM v_vizinhos_grafo
--   WHERE destino = 'Art. 5 CF' AND tipo_relacao = 'influenciado_por';
--
-- Grafo expandido de Beccaria (profundidade 1):
--   SELECT * FROM v_vizinhos_grafo WHERE origem = 'Beccaria';
--
-- Todos os nós do tipo 'filosofo':
--   SELECT identificador, titulo, descricao FROM grafo_nos WHERE tipo = 'filosofo';

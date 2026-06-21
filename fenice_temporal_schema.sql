-- Fenice bRain — Schema PostgreSQL: Versionamento Temporal de Legislação
-- Execute: psql -d fenice_brain -f fenice_temporal_schema.sql
-- Compatível com Supabase (PostgreSQL 15+)
-- Depende de: planalto_schema.sql (tabela legislacao_brasileira + uuid-ossp)

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ── Histórico de Revogações/Alterações ───────────────────────────────────────
-- Registra cada modificação sofrida por um artigo/dispositivo ao longo do tempo.
-- Permite queries temporais: "Como era o Art. 927 do CC em 2020?"

CREATE TABLE IF NOT EXISTS legislacao_historico (
    id               UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    lei_id           UUID REFERENCES legislacao_brasileira(id) ON DELETE CASCADE,
    numero_ano       VARCHAR(30)  NOT NULL,   -- ex: 'Lei 10406/2002'
    artigo           VARCHAR(20),             -- ex: 'Art. 927'
    texto_original   TEXT         NOT NULL,   -- texto antes da alteração
    texto_vigente    TEXT,                    -- texto após alteração (NULL se apenas revogado)
    lei_modificadora VARCHAR(30),             -- ex: 'Lei 14133/2021'
    data_modificacao DATE,
    tipo_modificacao VARCHAR(20)  NOT NULL,   -- 'revogacao', 'alteracao', 'acrescimo', 'renumeracao'
    registrado_em    TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_tipo_modificacao CHECK (
        tipo_modificacao IN ('revogacao', 'alteracao', 'acrescimo', 'renumeracao')
    )
);

CREATE INDEX IF NOT EXISTS idx_hist_numero_ano ON legislacao_historico(numero_ano);
CREATE INDEX IF NOT EXISTS idx_hist_artigo     ON legislacao_historico(artigo);
CREATE INDEX IF NOT EXISTS idx_hist_data_mod   ON legislacao_historico(data_modificacao);
CREATE INDEX IF NOT EXISTS idx_hist_lei_id     ON legislacao_historico(lei_id);
CREATE INDEX IF NOT EXISTS idx_hist_tipo       ON legislacao_historico(tipo_modificacao);

-- ── View: Linha do Tempo de um Artigo ────────────────────────────────────────
-- Mostra todas as alterações de um artigo em ordem cronológica.
-- Uso: SELECT * FROM v_linha_do_tempo WHERE artigo = 'Art. 927'
--        AND numero_ano = 'Lei 10406/2002' ORDER BY data_modificacao;

CREATE OR REPLACE VIEW v_linha_do_tempo AS
SELECT
    numero_ano,
    artigo,
    tipo_modificacao,
    lei_modificadora,
    data_modificacao,
    LEFT(texto_original, 200) AS texto_original_resumo,
    LEFT(texto_vigente,  200) AS texto_vigente_resumo,
    registrado_em
FROM legislacao_historico
ORDER BY numero_ano, artigo, data_modificacao NULLS LAST;

-- ── View: Revogações Recentes ─────────────────────────────────────────────────
-- Uso: SELECT * FROM v_revogacoes_recentes LIMIT 20;

CREATE OR REPLACE VIEW v_revogacoes_recentes AS
SELECT
    numero_ano,
    artigo,
    lei_modificadora,
    data_modificacao,
    LEFT(texto_original, 150) AS fragmento_revogado
FROM legislacao_historico
WHERE tipo_modificacao = 'revogacao'
ORDER BY data_modificacao DESC NULLS LAST, registrado_em DESC;

-- Exemplos de queries temporais:
-- "Como era o Art. 927 do CC antes de 2021?"
--   SELECT texto_original FROM legislacao_historico
--   WHERE numero_ano = 'Lei 10406/2002' AND artigo = 'Art. 927'
--     AND data_modificacao < '2021-01-01'
--   ORDER BY data_modificacao DESC LIMIT 1;
--
-- "Quais artigos do CC foram alterados nos últimos 2 anos?"
--   SELECT DISTINCT artigo, lei_modificadora, data_modificacao
--   FROM legislacao_historico
--   WHERE numero_ano = 'Lei 10406/2002'
--     AND data_modificacao >= CURRENT_DATE - INTERVAL '2 years'
--   ORDER BY data_modificacao DESC;

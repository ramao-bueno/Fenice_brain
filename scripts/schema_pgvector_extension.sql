-- =====================================================================
-- PGVECTOR Extension — Fenice Brain STF Embeddings
-- PostgreSQL 12+ com pgvector
-- =====================================================================

-- Criar extensão
CREATE EXTENSION IF NOT EXISTS vector;

-- =====================================================================
-- Adicionar coluna de embedding à tabela stf.sumulas
-- =====================================================================
ALTER TABLE stf.sumulas
ADD COLUMN IF NOT EXISTS embedding vector(1536);

-- =====================================================================
-- Índices para busca eficiente
-- =====================================================================

-- IVFFLAT é recomendado para < 1M vetores (nosso caso)
CREATE INDEX IF NOT EXISTS idx_sumulas_embedding_ivfflat ON stf.sumulas
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Alternativa: HNSW (melhor para buscas mas mais lento para inserts)
-- CREATE INDEX IF NOT EXISTS idx_sumulas_embedding_hnsw ON stf.sumulas
-- USING hnsw (embedding vector_cosine_ops)
-- WITH (m = 16, ef_construction = 64);

-- =====================================================================
-- FUNÇÃO: Busca Semântica por Embedding
-- =====================================================================
CREATE OR REPLACE FUNCTION stf.buscar_semanticamente(
    p_query_text TEXT,
    p_limite INT DEFAULT 10,
    p_similarity_threshold FLOAT DEFAULT 0.5
)
RETURNS TABLE(
    numero_identificador VARCHAR,
    tipo VARCHAR,
    setor_afetado VARCHAR,
    similarity_score FLOAT,
    enunciado_original TEXT
) AS $$
DECLARE
    v_embedding vector(1536);
    v_query_embedding vector(1536);
BEGIN
    -- NOTA: Em produção, você geraria o embedding via OpenAI aqui
    -- ou no aplicativo antes de chamar essa função.
    -- Por enquanto, retornamos NULL para sinalizar que é necessário
    -- usar busca por keywords no RAG endpoint

    RAISE NOTICE 'Use POST /sumulas/buscar-semantica no endpoint FastAPI para busca semântica completa';

    -- Retorna vazio - será implementado no Python
    RETURN;
END;
$$ LANGUAGE plpgsql STABLE;

-- =====================================================================
-- FUNÇÃO: Busca Híbrida (Keywords + Embeddings)
-- =====================================================================
CREATE OR REPLACE FUNCTION stf.buscar_hibrida(
    p_keywords TEXT[],
    p_similarity_threshold FLOAT DEFAULT 0.5,
    p_limite INT DEFAULT 10
)
RETURNS TABLE(
    numero_identificador VARCHAR,
    tipo VARCHAR,
    setor_afetado VARCHAR,
    match_type VARCHAR,  -- 'KEYWORD' ou 'SEMANTIC'
    score FLOAT
) AS $$
BEGIN
    -- Busca por keywords primeiro
    RETURN QUERY
    SELECT
        s.numero_identificador,
        s.tipo,
        s.setor_afetado,
        'KEYWORD'::VARCHAR as match_type,
        CAST(COUNT(*) AS FLOAT) / ARRAY_LENGTH(p_keywords, 1) as score
    FROM stf.sumulas s
    WHERE s.keywords && p_keywords AND s.status = 'ATIVO'
    GROUP BY s.id, s.numero_identificador, s.tipo, s.setor_afetado
    ORDER BY score DESC
    LIMIT p_limite;
END;
$$ LANGUAGE plpgsql STABLE;

-- =====================================================================
-- VIEW: Estatísticas de Embeddings
-- =====================================================================
CREATE VIEW stf.embedding_stats AS
SELECT
    COUNT(*) as total_sumulas,
    COUNT(CASE WHEN embedding IS NOT NULL THEN 1 END) as com_embedding,
    COUNT(CASE WHEN embedding IS NULL THEN 1 END) as sem_embedding,
    ROUND(
        COUNT(CASE WHEN embedding IS NOT NULL THEN 1 END)::FLOAT / COUNT(*) * 100,
        2
    ) as percentual_com_embedding
FROM stf.sumulas;

-- =====================================================================
-- COMENTÁRIOS
-- =====================================================================
COMMENT ON COLUMN stf.sumulas.embedding IS 'Embedding de 1536 dimensões gerado por text-embedding-3-small (OpenAI)';
COMMENT ON INDEX idx_sumulas_embedding_ivfflat IS 'Índice IVFFLAT para busca semântica eficiente com pgvector';

-- =====================================================================
-- FIM DA EXTENSÃO PGVECTOR
-- =====================================================================

-- =====================================================================
-- FENICE BRAIN — STF Jurisprudência Database Schema
-- PostgreSQL 12+
-- =====================================================================

-- Criar schema
CREATE SCHEMA IF NOT EXISTS stf;

-- =====================================================================
-- TABELA PRINCIPAL: Súmulas Vinculantes + Teses RG
-- =====================================================================
CREATE TABLE IF NOT EXISTS stf.sumulas (
    id SERIAL PRIMARY KEY,

    -- Identificação
    tipo VARCHAR(50) NOT NULL CHECK(tipo IN ('SUMULA_VINCULANTE', 'TEMA_REPERCUSSAO_GERAL')),
    numero_identificador VARCHAR(20) UNIQUE NOT NULL,  -- STF_SV_57, STF_TEMA_69
    numero_numerico INT,                                 -- 57, 69 (para ordenação)
    processo_paradigma VARCHAR(50),                      -- RE 574.706
    data_publicacao DATE,
    status VARCHAR(20) DEFAULT 'ATIVO' CHECK(status IN ('ATIVO', 'REVOGADO', 'MODIFICADO')),

    -- Conteúdo
    enunciado_original TEXT,
    nucleo_da_tese TEXT,

    -- Ancoragem Legal
    artigos_cf88 TEXT[],                                 -- Array de artigos CF/88
    leis_infraconstitucionais TEXT[],                    -- Array de leis

    -- Modulação
    houve_modulacao BOOLEAN DEFAULT FALSE,
    regra_modulacao TEXT,

    -- Impacto Business
    setor_afetado VARCHAR(50),  -- ADMINISTRATIVO, TRIBUTÁRIO, TRABALHISTA, etc.
    potencial_monetario VARCHAR(10) DEFAULT 'LOW' CHECK(potencial_monetario IN ('LOW', 'MEDIUM', 'HIGH')),
    vulnerabilidade_compliance TEXT,

    -- RAG / Busca Semântica
    keywords TEXT[],

    -- Metadata
    analizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    confiabilidade FLOAT DEFAULT 0.8,
    requer_revisao_manual BOOLEAN DEFAULT FALSE,

    -- Índices
    CONSTRAINT valid_numero_numerico CHECK(numero_numerico > 0 OR numero_numerico IS NULL)
);

-- =====================================================================
-- TABELA: Enunciados CJF
-- =====================================================================
CREATE TABLE IF NOT EXISTS stf.enunciados_cjf (
    id SERIAL PRIMARY KEY,

    numero_enunciado INT UNIQUE NOT NULL,
    jornada VARCHAR(100),
    artigo_referencia VARCHAR(50),

    texto TEXT NOT NULL,
    tema VARCHAR(100),

    keywords TEXT[],

    analizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT valid_numero CHECK(numero_enunciado > 0)
);

-- =====================================================================
-- TABELA: Ligações entre Súmulas e Artigos (denormalização)
-- =====================================================================
CREATE TABLE IF NOT EXISTS stf.sumula_artigos_cf (
    id SERIAL PRIMARY KEY,

    sumula_id INT NOT NULL REFERENCES stf.sumulas(id) ON DELETE CASCADE,
    artigo_cf INT NOT NULL,                              -- Art. 9, Art. 37, etc.

    UNIQUE(sumula_id, artigo_cf)
);

-- =====================================================================
-- TABELA: Histórico de Mudanças
-- =====================================================================
CREATE TABLE IF NOT EXISTS stf.sumula_history (
    id SERIAL PRIMARY KEY,

    sumula_id INT NOT NULL REFERENCES stf.sumulas(id) ON DELETE CASCADE,
    status_anterior VARCHAR(20),
    status_novo VARCHAR(20),

    mudanca_descricao TEXT,
    data_mudanca DATE NOT NULL,
    data_registrada TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================================
-- ÍNDICES PARA PERFORMANCE
-- =====================================================================
CREATE INDEX idx_sumulas_tipo ON stf.sumulas(tipo);
CREATE INDEX idx_sumulas_numero ON stf.sumulas(numero_numerico);
CREATE INDEX idx_sumulas_setor ON stf.sumulas(setor_afetado);
CREATE INDEX idx_sumulas_status ON stf.sumulas(status);
CREATE INDEX idx_sumulas_modulacao ON stf.sumulas(houve_modulacao);
CREATE INDEX idx_sumulas_keywords ON stf.sumulas USING GIN(keywords);

CREATE INDEX idx_enunciados_numero ON stf.enunciados_cjf(numero_enunciado);
CREATE INDEX idx_enunciados_jornada ON stf.enunciados_cjf(jornada);

-- =====================================================================
-- VIEWS ÚTEIS
-- =====================================================================

-- View: Súmulas com Modulação (críticas)
CREATE VIEW stf.sumulas_com_modulacao AS
SELECT
    numero_identificador,
    tipo,
    processo_paradigma,
    data_publicacao,
    regra_modulacao,
    setor_afetado,
    potencial_monetario
FROM stf.sumulas
WHERE houve_modulacao = TRUE AND status = 'ATIVO'
ORDER BY data_publicacao DESC;

-- View: Súmulas por Setor
CREATE VIEW stf.sumulas_por_setor AS
SELECT
    setor_afetado,
    COUNT(*) as total,
    COUNT(CASE WHEN houve_modulacao THEN 1 END) as com_modulacao,
    MAX(data_publicacao) as ultima_alteracao
FROM stf.sumulas
WHERE status = 'ATIVO'
GROUP BY setor_afetado
ORDER BY total DESC;

-- View: Súmulas Vinculantes
CREATE VIEW stf.sv_list AS
SELECT
    numero_identificador,
    processo_paradigma,
    data_publicacao,
    setor_afetado,
    houve_modulacao,
    requer_revisao_manual
FROM stf.sumulas
WHERE tipo = 'SUMULA_VINCULANTE' AND status = 'ATIVO'
ORDER BY numero_numerico;

-- View: Temas RG
CREATE VIEW stf.tema_rg_list AS
SELECT
    numero_identificador,
    processo_paradigma,
    data_publicacao,
    setor_afetado,
    houve_modulacao,
    potencial_monetario
FROM stf.sumulas
WHERE tipo = 'TEMA_REPERCUSSAO_GERAL' AND status = 'ATIVO'
ORDER BY numero_numerico;

-- =====================================================================
-- FUNÇÃO: Busca por Palavras-Chave (RAG)
-- =====================================================================
CREATE OR REPLACE FUNCTION stf.buscar_por_keywords(
    p_keywords TEXT[],
    p_limite INT DEFAULT 10
)
RETURNS TABLE(
    numero_identificador VARCHAR,
    tipo VARCHAR,
    similaridade FLOAT,
    setor_afetado VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        s.numero_identificador,
        s.tipo,
        CAST(COUNT(*) AS FLOAT) / ARRAY_LENGTH(p_keywords, 1) as similaridade,
        s.setor_afetado
    FROM stf.sumulas s
    WHERE s.keywords && p_keywords AND s.status = 'ATIVO'
    GROUP BY s.id, s.numero_identificador, s.tipo, s.setor_afetado
    ORDER BY similaridade DESC
    LIMIT p_limite;
END;
$$ LANGUAGE plpgsql STABLE;

-- =====================================================================
-- FUNÇÃO: Alert de Modulação
-- =====================================================================
CREATE OR REPLACE FUNCTION stf.alertar_modulacoes()
RETURNS TABLE(
    numero_identificador VARCHAR,
    setor_afetado VARCHAR,
    regra_modulacao TEXT,
    acao_necessaria VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        s.numero_identificador,
        s.setor_afetado,
        s.regra_modulacao,
        'REVISAR COMPLIANCE IMEDIATAMENTE'::VARCHAR as acao_necessaria
    FROM stf.sumulas s
    WHERE s.houve_modulacao = TRUE
        AND s.status = 'ATIVO'
        AND s.requer_revisao_manual = TRUE
    ORDER BY s.data_publicacao DESC;
END;
$$ LANGUAGE plpgsql STABLE;

-- =====================================================================
-- Comentários
-- =====================================================================
COMMENT ON TABLE stf.sumulas IS 'Súmulas Vinculantes e Temas de Repercussão Geral do STF com análise jurídica completa';
COMMENT ON COLUMN stf.sumulas.numero_identificador IS 'ID único: STF_SV_57 ou STF_TEMA_69';
COMMENT ON COLUMN stf.sumulas.houve_modulacao IS 'TRUE se houve modulação de efeitos (crítico para compliance)';
COMMENT ON COLUMN stf.sumulas.keywords IS 'Array de palavras-chave para busca semântica (RAG)';

-- =====================================================================
-- GRANT (opcional — ajuste conforme necessário)
-- =====================================================================
-- GRANT USAGE ON SCHEMA stf TO seu_usuario;
-- GRANT SELECT ON ALL TABLES IN SCHEMA stf TO seu_usuario;
-- GRANT SELECT ON ALL VIEWS IN SCHEMA stf TO seu_usuario;

-- =====================================================================
-- FIM DO SCHEMA
-- =====================================================================

-- =====================================================================
-- WEBHOOKS Extension — Fenice Brain STF Alertas
-- PostgreSQL 12+
-- =====================================================================

-- =====================================================================
-- TABELA: Webhooks Registrados
-- =====================================================================
CREATE TABLE IF NOT EXISTS stf.webhooks (
    id SERIAL PRIMARY KEY,

    -- Identificação
    nome VARCHAR(100) NOT NULL UNIQUE,
    url VARCHAR(500) NOT NULL,
    tipo VARCHAR(20) NOT NULL CHECK(tipo IN ('DISCORD', 'SLACK', 'EMAIL', 'CUSTOM')),

    -- Eventos
    eventos TEXT[] NOT NULL DEFAULT ARRAY['MODULACAO_DETECTADA', 'SUMULA_NOVA'],
    ativo BOOLEAN DEFAULT TRUE,

    -- Autenticação (se necessária)
    api_key VARCHAR(255),
    headers JSONB,  -- Cabeçalhos customizados

    -- Filtros (opcional)
    filtro_setor VARCHAR(50),  -- Apenas este setor
    filtro_tipo VARCHAR(50),   -- SUMULA_VINCULANTE ou TEMA_REPERCUSSAO_GERAL

    -- Metadata
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ultimo_acionamento TIMESTAMP,
    total_acionamentos INT DEFAULT 0,
    ultimo_status INT,  -- HTTP status code (200, 500, etc)
    ultimo_erro TEXT
);

-- =====================================================================
-- TABELA: Histórico de Alertas Disparados
-- =====================================================================
CREATE TABLE IF NOT EXISTS stf.webhook_history (
    id SERIAL PRIMARY KEY,

    webhook_id INT NOT NULL REFERENCES stf.webhooks(id) ON DELETE CASCADE,
    evento VARCHAR(50) NOT NULL,
    numero_sumula VARCHAR(20),
    payload JSONB NOT NULL,

    -- Resposta do webhook
    http_status INT,
    response_body TEXT,
    sucesso BOOLEAN,
    tempo_ms INT,

    -- Timestamp
    acionado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================================
-- ÍNDICES
-- =====================================================================
CREATE INDEX idx_webhooks_ativo ON stf.webhooks(ativo);
CREATE INDEX idx_webhooks_tipo ON stf.webhooks(tipo);
CREATE INDEX idx_webhook_history_webhook_id ON stf.webhook_history(webhook_id);
CREATE INDEX idx_webhook_history_evento ON stf.webhook_history(evento);
CREATE INDEX idx_webhook_history_sucesso ON stf.webhook_history(sucesso);

-- =====================================================================
-- VIEW: Webhooks Ativos
-- =====================================================================
CREATE VIEW stf.webhooks_ativos AS
SELECT
    id,
    nome,
    url,
    tipo,
    eventos,
    filtro_setor,
    filtro_tipo,
    ultimo_acionamento,
    total_acionamentos,
    ultimo_status
FROM stf.webhooks
WHERE ativo = TRUE;

-- =====================================================================
-- VIEW: Estatísticas de Webhooks
-- =====================================================================
CREATE VIEW stf.webhook_stats AS
SELECT
    w.nome,
    w.tipo,
    COUNT(h.id) as total_acionamentos,
    COUNT(CASE WHEN h.sucesso THEN 1 END) as sucessos,
    COUNT(CASE WHEN NOT h.sucesso THEN 1 END) as falhas,
    ROUND(
        COUNT(CASE WHEN h.sucesso THEN 1 END)::FLOAT / NULLIF(COUNT(h.id), 0) * 100,
        2
    ) as taxa_sucesso,
    AVG(h.tempo_ms) as tempo_medio_ms,
    MAX(h.acionado_em) as ultimo_acionamento
FROM stf.webhooks w
LEFT JOIN stf.webhook_history h ON w.id = h.webhook_id
GROUP BY w.id, w.nome, w.tipo;

-- =====================================================================
-- FUNÇÃO: Disparar Webhook quando Modulação Detectada
-- =====================================================================
CREATE OR REPLACE FUNCTION stf.disparar_alerta_modulacao()
RETURNS TRIGGER AS $$
DECLARE
    v_webhook RECORD;
    v_payload JSONB;
BEGIN
    -- Apenas se modulação foi adicionada/modificada
    IF (NEW.houve_modulacao != OLD.houve_modulacao AND NEW.houve_modulacao = TRUE) THEN
        -- Montar payload
        v_payload := jsonb_build_object(
            'evento', 'MODULACAO_DETECTADA',
            'numero_identificador', NEW.numero_identificador,
            'tipo', NEW.tipo,
            'setor_afetado', NEW.setor_afetado,
            'regra_modulacao', NEW.regra_modulacao,
            'potencial_monetario', NEW.potencial_monetario,
            'vulnerabilidade_compliance', NEW.vulnerabilidade_compliance,
            'data_detectada', NOW()::TEXT
        );

        -- Disparar para todos os webhooks ativos que têm 'MODULACAO_DETECTADA' no eventos
        FOR v_webhook IN
            SELECT * FROM stf.webhooks
            WHERE ativo = TRUE
                AND 'MODULACAO_DETECTADA' = ANY(eventos)
                AND (filtro_setor IS NULL OR filtro_setor = NEW.setor_afetado)
                AND (filtro_tipo IS NULL OR filtro_tipo = NEW.tipo)
        LOOP
            -- Registrar que vai disparar (será executado por worker async)
            INSERT INTO stf.webhook_history (webhook_id, evento, numero_sumula, payload, sucesso)
            VALUES (v_webhook.id, 'MODULACAO_DETECTADA', NEW.numero_identificador, v_payload, NULL);
        END LOOP;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para disparar alertas
DROP TRIGGER IF EXISTS trg_alerta_modulacao ON stf.sumulas;
CREATE TRIGGER trg_alerta_modulacao
AFTER UPDATE ON stf.sumulas
FOR EACH ROW
EXECUTE FUNCTION stf.disparar_alerta_modulacao();

-- =====================================================================
-- FUNÇÃO: Listar Webhooks com Estatísticas
-- =====================================================================
CREATE OR REPLACE FUNCTION stf.listar_webhooks_com_stats()
RETURNS TABLE(
    webhook_id INT,
    nome VARCHAR,
    tipo VARCHAR,
    url VARCHAR,
    ativo BOOLEAN,
    total_acionamentos INT,
    taxa_sucesso FLOAT,
    ultimo_acionamento TIMESTAMP,
    ultimo_status INT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        w.id,
        w.nome,
        w.tipo,
        w.url,
        w.ativo,
        COALESCE(COUNT(h.id), 0)::INT as total_acionamentos,
        COALESCE(
            COUNT(CASE WHEN h.sucesso THEN 1 END)::FLOAT / NULLIF(COUNT(h.id), 0) * 100,
            0
        ) as taxa_sucesso,
        MAX(h.acionado_em) as ultimo_acionamento,
        w.ultimo_status
    FROM stf.webhooks w
    LEFT JOIN stf.webhook_history h ON w.id = h.webhook_id
    GROUP BY w.id, w.nome, w.tipo, w.url, w.ativo, w.ultimo_status
    ORDER BY w.criado_em DESC;
END;
$$ LANGUAGE plpgsql;

-- =====================================================================
-- COMENTÁRIOS
-- =====================================================================
COMMENT ON TABLE stf.webhooks IS 'Webhooks registrados para alertas de modulação e novas súmulas';
COMMENT ON COLUMN stf.webhooks.eventos IS 'Array de eventos que disparam o webhook: MODULACAO_DETECTADA, SUMULA_NOVA';
COMMENT ON COLUMN stf.webhooks.filtro_setor IS 'Se não NULL, webhook só dispara para este setor (ADMINISTRATIVO, TRIBUTÁRIO, etc)';
COMMENT ON TABLE stf.webhook_history IS 'Histórico de todos os alertas disparados, sucesso ou falha';

-- =====================================================================
-- FIM DA EXTENSÃO WEBHOOKS
-- =====================================================================

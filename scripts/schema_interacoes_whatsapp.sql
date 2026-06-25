-- =====================================================================
-- Tabela de log de interações WhatsApp via AvisaAPI + N8N
-- Aplicar no Supabase SQL Editor
-- =====================================================================

CREATE TABLE IF NOT EXISTS public.interacoes_whatsapp (
    id              BIGSERIAL PRIMARY KEY,

    -- Quem enviou
    numero_remetente TEXT NOT NULL,           -- ex: 5521976531414
    nome_remetente   TEXT,
    email_remetente  TEXT,

    -- Conversa
    session_id       TEXT,                   -- identificador de sessão AvisaAPI (se disponível)
    message_id       TEXT,                   -- ID da mensagem recebida

    -- Conteúdo
    mensagem_cliente TEXT NOT NULL,          -- texto enviado pelo cliente
    resposta_ai      TEXT,                   -- resposta gerada pelo Groq
    modelo_ai        TEXT DEFAULT 'llama-3.3-70b-versatile',

    -- Metadados
    provider         TEXT DEFAULT 'avisa',
    canal            TEXT DEFAULT 'whatsapp',
    entregue         BOOLEAN DEFAULT NULL,   -- NULL = não tentado, TRUE = ok, FALSE = falhou
    http_status_avisa INT,                   -- status HTTP da chamada de envio

    created_at       TIMESTAMPTZ DEFAULT NOW()
);

-- Índices
CREATE INDEX IF NOT EXISTS idx_wapp_numero      ON public.interacoes_whatsapp (numero_remetente);
CREATE INDEX IF NOT EXISTS idx_wapp_session     ON public.interacoes_whatsapp (session_id);
CREATE INDEX IF NOT EXISTS idx_wapp_created_at  ON public.interacoes_whatsapp (created_at DESC);
CREATE INDEX IF NOT EXISTS idx_wapp_entregue    ON public.interacoes_whatsapp (entregue);

-- Comentários
COMMENT ON TABLE public.interacoes_whatsapp IS 'Log de todas as interações WhatsApp recebidas via AvisaAPI e processadas pelo N8N + Groq';
COMMENT ON COLUMN public.interacoes_whatsapp.numero_remetente IS 'Número em formato E.164 sem + (ex: 5521976531414)';
COMMENT ON COLUMN public.interacoes_whatsapp.entregue IS 'NULL=não tentado, TRUE=resposta enviada, FALSE=falha no envio';

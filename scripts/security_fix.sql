-- ============================================================
-- Fenice bRain — Security Hardening
-- Execute no SQL Editor do Supabase: qcfdssnpjzvjbvemhrik
-- ============================================================

-- ============================================================
-- 1. CORRIGIR SECURITY DEFINER → SECURITY INVOKER nas 3 views
--    (CVE crítico: views com DEFINER executam como superuser,
--     ignorando RLS e expondo todos os dados para qualquer usuário)
-- ============================================================

ALTER VIEW public.v_vizinhos_grafo     SET (security_invoker = true);
ALTER VIEW public.v_linha_do_tempo     SET (security_invoker = true);
ALTER VIEW public.v_revogacoes_recentes SET (security_invoker = true);

-- Garantir que a nova view também seja INVOKER
ALTER VIEW public.v_rag_status         SET (security_invoker = true);

-- ============================================================
-- 2. HABILITAR RLS em TODAS as tabelas do projeto
--    (sem RLS = qualquer anon lê/escreve tudo via REST API)
-- ============================================================

-- Tabelas existentes
ALTER TABLE IF EXISTS public.legislacao_brasileira    ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.artigos                  ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.grafo_nos                ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.grafo_arestas            ENABLE ROW LEVEL SECURITY;

-- Tabelas novas do RAG semântico
ALTER TABLE IF EXISTS public.documentos_juridicos     ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.documentos_chunks        ENABLE ROW LEVEL SECURITY;

-- Outras tabelas que possam existir
ALTER TABLE IF EXISTS public.leads                    ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.grafo_temporal           ENABLE ROW LEVEL SECURITY;

-- ============================================================
-- 3. REVOGAR acesso anônimo direto a tabelas sensíveis
--    (a API usa service_role que bypassa RLS — isso não quebra nada)
-- ============================================================

REVOKE ALL ON public.documentos_juridicos  FROM anon;
REVOKE ALL ON public.documentos_chunks     FROM anon;
REVOKE ALL ON public.grafo_nos             FROM anon;
REVOKE ALL ON public.grafo_arestas         FROM anon;
REVOKE ALL ON public.legislacao_brasileira FROM anon;
REVOKE ALL ON public.artigos               FROM anon;

-- ============================================================
-- 4. POLÍTICAS RLS — bloqueio total para anon e authenticated
--    A API (service_role key) bypassa RLS por design do Supabase
--    Nenhuma chamada direta à tabela funciona sem a service_role
-- ============================================================

-- documentos_juridicos: somente service_role (backend)
DROP POLICY IF EXISTS "block_anon_juridicos"  ON public.documentos_juridicos;
DROP POLICY IF EXISTS "block_auth_juridicos"  ON public.documentos_juridicos;
CREATE POLICY "somente_service_role" ON public.documentos_juridicos
  AS RESTRICTIVE FOR ALL
  TO anon, authenticated
  USING (false);

-- documentos_chunks: somente service_role (backend)
DROP POLICY IF EXISTS "block_anon_chunks"     ON public.documentos_chunks;
DROP POLICY IF EXISTS "block_auth_chunks"     ON public.documentos_chunks;
CREATE POLICY "somente_service_role" ON public.documentos_chunks
  AS RESTRICTIVE FOR ALL
  TO anon, authenticated
  USING (false);

-- legislacao_brasileira: leitura permitida (Free tier da API usa ela)
DROP POLICY IF EXISTS "leitura_publica_legislacao" ON public.legislacao_brasileira;
CREATE POLICY "leitura_publica_legislacao" ON public.legislacao_brasileira
  AS PERMISSIVE FOR SELECT
  TO anon, authenticated
  USING (true);

-- Escrita somente service_role
DROP POLICY IF EXISTS "escrita_somente_service" ON public.legislacao_brasileira;
CREATE POLICY "escrita_somente_service" ON public.legislacao_brasileira
  AS RESTRICTIVE FOR INSERT
  TO anon, authenticated
  USING (false);

-- artigos: leitura pública (usado no /artigo e /lei_info)
DROP POLICY IF EXISTS "leitura_publica_artigos" ON public.artigos;
CREATE POLICY "leitura_publica_artigos" ON public.artigos
  AS PERMISSIVE FOR SELECT
  TO anon, authenticated
  USING (true);

-- grafo_nos e grafo_arestas: leitura pública (usado no /grafo)
DROP POLICY IF EXISTS "leitura_publica_nos"     ON public.grafo_nos;
DROP POLICY IF EXISTS "leitura_publica_arestas" ON public.grafo_arestas;
CREATE POLICY "leitura_publica_nos"     ON public.grafo_nos
  AS PERMISSIVE FOR SELECT TO anon, authenticated USING (true);
CREATE POLICY "leitura_publica_arestas" ON public.grafo_arestas
  AS PERMISSIVE FOR SELECT TO anon, authenticated USING (true);

-- ============================================================
-- 5. PROTEGER RPCs sensíveis — revogar execução de anon
-- ============================================================

REVOKE EXECUTE ON FUNCTION public.match_chunks FROM anon;
REVOKE EXECUTE ON FUNCTION public.set_updated_at FROM anon;

-- buscar_legislacao é usada pelo Free tier — manter
-- (se quiser bloquear também: REVOKE EXECUTE ON FUNCTION public.buscar_legislacao FROM anon)

-- ============================================================
-- 6. VERIFICAÇÃO — rode após aplicar o script
-- ============================================================

-- Confirmar que as views estão com security_invoker:
SELECT schemaname, viewname,
       pg_get_viewdef(viewname::text, true) as def
FROM pg_views
WHERE schemaname = 'public'
  AND viewname IN ('v_vizinhos_grafo','v_linha_do_tempo',
                   'v_revogacoes_recentes','v_rag_status');

-- Confirmar RLS ativado:
SELECT tablename, rowsecurity
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY tablename;

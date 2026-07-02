-- ══════════════════════════════════════════════════════════════════════
-- POLÍTICA DE ACESSO FENICE — LOCKDOWN default-deny (aplicado 2026-07-02)
-- Só service_role (backend) acessa dados. anon/authenticated sem leitura.
-- Registro versionado das migrations aplicadas via MCP Supabase.
-- Ver docs/superpowers/reports/2026-07-02-politica-acesso-supabase.md
-- ══════════════════════════════════════════════════════════════════════

-- ── migration: politica_acesso_lockdown_default_deny ──────────────────

alter table public.apoiadores_observatorio enable row level security;
alter table public.fenice_access_logs      enable row level security;

drop policy if exists apoiadores_insert_publico on public.apoiadores_observatorio;
create policy apoiadores_insert_publico on public.apoiadores_observatorio
  for insert to anon, authenticated with check (true);

drop policy if exists leitura_publica_artigos   on public.artigos;
drop policy if exists leitura_publica_arestas    on public.grafo_arestas;
drop policy if exists leitura_publica            on public.grafo_arestas;
drop policy if exists leitura_publica_nos        on public.grafo_nos;
drop policy if exists leitura_publica            on public.grafo_nos;
drop policy if exists leitura_publica_legislacao on public.legislacao_brasileira;
drop policy if exists leitura_publica            on public.legislacao_brasileira;
drop policy if exists leitura_publica            on public.legislacao_historico;

alter view public.vw_wow_atendimentos_dia set (security_invoker = on);
alter view public.vw_wow_funil_area       set (security_invoker = on);
alter view public.vw_wow_acoes_dia        set (security_invoker = on);
alter view public.vw_sfs_observatorio     set (security_invoker = on);
revoke all on public.vw_wow_atendimentos_dia, public.vw_wow_funil_area,
              public.vw_wow_acoes_dia, public.vw_sfs_observatorio
  from anon, authenticated;

revoke execute on function public.rls_auto_enable() from anon, authenticated, public;

-- ── migration: hardening_function_search_path ─────────────────────────

alter function public.set_updated_at() set search_path = public, pg_temp;
alter function public.update_fenice_leads_atualizado_em() set search_path = public, pg_temp;
alter function public.match_chunks(query_embedding vector, match_threshold double precision, match_count integer)
  set search_path = public, pg_temp;

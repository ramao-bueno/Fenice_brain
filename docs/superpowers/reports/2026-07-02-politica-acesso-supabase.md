# Política de Controle de Acesso — Banco Fenice (Supabase)

**Data:** 2026-07-02 · **Projeto:** `qcfdssnpjzvjbvemhrik` · **Autor:** Ramão + Claude

> "Ninguém é forte — mas temos que desenvolver políticas de controle dos nossos projetos e implementá-las."

## Princípio — DEFAULT-DENY

**Só o backend (`service_role`) acessa dados.** `anon` e `authenticated` (devs
cadastrados) **não têm leitura** de nenhuma tabela. Todo acesso externo passa
**sempre pela API server-side** (FastAPI / N8N), que usa a `service_role` key —
a qual **ignora RLS** por design. Logo, ligar RLS **não quebra** os fluxos internos.

Regra mental: *se a porta pode ser aberta com a anon key, ela está aberta para o mundo.*

## Regras (padrão para toda tabela nova)

1. **RLS sempre ligada** em toda tabela do schema `public` (exposto ao PostgREST).
2. **Sem policy de leitura** para anon/authenticated → o padrão é negar. Não criar
   `leitura_publica` "por conveniência".
3. **Escrita/leitura server-side** = `service_role` (bypassa RLS; não precisa policy).
4. **Exceção controlada — formulários públicos:** policy **só de INSERT** para anon
   (write-only). Nunca SELECT. Ex.: `apoiadores_observatorio` (cadastro do Observatório).
5. **Views** que tocam dados sensíveis: `security_invoker = on` + `revoke` de anon/auth.
   Nunca deixar view `SECURITY DEFINER` acessível a anon (vaza a tabela por baixo da RLS).
6. **Funções `SECURITY DEFINER`:** `revoke execute` de anon/authenticated se não forem
   deliberadamente públicas. `search_path` sempre fixado (`set search_path = public, pg_temp`).
7. **Segredos nunca no git.** `service_role` key só em `.env` / no backend.

## O que foi implementado em 2026-07-02

- RLS ligada em `apoiadores_observatorio` e `fenice_access_logs` (estavam abertas).
- Derrubadas TODAS as leituras públicas: `artigos`, `legislacao_brasileira`,
  `legislacao_historico`, `grafo_nos`, `grafo_arestas`.
- Form do Observatório: policy write-only (INSERT anon/auth), sem leitura.
- 4 views de BI (`vw_wow_*`, `vw_sfs_observatorio`): `security_invoker=on` + revoke anon/auth.
- `rls_auto_enable()`: revoke execute de anon/authenticated/public.
- `search_path` fixado em `set_updated_at`, `update_fenice_leads_atualizado_em`, `match_chunks`.

Resultado do advisor: **17/17 tabelas com RLS**, 0 abertas; todos os ERROS de segurança
zerados. Restam INFO ("RLS sem policy" = estado desejado) e WARNs aceitos (form público;
extensões `unaccent`/`vector` no public — mover quebraria o RAG).

## ⚠️ A verificar (impacto possível no cliente)

O lockdown fecha leitura anon/authenticated. Se **algum consumo for client-side** (JS do
site lendo Supabase direto com anon key), ele passa a voltar vazio. **Confirmar que:**
- A API pública `/buscar` lê via **FastAPI (service_role)**, não via anon no navegador.
- O site do Observatório **insere** o cadastro (funciona) e **não lê** a lista no cliente.

Se algo quebrar, o conserto é apontar o consumo para o backend server-role — **não**
reabrir leitura pública.

## SQL aplicado
Registro versionado em `scripts/db_security/2026-07-02-lockdown.sql`.

*بِسْمِ اللهِ الرَّحْمَنِ الرَّحِيمِ · Fenice IT · Justech.IA*

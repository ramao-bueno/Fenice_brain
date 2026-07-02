-- Captura de diálogos do atendimento WOW (Téo) para o loop de aprendizado.
-- PII: acesso só via service key (server-side). Aplicada em 2026-07-02.
create table if not exists public.fenice_tim_dialogos (
  id bigint generated always as identity primary key,
  numero text not null,
  ts timestamptz not null default now(),
  direcao text not null check (direcao in ('in','out')),
  mensagem text,
  area text,
  estagio text,
  acao text,
  intencao text
);
create index if not exists idx_dialogos_numero_ts on public.fenice_tim_dialogos (numero, ts);
alter table public.fenice_tim_dialogos enable row level security;

-- Camada de reporting (Power BI) sobre os diálogos WOW. Aplicada em 2026-07-02.
-- Princípio: tabelas cruas enxutas; VIEWS = a lente do BI (contrato estável).
-- O Power BI conecta nas vw_*, nunca na tabela crua.

alter table public.fenice_tim_dialogos add column if not exists canal text not null default 'whatsapp';

-- Volume/time-series: mensagens e contatos por dia × área × canal
create or replace view public.vw_wow_atendimentos_dia as
select
  date_trunc('day', ts)::date          as dia,
  coalesce(area, '(sem_area)')         as area,
  coalesce(canal, 'whatsapp')          as canal,
  count(*) filter (where direcao='in')  as msgs_recebidas,
  count(*) filter (where direcao='out') as msgs_enviadas,
  count(distinct numero)               as contatos_distintos
from public.fenice_tim_dialogos
group by 1, 2, 3;

-- Funil: contatos e interações por estágio × área
create or replace view public.vw_wow_funil_area as
select
  coalesce(area, '(sem_area)')       as area,
  coalesce(estagio, '(sem_estagio)') as estagio,
  count(distinct numero)             as contatos,
  count(*)                           as interacoes
from public.fenice_tim_dialogos
group by 1, 2;

-- Mix de ações por dia (handoff, descoberta, menu, responder…) — sobre mensagens recebidas
create or replace view public.vw_wow_acoes_dia as
select
  date_trunc('day', ts)::date    as dia,
  coalesce(area, '(sem_area)')   as area,
  coalesce(acao, '(sem_acao)')   as acao,
  count(*)                       as qtd
from public.fenice_tim_dialogos
where direcao = 'in'
group by 1, 2, 3;

-- Unidade SFS (Observatório de São Francisco do Sul) — dashboard próprio
create or replace view public.vw_sfs_observatorio as
select
  date_trunc('day', ts)::date          as dia,
  coalesce(estagio, '(sem_estagio)')   as estagio,
  coalesce(acao, '(sem_acao)')         as acao,
  count(*) filter (where direcao='in')  as msgs_recebidas,
  count(*) filter (where direcao='out') as msgs_enviadas,
  count(distinct numero)               as contatos
from public.fenice_tim_dialogos
where area = 'observatorio'
group by 1, 2, 3;

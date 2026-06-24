-- ============================================================
-- Fenice RAG Semântico — Schema Supabase
-- Execute no SQL Editor do Supabase (projeto qcfdssnpjzvjbvemhrik)
-- ============================================================

-- 1. Habilitar extensão pgvector (uma vez por projeto)
create extension if not exists vector;

-- ============================================================
-- 2. Tabela de documentos jurídicos (fonte)
-- ============================================================
create table if not exists documentos_juridicos (
  id          bigserial primary key,
  codigo      text not null,        -- "CF", "CC", "CPC", "CP", "CLT", "CDC"
  artigo      text not null,        -- "Art. 1", "Art. 121"
  titulo      text,                 -- nome do artigo quando disponível
  conteudo    text not null,        -- texto completo do artigo (corpo da nota)
  fonte       text not null,        -- "vault" | "planalto"
  vigente     boolean default true, -- false = revogado (planalto_temporal.py)
  data_ref    date,                 -- data da última verificação de vigência
  created_at  timestamptz default now(),
  updated_at  timestamptz default now(),

  -- garante upsert idempotente: mesma fonte não duplica o mesmo artigo
  unique(codigo, artigo, fonte)
);

-- Trigger para atualizar updated_at automaticamente
create or replace function set_updated_at()
returns trigger language plpgsql as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

create trigger trg_documentos_juridicos_updated_at
  before update on documentos_juridicos
  for each row execute function set_updated_at();

-- ============================================================
-- 3. Tabela de chunks vetorizados
-- ============================================================
create table if not exists documentos_chunks (
  id           bigserial primary key,
  documento_id bigint not null references documentos_juridicos(id) on delete cascade,
  chunk_index  int not null default 0,   -- sempre 0 (1 artigo = 1 chunk)
  conteudo     text not null,            -- texto limpo enviado ao embedding
  embedding    vector(1024),             -- multilingual-e5-large = 1024 dims
  created_at   timestamptz default now()
);

-- ============================================================
-- 4. Índice HNSW (melhor que IVFFlat para inserts incrementais)
--    Suporta atualização em tempo real sem rebuild de clusters
-- ============================================================
create index if not exists idx_chunks_hnsw
  on documentos_chunks
  using hnsw (embedding vector_cosine_ops);

-- ============================================================
-- 5. RPC match_chunks — busca por similaridade cosseno
-- ============================================================
create or replace function match_chunks(
  query_embedding  vector(1024),
  match_threshold  float,
  match_count      int
)
returns table (
  id           bigint,
  documento_id bigint,
  conteudo     text,
  codigo       text,
  artigo       text,
  vigente      boolean,
  similarity   float
)
language sql stable
as $$
  select
    dc.id,
    dc.documento_id,
    dc.conteudo,
    dj.codigo,
    dj.artigo,
    dj.vigente,
    1 - (dc.embedding <=> query_embedding) as similarity
  from documentos_chunks dc
  join documentos_juridicos dj on dj.id = dc.documento_id
  where 1 - (dc.embedding <=> query_embedding) > match_threshold
    and dj.vigente = true                    -- filtra revogados por padrão
  order by dc.embedding <=> query_embedding  -- menor distância = maior similaridade
  limit match_count;
$$;

-- ============================================================
-- 6. View auxiliar para monitoramento da ingestão
-- ============================================================
create or replace view v_rag_status as
select
  dj.codigo,
  dj.fonte,
  count(*)                                       as total_artigos,
  count(dc.id)                                   as total_chunks,
  count(*) filter (where dj.vigente = true)      as vigentes,
  count(*) filter (where dj.vigente = false)     as revogados,
  max(dj.updated_at)                             as ultima_atualizacao
from documentos_juridicos dj
left join documentos_chunks dc on dc.documento_id = dj.id
group by dj.codigo, dj.fonte
order by dj.codigo, dj.fonte;

-- ============================================================
-- Como usar:
--   SELECT * FROM v_rag_status;
--   SELECT * FROM match_chunks('[0.1, 0.2, ...]'::vector, 0.70, 5);
-- ============================================================

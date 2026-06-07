# Embeddings + RAG — Fenice Brain STF

## 🎯 Visão Geral

Sistema de Busca Semântica com Embeddings OpenAI + pgvector + FastAPI. Converte súmulas em vetores (embeddings) para busca por similaridade, não por palavras-chave.

**Benefícios:**
- ✅ Busca por conceito, não por palavra
- ✅ "direito de greve" encontra "direito de paralisação dos servidores"
- ✅ Embeddings cached no PostgreSQL (sem chamadas repetidas)
- ✅ Busca híbrida (semântica + keywords)

---

## 📦 Instalação

### 1️⃣ Instalar Dependências

```bash
pip install openai psycopg2-binary fastapi uvicorn
```

### 2️⃣ Ativar pgvector no PostgreSQL

Pgvector permite armazenar vetores no PostgreSQL:

**Windows (com WSL2 ou VM Linux):**
```bash
# Via apt (Linux)
sudo apt install postgresql-15-pgvector

# Ou via pip
pip install pgvector
```

**Alternativa: Docker (Recomendado)**
```bash
docker run -d \
  --name postgres-pgvector \
  -e POSTGRES_DB=fenice_brain \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  pgvector/pgvector:pg15-latest
```

### 3️⃣ Configurar OpenAI API Key

```bash
# Via variável de ambiente
export OPENAI_API_KEY="sk-proj-..."

# Ou via .env
echo "OPENAI_API_KEY=sk-proj-..." > .env
```

---

## 🔧 Setup

### Passo 1: Ativar pgvector no Banco

```bash
psql -U postgres -d fenice_brain -f schema_pgvector_extension.sql
```

Isso cria:
- Extensão `vector`
- Coluna `embedding` (vector(1536)) na tabela `stf.sumulas`
- Índices IVFFLAT para busca eficiente
- View `stf.embedding_stats` para monitoramento

### Passo 2: Gerar Embeddings

```bash
# Primeira execução (gera embeddings para todas as súmulas)
python embeddings_openai_generator.py

# Opções
python embeddings_openai_generator.py \
  --api-key sk-proj-... \
  --host localhost \
  --database fenice_brain \
  --user postgres \
  --batch-size 10 \
  --delay 0.5 \
  --force  # Regenerar todos
```

**Output esperado:**
```
🚀 Gerador de Embeddings — Fenice Brain STF
=============================================

✅ Conectado a fenice_brain@localhost
✅ Extensão pgvector criada/ativada
✅ Coluna embedding adicionada
✅ Índice IVFFLAT criado

📊 Processando 10 súmulas...
✅ [1/10] (10%) STF_SV_57 — Embedding salvo
✅ [2/10] (20%) STF_TEMA_69 — Embedding salvo
...
✅ [10/10] (100%) STF_TEMA_220 — Embedding salvo

📈 Resultado:
  ✅ Processadas: 10
  ❌ Erros: 0
  📊 Taxa de sucesso: 100%

📊 Total com embedding: 10
```

---

## 🚀 Usando RAG Retriever (Standalone)

### Exemplo em Python

```python
from embeddings_rag_retriever import RAGRetriever

# Inicializar
retriever = RAGRetriever(
    openai_api_key="sk-proj-...",
    db_host="localhost"
)

# Conectar
if not retriever.conectar():
    exit(1)

# 1. Busca Semântica
query = "direito de greve dos servidores públicos"
resultados = retriever.buscar_semanticamente(query, limite=5)

for r in resultados:
    print(f"{r.numero_identificador}: {r.similarity_score:.2%}")
    print(f"  Setor: {r.setor_afetado}")

# 2. Busca Híbrida
resultados = retriever.buscar_hibrida(
    "greve servidores",
    keywords=["administrativo", "direito-publico"],
    limite=5,
    alpha=0.5  # 50% semântica, 50% keywords
)

# 3. Gerar Contexto para RAG (uso em LLM)
contexto = retriever.gerar_contexto_rag(
    query="direito de greve",
    num_referencias=3
)
print(contexto)  # Pronto para usar em prompt de LLM

# Estatísticas
stats = retriever.contar_embeddings()
print(f"Total com embedding: {stats['com_embedding']} / {stats['total_sumulas']}")

retriever.fechar()
```

---

## 📚 Endpoints FastAPI

### 1️⃣ Busca Semântica

```bash
curl -X POST "http://localhost:8000/sumulas/buscar-semantica" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "direito de greve dos servidores públicos",
    "limite": 5,
    "threshold": 0.5
  }?api_key=sua_chave'
```

**Resposta:**
```json
[
  {
    "numero_identificador": "STF_SV_57",
    "tipo": "SUMULA_VINCULANTE",
    "setor_afetado": "ADMINISTRATIVO",
    "similarity_score": 0.89,
    "enunciado_original": "O direito de greve dos servidores públicos...",
    "match_type": "SEMANTIC"
  },
  {
    "numero_identificador": "STF_TEMA_69",
    "tipo": "TEMA_REPERCUSSAO_GERAL",
    "setor_afetado": "ADMINISTRATIVO",
    "similarity_score": 0.82,
    "enunciado_original": "...",
    "match_type": "SEMANTIC"
  }
]
```

### 2️⃣ Busca Híbrida (Semântica + Keywords)

```bash
curl -X POST "http://localhost:8000/sumulas/buscar-hibrida" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "direito de greve",
    "limite": 5,
    "threshold": 0.4
  }' \
  -G \
  -d "keywords=administrativo&keywords=direito-publico&alpha=0.5&api_key=sua_chave"
```

**Parâmetros:**
- `query`: Texto para busca semântica
- `limite`: Número máximo de resultados (1-50)
- `threshold`: Limite mínimo de similaridade (0-1)
- `keywords`: (opcional) Palavras-chave adicionais (query param repetido)
- `alpha`: Peso da semântica (1.0=100% semântica, 0.0=100% keywords)

### 3️⃣ Estatísticas de Embeddings

```bash
curl "http://localhost:8000/embeddings/stats?api_key=sua_chave"
```

**Resposta:**
```json
{
  "total_sumulas": 10,
  "com_embedding": 10,
  "sem_embedding": 0,
  "percentual_com_embedding": 100.0
}
```

---

## 🧠 Como Funciona

### 1. Geração de Embeddings

```
Súmula (texto) 
  → OpenAI text-embedding-3-small 
    → Vector (1536 dimensões) 
      → PostgreSQL (pgvector)
```

**Exemplo:**
```
"O direito de greve dos servidores públicos..." 
  → [0.123, -0.456, 0.789, ..., 0.234] (1536 números)
```

### 2. Busca Semântica

```
Query: "direito de paralisação" 
  → Embedding via OpenAI 
    → Busca no PostgreSQL com similaridade cosine 
      → Ordena por proximidade
```

### 3. Índices IVFFLAT

Para 10 súmulas com embeddings:
- **IVFFLAT** (100 listas): Rápido, baixa memória ✅
- **HNSW**: Mais preciso, mais memória (descomente em schema_pgvector_extension.sql)

---

## 📊 Queries SQL Úteis

### Ver Embeddings

```sql
-- Contar súmulas com embedding
SELECT * FROM stf.embedding_stats;

-- Ver primeira 10 dimensões do embedding de uma súmula
SELECT numero_identificador, embedding::text FROM stf.sumulas 
WHERE embedding IS NOT NULL LIMIT 1;
```

### Busca Direta em SQL

```sql
-- Busca semântica em SQL puro
-- (mas requer gerar embedding da query via Python)
SELECT 
  numero_identificador,
  (1 - (embedding <-> 'seu_embedding_aqui'::vector)) as similarity
FROM stf.sumulas
WHERE embedding IS NOT NULL AND status = 'ATIVO'
ORDER BY embedding <-> 'seu_embedding_aqui'::vector
LIMIT 5;
```

### Análise de Similaridade

```sql
-- Encontrar súmulas mais similares a STF_SV_57
SELECT 
  s2.numero_identificador,
  (1 - (s1.embedding <-> s2.embedding)) as similarity
FROM stf.sumulas s1
JOIN stf.sumulas s2 ON 1=1
WHERE s1.numero_identificador = 'STF_SV_57'
  AND s2.id != s1.id
  AND s1.embedding IS NOT NULL
  AND s2.embedding IS NOT NULL
ORDER BY s1.embedding <-> s2.embedding
LIMIT 10;
```

---

## 💰 Custos OpenAI

**text-embedding-3-small:**
- $0.02 / 1M tokens
- Embedding de 1 súmula (~200 tokens) = $0.000004
- 10 súmulas = $0.00004
- 1.000 súmulas = $0.004

**Otimizações:**
- Embeddings cached no PostgreSQL (sem re-cálculos)
- Use `--delay` para rate limiting
- Batch processing automático

---

## 🔗 Integração com LLM

### Usar Contexto RAG em Claude

```python
from embeddings_rag_retriever import RAGRetriever

retriever = RAGRetriever()
retriever.conectar()

# Gerar contexto
contexto = retriever.gerar_contexto_rag(
    query="direito de greve",
    num_referencias=3
)

# Usar em prompt
from anthropic import Anthropic

client = Anthropic()
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": f"""Baseado neste contexto jurídico:

{contexto}

Responda: {query}"""
    }]
)

print(response.content[0].text)
retriever.fechar()
```

---

## 🚨 Troubleshooting

### "pgvector not found"
```bash
# Instalar pgvector
sudo apt install postgresql-15-pgvector

# Ou verificar instalação
psql -U postgres -d fenice_brain -c "CREATE EXTENSION vector;" 
```

### "embedding IS NULL"
```bash
# Gerar embeddings
python embeddings_openai_generator.py

# Verificar
psql -U postgres -d fenice_brain -c "SELECT COUNT(*) FROM stf.sumulas WHERE embedding IS NOT NULL;"
```

### "OpenAI rate limit exceeded"
```bash
# Aumentar delay entre requisições
python embeddings_openai_generator.py --delay 2.0  # 2 segundos
```

### "OPENAI_API_KEY not set"
```bash
# Verificar
echo $OPENAI_API_KEY

# Setar
export OPENAI_API_KEY="sk-proj-..."

# Ou criar .env
echo "OPENAI_API_KEY=sk-proj-..." >> .env
python -c "from dotenv import load_dotenv; load_dotenv()"
```

---

## 📈 Performance

### Índices

```bash
# Verificar índice criado
psql -U postgres -d fenice_brain -c "\d stf.sumulas"

# Analisar query
EXPLAIN ANALYZE
SELECT * FROM stf.sumulas 
WHERE embedding IS NOT NULL 
ORDER BY embedding <-> '[..1536 dimensões...]'::vector
LIMIT 5;
```

### Benchmark (10 súmulas)

| Operação | Tempo |
|----------|-------|
| Busca semântica | ~50ms |
| Busca por keywords | ~10ms |
| Geração de embedding | ~100ms |

---

## 🔐 Segurança

- ✅ API Key obrigatória
- ✅ Embeddings never logged
- ✅ HTTPS em produção
- ⚠️ Rotacionar OpenAI API Keys regularmente

---

## 📚 Próximas Melhorias

1. **Fine-tuning de Embeddings** — Treinar modelo com domínio jurídico
2. **Caching de Queries** — Redis para queries populares
3. **Embeddings Multilíngues** — Suportar português + inglês
4. **Integração com GPT-4** — Análise jurídica automática
5. **Webhooks** — Alertar quando nova súmula similar publicada

---

## 📖 Referências

- [OpenAI Embeddings API](https://platform.openai.com/docs/guides/embeddings)
- [pgvector Documentation](https://github.com/pgvector/pgvector)
- [FastAPI](https://fastapi.tiangolo.com/)
- [PostgreSQL Vector Index](https://www.postgresql.org/docs/current/indexes-types.html)


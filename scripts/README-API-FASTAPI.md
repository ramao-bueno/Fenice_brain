# API FastAPI — Fenice Brain STF Jurisprudência

## 🚀 Iniciar a API

### Prerequisitos
```bash
pip install fastapi uvicorn psycopg2-binary python-dotenv
```

### Rodar Localmente
```bash
python api_stf_fastapi.py

# Ou via uvicorn
uvicorn api_stf_fastapi:app --reload --host 0.0.0.0 --port 8000
```

### Acessar Documentação
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI JSON:** http://localhost:8000/openapi.json

---

## 🔐 Autenticação

Todas as requisições precisam de `api_key`:

```bash
# Via query parameter
curl "http://localhost:8000/sumulas?api_key=sua_chave_secreta_aqui"

# Via variável de ambiente
export API_KEY="sua_chave_secreta_aqui"
```

---

## 📚 Endpoints

### 1️⃣ Health Check
```bash
curl "http://localhost:8000/health"

# Resposta
{
  "status": "ok",
  "timestamp": "2026-06-07T20:45:00.123456",
  "sumulas_total": 10
}
```

### 2️⃣ Listar Todas as Súmulas
```bash
# Sem filtros
curl "http://localhost:8000/sumulas?api_key=sua_chave"

# Com filtros
curl "http://localhost:8000/sumulas?tipo=SUMULA_VINCULANTE&setor=ADMINISTRATIVO&api_key=sua_chave"

# Com paginação
curl "http://localhost:8000/sumulas?limit=20&offset=0&api_key=sua_chave"
```

**Parâmetros:**
- `tipo` — `SUMULA_VINCULANTE` ou `TEMA_REPERCUSSAO_GERAL`
- `setor` — Filtrar por setor (ADMINISTRATIVO, TRIBUTÁRIO, etc)
- `modulacao` — `true` ou `false`
- `limit` — Número de resultados (1-1000, padrão 50)
- `offset` — Para paginação

### 3️⃣ Obter Detalhe de Uma Súmula
```bash
curl "http://localhost:8000/sumulas/STF_SV_57?api_key=sua_chave"

# Resposta
{
  "numero_identificador": "STF_SV_57",
  "tipo": "SUMULA_VINCULANTE",
  "processo_paradigma": "RE 574.706",
  "data_publicacao": "2008-12-19",
  "enunciado_original": "O direito de greve dos servidores públicos...",
  "nucleo_da_tese": "...",
  "artigos_cf88": ["Art. 9", "Art. 37"],
  "setor_afetado": "ADMINISTRATIVO",
  "houve_modulacao": false,
  "regra_modulacao": null,
  "vulnerabilidade_compliance": "...",
  "confiabilidade": 0.8,
  "requer_revisao_manual": true
}
```

### 4️⃣ Busca Semântica (RAG)
```bash
curl -X POST "http://localhost:8000/sumulas/buscar" \
  -H "Content-Type: application/json" \
  -d '{
    "keywords": ["administrativo", "direito-greve"],
    "limite": 10
  }?api_key=sua_chave'

# Ou via query params
curl "http://localhost:8000/sumulas/buscar?keywords=administrativo&keywords=direito&limite=10&api_key=sua_chave"
```

### 5️⃣ Súmulas com Modulação (Críticas)
```bash
curl "http://localhost:8000/sumulas/com-modulacao?api_key=sua_chave"

# Resposta — todas as com modulação
[
  {
    "numero_identificador": "STF_TEMA_69",
    "tipo": "TEMA_REPERCUSSAO_GERAL",
    "setor_afetado": "TRIBUTÁRIO",
    "regra_modulacao": "efeitos a partir de 15/03/2017",
    ...
  }
]
```

### 6️⃣ Estatísticas por Setor
```bash
curl "http://localhost:8000/sumulas/por-setor?api_key=sua_chave"

# Resposta
[
  {
    "setor_afetado": "TRIBUTÁRIO",
    "total": 45,
    "com_modulacao": 12,
    "ultima_alteracao": "2026-03-15"
  },
  {
    "setor_afetado": "ADMINISTRATIVO",
    "total": 38,
    "com_modulacao": 8,
    "ultima_alteracao": "2026-02-20"
  }
]
```

### 7️⃣ Alertas de Compliance
```bash
curl "http://localhost:8000/alertas/compliance?api_key=sua_chave"

# Resposta — modulações que requerem revisão
[
  {
    "numero_identificador": "STF_TEMA_220",
    "setor_afetado": "PREVIDENCIÁRIO",
    "regra_modulacao": "regra específica de transição",
    "acao_necessaria": "REVISAR COMPLIANCE IMEDIATAMENTE"
  }
]
```

### 8️⃣ Estatísticas Gerais
```bash
curl "http://localhost:8000/estatisticas?api_key=sua_chave"

# Resposta
{
  "timestamp": "2026-06-07T20:45:00",
  "sumulas": [
    {
      "tipo": "SUMULA_VINCULANTE",
      "total": 5,
      "com_modulacao": 2
    },
    {
      "tipo": "TEMA_REPERCUSSAO_GERAL",
      "total": 5,
      "com_modulacao": 2
    }
  ],
  "total_geral": 10
}
```

---

## 🐍 Exemplos em Python

### Instalar Client
```bash
pip install requests
```

### Listar Súmulas
```python
import requests

BASE_URL = "http://localhost:8000"
API_KEY = "sua_chave_secreta_aqui"

# Listar todas
response = requests.get(
    f"{BASE_URL}/sumulas",
    params={"api_key": API_KEY}
)
print(response.json())

# Com filtros
response = requests.get(
    f"{BASE_URL}/sumulas",
    params={
        "tipo": "SUMULA_VINCULANTE",
        "setor": "ADMINISTRATIVO",
        "api_key": API_KEY
    }
)
print(response.json())
```

### Obter Detalhe
```python
response = requests.get(
    f"{BASE_URL}/sumulas/STF_SV_57",
    params={"api_key": API_KEY}
)
sumula = response.json()
print(sumula['enunciado_original'])
```

### Busca Semântica
```python
response = requests.post(
    f"{BASE_URL}/sumulas/buscar",
    json={
        "keywords": ["administrativo", "direito-greve"],
        "limite": 5
    },
    params={"api_key": API_KEY}
)
resultados = response.json()
for sumula in resultados:
    print(f"{sumula['numero_identificador']}: {sumula['setor_afetado']}")
```

### Alertas de Compliance
```python
response = requests.get(
    f"{BASE_URL}/alertas/compliance",
    params={"api_key": API_KEY}
)
alertas = response.json()
for alerta in alertas:
    print(f"⚠️  {alerta['numero_identificador']}")
    print(f"   Setor: {alerta['setor_afetado']}")
    print(f"   Ação: {alerta['acao_necessaria']}")
```

---

## 🔧 Variáveis de Ambiente

```bash
# .env
DB_HOST=localhost
DB_NAME=fenice_brain
DB_USER=postgres
DB_PASSWORD=sua_senha
API_KEY=sua_chave_secreta_aqui
```

Ou via linha de comando:
```bash
export DB_HOST=localhost
export DB_NAME=fenice_brain
export API_KEY=sua_chave
python api_stf_fastapi.py
```

---

## 🐳 Deploy com Docker

### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY api_stf_fastapi.py .

ENV DB_HOST=postgres
ENV DB_NAME=fenice_brain
ENV DB_USER=postgres
ENV API_KEY=sua_chave

CMD ["python", "api_stf_fastapi.py"]
```

### requirements.txt
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
psycopg2-binary==2.9.9
python-dotenv==1.0.0
```

### Docker Compose
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: fenice_brain
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - ./schema_stf_postgresql.sql:/docker-entrypoint-initdb.d/schema.sql

  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      DB_HOST: postgres
      DB_NAME: fenice_brain
      DB_USER: postgres
      DB_PASSWORD: postgres
      API_KEY: sua_chave_secreta
    depends_on:
      - postgres
```

Rodar:
```bash
docker-compose up
```

---

## 📊 Casos de Uso

### Compliance Officer
```bash
# Verificar todas as modulações
curl "http://localhost:8000/alertas/compliance?api_key=sua_chave" | jq .

# Estatísticas por setor
curl "http://localhost:8000/sumulas/por-setor?api_key=sua_chave" | jq '.[] | select(.com_modulacao > 0)'
```

### Desenvolvedor SaaS Jurídico
```python
# Buscar súmulas relevantes para cliente
response = requests.get(
    "http://localhost:8000/sumulas/buscar",
    json={"keywords": ["tributário", "imposto"]},
    params={"api_key": API_KEY}
)
clientes_afetados = response.json()
```

### Analytics/Dashboard
```bash
# Exportar para Grafana
curl "http://localhost:8000/estatisticas?api_key=sua_chave" | jq .
```

---

## 🐛 Troubleshooting

### "Database connection failed"
```bash
# Verificar conexão PostgreSQL
psql -U postgres -h localhost -d fenice_brain -c "SELECT COUNT(*) FROM stf.sumulas;"
```

### "Endpoint returns 403"
```bash
# Verificar API_KEY
echo "API_KEY atual: $(echo $API_KEY)"
```

### "Query timeout"
```bash
# Aumentar timeout ou reduzir limit
curl "http://localhost:8000/sumulas?limit=10&api_key=sua_chave"
```

---

## 📈 Performance

- **Índices:** Criados em `tipo`, `numero_numerico`, `setor_afetado`, `houve_modulacao`, `keywords`
- **Limit máximo:** 1.000 resultados por requisição
- **Cache:** Implementar no proxy (nginx) ou no cliente

---

## 🔐 Segurança

- [ ] Usar HTTPS em produção
- [ ] Rotacionar API_KEY regularmente
- [ ] Limitar taxa (rate limiting)
- [ ] Logar requisições
- [ ] Autenticação mais robusta (OAuth2, JWT)

---

## Próximas Integrações

1. **Embeddings** — Integrar com OpenAI para busca semântica melhorada
2. **WebSockets** — Streaming de alertas em tempo real
3. **GraphQL** — Alternativa a REST


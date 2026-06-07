# PostgreSQL Setup — Fenice Brain STF Database

## 1️⃣ Instalação PostgreSQL

### Windows
```powershell
# Via Chocolatey (recomendado)
choco install postgresql

# Ou baixar em: https://www.postgresql.org/download/windows/
```

### macOS
```bash
brew install postgresql@15
brew services start postgresql@15
```

### Linux (Ubuntu/Debian)
```bash
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

---

## 2️⃣ Criar Database e Usuário

```bash
# Conectar como superuser
psql -U postgres

# Criar database
CREATE DATABASE fenice_brain;

# Criar usuário (opcional)
CREATE USER fenice WITH PASSWORD 'sua_senha_segura';
ALTER ROLE fenice CREATEDB;

# Dar permissões
GRANT ALL PRIVILEGES ON DATABASE fenice_brain TO fenice;

# Sair
\q
```

---

## 3️⃣ Criar Schema

```bash
# Opção 1: Via script SQL
psql -U postgres -d fenice_brain -f schema_stf_postgresql.sql

# Opção 2: Via Python (recomendado)
python import_stf_to_postgresql.py --host localhost --database fenice_brain --user postgres --password ""
```

---

## 4️⃣ Importar Dados (SV + RG)

### Primeira Execução (com schema)
```bash
python import_stf_to_postgresql.py \
  --host localhost \
  --database fenice_brain \
  --user postgres \
  --password "" \
  --schema-file schema_stf_postgresql.sql \
  --json-file exports/stf_sumulas_export.json
```

### Execuções Posteriores (apenas dados)
```bash
python import_stf_to_postgresql.py \
  --host localhost \
  --database fenice_brain \
  --user postgres \
  --skip-schema
```

---

## 5️⃣ Queries Úteis

### Conectar ao banco
```bash
psql -U postgres -d fenice_brain
```

### Ver Estatísticas
```sql
SELECT tipo, COUNT(*) as total, 
       COUNT(CASE WHEN houve_modulacao THEN 1 END) as com_modulacao
FROM stf.sumulas
GROUP BY tipo;
```

### Súmulas com Modulação (⚠️ Críticas)
```sql
SELECT * FROM stf.sumulas_com_modulacao;

-- Ou mais detalhes:
SELECT numero_identificador, setor_afetado, regra_modulacao, data_publicacao
FROM stf.sumulas
WHERE houve_modulacao = TRUE AND status = 'ATIVO'
ORDER BY data_publicacao DESC;
```

### Súmulas por Setor (para compliance)
```sql
SELECT * FROM stf.sumulas_por_setor
ORDER BY total DESC;
```

### Busca por Palavras-Chave (RAG)
```sql
SELECT * FROM stf.buscar_por_keywords(ARRAY['administrativo', 'direito-greve']);

-- Ou:
SELECT * FROM stf.buscar_por_keywords(ARRAY['tributário', 'imposto'], 5);
```

### Súmulas Vinculantes
```sql
SELECT * FROM stf.sv_list;

-- Com paginação:
SELECT * FROM stf.sv_list LIMIT 10 OFFSET 0;
```

### Temas de Repercussão Geral
```sql
SELECT * FROM stf.tema_rg_list;

-- Apenas HIGH impact:
SELECT * FROM stf.tema_rg_list 
WHERE potencial_monetario = 'HIGH';
```

### Alertas de Compliance
```sql
SELECT * FROM stf.alertar_modulacoes();
```

### Artigos CF/88 Mais Citados
```sql
SELECT artigo, COUNT(*) as referencias
FROM stf.sumula_artigos_cf
GROUP BY artigo
ORDER BY referencias DESC
LIMIT 10;
```

### Súmulas que Requerem Revisão Manual
```sql
SELECT numero_identificador, setor_afetado, confiabilidade
FROM stf.sumulas
WHERE requer_revisao_manual = TRUE
ORDER BY confiabilidade ASC;
```

---

## 6️⃣ Integração com Aplicações

### Python (psycopg2)
```python
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="fenice_brain",
    user="postgres",
    password=""
)
cursor = conn.cursor()

# Buscar
cursor.execute("""
    SELECT numero_identificador, setor_afetado 
    FROM stf.sumulas 
    WHERE houve_modulacao = TRUE
""")

for row in cursor.fetchall():
    print(row)

conn.close()
```

### Node.js (pg)
```javascript
const { Client } = require('pg');

const client = new Client({
    host: 'localhost',
    database: 'fenice_brain',
    user: 'postgres',
    password: ''
});

await client.connect();

const result = await client.query(
    'SELECT * FROM stf.sumulas_com_modulacao'
);

console.log(result.rows);
await client.end();
```

### SQL Direto
```bash
psql -U postgres -d fenice_brain -c "SELECT COUNT(*) FROM stf.sumulas;"
```

---

## 7️⃣ Backup e Restore

### Backup Completo
```bash
pg_dump -U postgres -d fenice_brain > backup_fenice_brain.sql
```

### Backup apenas dados (sem schema)
```bash
pg_dump -U postgres -d fenice_brain --data-only > dados_sumulas.sql
```

### Restaurar
```bash
psql -U postgres -d fenice_brain < backup_fenice_brain.sql
```

---

## 8️⃣ Performance

### Índices já criados
```sql
-- Visualizar índices
\d stf.sumulas

-- Ou via query
SELECT schemaname, tablename, indexname 
FROM pg_indexes 
WHERE schemaname = 'stf';
```

### Análise de query
```sql
EXPLAIN ANALYZE
SELECT * FROM stf.sumulas WHERE houve_modulacao = TRUE;
```

### Vacuum e Analyze (manutenção)
```sql
VACUUM ANALYZE stf.sumulas;
REINDEX TABLE stf.sumulas;
```

---

## 9️⃣ Monitoramento

### Tamanho do banco
```sql
SELECT pg_size_pretty(pg_database_size('fenice_brain'));
```

### Tamanho das tabelas
```sql
SELECT schemaname, tablename, pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename))
FROM pg_tables
WHERE schemaname = 'stf'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

### Conexões ativas
```sql
SELECT datname, count(*) 
FROM pg_stat_activity 
GROUP BY datname;
```

---

## 🔟 Troubleshooting

### Erro: "FATAL: Ident authentication failed"
Editar `pg_hba.conf` (geralmente em `C:\Program Files\PostgreSQL\15\data\pg_hba.conf`):
Trocar `ident` por `md5` ou `password` para a linha de localhost.

### Erro: "database does not exist"
```bash
psql -U postgres -l  # Listar databases
```

### Verificar se PostgreSQL está rodando
```bash
# Windows
Get-Service postgresql*

# Linux
sudo systemctl status postgresql

# macOS
brew services list | grep postgres
```

### Conectar sem senha
Criar `~/.pgpass` (macOS/Linux) ou `%APPDATA%\postgresql\pgpass.conf` (Windows):
```
localhost:5432:fenice_brain:postgres:
```

---

## 📚 Próximas Integrações

1. **API REST** — FastAPI endpoints para busca
2. **Embeddings** — OpenAI/Anthropic para RAG
3. **Alertas** — Webhook quando modulação detectada
4. **Dashboard** — Grafana/Metabase para compliance

---

## 📖 Referências

- [PostgreSQL Docs](https://www.postgresql.org/docs/)
- [psycopg2](https://www.psycopg.org/)
- [pg Node.js](https://node-postgres.com/)


# Dashboard Grafana — Fenice Brain STF

## 🎯 Visão Geral

Dashboard em tempo real para visualizar jurisprudência STF, alertas de compliance, e performance de webhooks. Inclui:

- 📊 **Dashboard Principal** — Estatísticas gerais, distribuição por setor, timelines
- 🚨 **Dashboard Compliance** — Modulações críticas, webhooks, alertas
- 📈 **Gráficos em tempo real** — Auto-refresh a cada 1-5 minutos
- 🔍 **Filtros customizáveis** — Por período, setor, tipo

---

## 🚀 Quick Start (Docker)

### 1️⃣ Preparar Estrutura

```bash
# Clonar diretórios necessários
mkdir -p provisioning/datasources provisioning/dashboards

# Copiar arquivos de configuração
cp docker-compose-grafana.yml docker-compose.yml
cp provisioning/datasources/postgres.yml ./provisioning/datasources/
cp provisioning/dashboards/*.json ./provisioning/dashboards/
```

### 2️⃣ Rodar Stack

```bash
docker-compose up -d

# Ou com logs
docker-compose up
```

**Output esperado:**
```
Creating fenice-postgres   ... done
Creating fenice-grafana    ... done
Creating fenice-pgadmin    ... done
```

### 3️⃣ Acessar Dashboards

| Serviço | URL | Credenciais |
|---------|-----|------------|
| **Grafana** | http://localhost:3000 | admin / admin |
| **pgAdmin** | http://localhost:5050 | admin@fenice.local / admin |
| **PostgreSQL** | localhost:5432 | fenice / fenice_secure_password |

---

## 📊 Dashboards Disponíveis

### 1. Dashboard Principal — "Fenice Brain STF Jurisprudência"

**Painéis:**
- 📊 **Total de Súmulas** — Métrica de quantidade total
- 📈 **Timeline de Publicações** — Série temporal de súmulas publicadas
- 🎯 **Distribuição por Setor** — Pizza chart (Administrativo, Tributário, etc)
- ⚠️ **Súmulas com Modulação** — Contagem de críticas
- 🎯 **Modulação por Setor** — Stacked bar chart comparativo
- 🏛️ **Tipo de Jurisprudência** — Sumula Vinculante vs Tema RG
- 📊 **Taxa de Modulação (%)** — Gauge (meta: < 20%)

**Atualização:** 1 minuto

---

### 2. Dashboard Compliance — "Compliance & Webhooks"

**Painéis:**
- 🔗 **Webhooks Ativos** — Quantos estão ligados
- ⏳ **Alertas Pendentes** — Ainda não processados
- ✅ **Taxa Sucesso Webhooks (24h)** — Gauge (meta: > 95%)
- 🚨 **Requer Revisão Manual** — Súmulas críticas
- 📈 **Webhooks Disparados vs Falhas** — Timeline (30 dias)
- ⚠️ **Modulações Críticas por Setor** — Top setores com modulação
- 🔗 **Performance de Webhooks** — Sucessos vs falhas por webhook (7 dias)

**Atualização:** 5 minutos

---

## 🔧 Configuração Manual (sem Docker)

### 1️⃣ Instalar Grafana

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install -y software-properties-common
sudo add-apt-repository "deb https://packages.grafana.com/oss/deb stable main"
sudo apt-get update
sudo apt-get install grafana-server
sudo systemctl start grafana-server
sudo systemctl enable grafana-server
```

**macOS:**
```bash
brew install grafana
brew services start grafana
```

**Windows:**
Download em https://grafana.com/grafana/download

### 2️⃣ Adicionar Datasource PostgreSQL

1. Abrir Grafana: http://localhost:3000
2. Login: admin / admin
3. Menu → **Connections → Datasources**
4. Clique **Add datasource**
5. Selecione **PostgreSQL**
6. Preencha:
   - **Name:** Fenice Brain — STF
   - **Host:** localhost:5432
   - **Database:** fenice_brain
   - **User:** postgres (ou fenice)
   - **Password:** (sua senha)
   - **SSL Mode:** disable
7. Clique **Save & Test**

### 3️⃣ Importar Dashboards

**Opção A: Via UI**
1. Menu → **Dashboards → New → Import**
2. Upload JSON file:
   - `fenice-main.json`
   - `fenice-compliance.json`

**Opção B: Via CLI**
```bash
# Copia os arquivos para Grafana
cp provisioning/dashboards/*.json /var/lib/grafana/dashboards/
sudo systemctl restart grafana-server
```

---

## 📈 Queries SQL dos Dashboards

### Total de Súmulas
```sql
SELECT COUNT(*) as "Total de Súmulas" FROM stf.sumulas
```

### Distribuição por Setor
```sql
SELECT setor_afetado as "Setor", COUNT(*) as "Total"
FROM stf.sumulas
WHERE setor_afetado IS NOT NULL
GROUP BY setor_afetado
ORDER BY COUNT(*) DESC
```

### Modulações Críticas
```sql
SELECT 
    numero_identificador,
    tipo,
    setor_afetado,
    regra_modulacao,
    data_publicacao
FROM stf.sumulas
WHERE houve_modulacao = TRUE AND status = 'ATIVO'
ORDER BY data_publicacao DESC
LIMIT 100
```

### Performance de Webhooks
```sql
SELECT 
    w.nome,
    COUNT(*) as total,
    COUNT(CASE WHEN h.sucesso THEN 1 END) as sucessos,
    COUNT(CASE WHEN h.sucesso = FALSE THEN 1 END) as falhas,
    ROUND(COUNT(CASE WHEN h.sucesso THEN 1 END)::FLOAT / COUNT(*) * 100, 2) as taxa_sucesso,
    AVG(h.tempo_ms) as tempo_medio_ms
FROM stf.webhooks w
LEFT JOIN stf.webhook_history h ON w.id = h.webhook_id
WHERE h.acionado_em > NOW() - INTERVAL '7 days'
GROUP BY w.id, w.nome
ORDER BY taxa_sucesso DESC
```

### Timeline de Alertas
```sql
SELECT 
    DATE(acionado_em) as data,
    COUNT(CASE WHEN sucesso THEN 1 END) as sucessos,
    COUNT(CASE WHEN sucesso = FALSE THEN 1 END) as falhas
FROM stf.webhook_history
WHERE acionado_em > NOW() - INTERVAL '30 days'
GROUP BY DATE(acionado_em)
ORDER BY data
```

---

## 🎨 Customizar Dashboards

### Adicionar Novo Painel

1. Abrir dashboard
2. Clique **Add panel**
3. Escolha visualização (Stat, Graph, Table, etc)
4. Escreva query SQL
5. Configure cores, thresholds, legends
6. Salve

**Exemplo — Top 10 Súmulas Críticas:**
```sql
SELECT 
    numero_identificador,
    setor_afetado,
    potencial_monetario,
    vulnerabilidade_compliance
FROM stf.sumulas
WHERE houve_modulacao = TRUE AND status = 'ATIVO'
ORDER BY 
    CASE potencial_monetario
        WHEN 'HIGH' THEN 1
        WHEN 'MEDIUM' THEN 2
        ELSE 3
    END,
    data_publicacao DESC
LIMIT 10
```

### Modificar Cores/Thresholds

1. Abrir painel
2. Clique **Edit**
3. Vá para **Field options**
4. Configure:
   - **Color mode:** Background, Value, Text
   - **Thresholds:** Define cores por valor
   - **Legend:** Mostrar/ocultar

---

## 📱 Alertas no Grafana

### Criar Alerta de Modulação Alta

1. Abrir dashboard de Compliance
2. Painel **Taxa Sucesso Webhooks**
3. Clique **Alert** → **Create alert**
4. Configure:
   - **Condition:** `Taxa_sucesso < 80`
   - **For:** 5 minutes
   - **If:** Send notification to Slack/Email
5. Salve

---

## 🔐 Segurança

### Proteger Grafana com Senha Forte

```bash
# Via CLI
docker exec -it fenice-grafana grafana-cli admin reset-admin-password NEW_PASSWORD

# Ou editar /etc/grafana/grafana.ini (local)
[security]
admin_user = admin
admin_password = SenhaForte123!
```

### Restringir Acesso por IP

```nginx
# nginx.conf
location / {
    allow 192.168.1.0/24;  # Sua rede
    deny all;
    proxy_pass http://grafana:3000;
}
```

---

## 📊 Casos de Uso

### Compliance Officer

Dashboard **Compliance & Webhooks:**
- Ver alertas pendentes em tempo real
- Monitorar taxa de sucesso de notificações
- Identificar setores com mais modulações

### Gestor Jurídico

Dashboard **Principal:**
- Estatísticas gerais de súmulas
- Tendências por setor
- Taxa de modulação da instituição

### DevOps/SRE

Monitorar health via alerts:
```
IF webhooks_ativos < 1 → Alerta
IF taxa_sucesso < 85% → Alerta
IF alertas_pendentes > 100 → Alerta
```

---

## 🐛 Troubleshooting

### "Cannot connect to PostgreSQL"

```bash
# Verificar conexão
docker exec fenice-postgres psql -U fenice -d fenice_brain -c "SELECT 1"

# Logs do Grafana
docker logs fenice-grafana | grep -i "postgres\|connection"
```

### "Dashboard shows no data"

1. Verificar datasource está conectado:
   - Menu → **Connections → Data sources**
   - Clique em **Fenice Brain — STF**
   - Clique **Test** no final

2. Verificar dados no banco:
```bash
psql -U fenice -d fenice_brain -c "SELECT COUNT(*) FROM stf.sumulas;"
```

3. Se 0 resultados, rodou `import_stf_to_postgresql.py`?

### "Grafana won't start"

```bash
# Ver logs
docker logs fenice-grafana

# Ou verificar porta
lsof -i :3000

# Reiniciar
docker restart fenice-grafana
```

---

## 📈 Backup/Restore

### Backup Grafana

```bash
# Dashboards JSON
docker exec fenice-grafana \
  find /var/lib/grafana/dashboards -name "*.json" \
  -exec cp {} ./backups/ \;

# Database completo
docker exec fenice-postgres \
  pg_dump -U fenice fenice_brain > fenice_backup.sql
```

### Restore

```bash
docker exec -i fenice-postgres \
  psql -U fenice fenice_brain < fenice_backup.sql
```

---

## 🚀 Deploy em Produção

### Via Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: grafana
spec:
  replicas: 1
  template:
    spec:
      containers:
      - name: grafana
        image: grafana/grafana:latest
        ports:
        - containerPort: 3000
        env:
        - name: GF_SECURITY_ADMIN_PASSWORD
          valueFrom:
            secretKeyRef:
              name: grafana-secret
              key: admin-password
        volumeMounts:
        - name: grafana-storage
          mountPath: /var/lib/grafana
      volumes:
      - name: grafana-storage
        persistentVolumeClaim:
          claimName: grafana-pvc
```

### Via Terraform

```hcl
resource "docker_container" "grafana" {
  name  = "fenice-grafana"
  image = docker_image.grafana.latest
  ports {
    internal = 3000
    external = 3000
  }
  env = [
    "GF_SECURITY_ADMIN_PASSWORD=SecurePassword123!"
  ]
}
```

---

## 📚 Próximas Melhorias

1. **Alertas Automáticos** — Slack/Email quando modulação detectada
2. **Dashboard Dinâmico** — Filtros por período, setor, tipo
3. **Exportar Relatórios** — PDF mensal de compliance
4. **Integração com API** — Sync automático de dados via FastAPI
5. **Heatmap por Semana** — Visualizar padrões temporais

---

## 📖 Referências

- [Grafana Documentation](https://grafana.com/docs/)
- [PostgreSQL Datasource](https://grafana.com/docs/grafana/latest/datasources/postgres/)
- [Building Dashboards](https://grafana.com/docs/grafana/latest/dashboards/)
- [Alert Rules](https://grafana.com/docs/grafana/latest/alerting/alert-rules/)


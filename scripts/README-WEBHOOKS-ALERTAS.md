# Webhooks + Alertas — Fenice Brain STF

## 🎯 Visão Geral

Sistema de notificações em tempo real para modulação de efeitos (jurisprudência crítica). Dispara alertas automáticos via Discord, Slack, Email ou webhooks customizados.

**Funcionalidades:**
- ✅ Notificações automáticas quando modulação detectada
- ✅ Suporte para Discord, Slack, Email, Webhooks customizados
- ✅ Filtros por setor e tipo de súmula
- ✅ Histórico completo de alertas
- ✅ Monitor em tempo real (background worker)

---

## 📦 Instalação

### 1️⃣ Instalar Dependências

```bash
pip install psycopg2-binary requests
```

### 2️⃣ Ativar Schema de Webhooks

```bash
psql -U postgres -d fenice_brain -f schema_webhooks_extension.sql
```

Isso cria:
- Tabela `stf.webhooks` (webhooks registrados)
- Tabela `stf.webhook_history` (histórico de alertas)
- Views para estatísticas
- Trigger para disparar alertas automaticamente

---

## 🚀 Setup Rápido

### Passo 1: Registrar Webhook via API

**Discord:**
```bash
curl -X POST "http://localhost:8000/webhooks" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Discord STF Alertas",
    "url": "https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_TOKEN",
    "tipo": "DISCORD",
    "eventos": ["MODULACAO_DETECTADA"],
    "filtro_setor": null,
    "filtro_tipo": null
  }?api_key=sua_chave'
```

**Slack:**
```bash
curl -X POST "http://localhost:8000/webhooks" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Slack STF Alertas",
    "url": "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK",
    "tipo": "SLACK",
    "eventos": ["MODULACAO_DETECTADA"],
    "filtro_setor": "TRIBUTÁRIO"
  }?api_key=sua_chave'
```

**Webhook Customizado:**
```bash
curl -X POST "http://localhost:8000/webhooks" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Seu Sistema",
    "url": "https://seu-api.com/webhooks/stf",
    "tipo": "CUSTOM",
    "eventos": ["MODULACAO_DETECTADA", "SUMULA_NOVA"],
    "api_key": "sua-api-key-secreta"
  }?api_key=sua_chave'
```

### Passo 2: Iniciar Monitor

```bash
# Execução única (processa alertas pendentes)
python webhooks_monitor.py --uma-vez

# Contínua (background)
python webhooks_monitor.py --intervalo 30 &

# Ou com nohup (survive terminal close)
nohup python webhooks_monitor.py --intervalo 30 > webhooks_monitor.log 2>&1 &
```

### Passo 3: Testar

```bash
# Listar webhooks
curl "http://localhost:8000/webhooks?api_key=sua_chave" | jq

# Ver estatísticas
curl "http://localhost:8000/webhooks/stats?api_key=sua_chave" | jq
```

---

## 📚 Endpoints FastAPI

### 1️⃣ Criar Webhook

```bash
POST /webhooks
```

**Request:**
```json
{
  "nome": "Discord STF Alertas",
  "url": "https://discord.com/api/webhooks/...",
  "tipo": "DISCORD",
  "eventos": ["MODULACAO_DETECTADA"],
  "filtro_setor": "ADMINISTRATIVO",
  "filtro_tipo": "SUMULA_VINCULANTE",
  "api_key": null
}
```

**Response:**
```json
{
  "id": 1,
  "nome": "Discord STF Alertas",
  "url": "https://discord.com/api/webhooks/...",
  "tipo": "DISCORD",
  "eventos": ["MODULACAO_DETECTADA"],
  "ativo": true,
  "total_acionamentos": 0,
  "taxa_sucesso": null,
  "ultimo_acionamento": null
}
```

### 2️⃣ Listar Webhooks

```bash
GET /webhooks?api_key=sua_chave
```

**Response:**
```json
[
  {
    "id": 1,
    "nome": "Discord STF Alertas",
    "tipo": "DISCORD",
    "url": "https://discord.com/api/webhooks/...",
    "ativo": true,
    "total_acionamentos": 5,
    "taxa_sucesso": 100.0,
    "ultimo_acionamento": "2026-06-07T20:45:00",
    "ultimo_status": 204
  },
  {
    "id": 2,
    "nome": "Slack STF Alertas",
    "tipo": "SLACK",
    "url": "https://hooks.slack.com/services/...",
    "ativo": true,
    "total_acionamentos": 3,
    "taxa_sucesso": 100.0,
    "ultimo_acionamento": "2026-06-07T20:40:00",
    "ultimo_status": 200
  }
]
```

### 3️⃣ Deletar Webhook

```bash
DELETE /webhooks/1?api_key=sua_chave
```

### 4️⃣ Ativar/Desativar Webhook

```bash
# Ativar
PATCH /webhooks/1/ativar?api_key=sua_chave

# Desativar
PATCH /webhooks/1/desativar?api_key=sua_chave
```

### 5️⃣ Estatísticas de Webhooks

```bash
GET /webhooks/stats?api_key=sua_chave
```

**Response:**
```json
{
  "periodo": "últimos 7 dias",
  "total_alertas": 15,
  "sucessos": 14,
  "falhas": 1,
  "pendentes": 0,
  "taxa_sucesso": 93.33
}
```

---

## 🔗 Como Funciona

### 1. Trigger no PostgreSQL

Quando uma súmula com `houve_modulacao = TRUE` é salva:

```sql
-- Trigger automático dispara:
INSERT INTO stf.webhook_history 
  (webhook_id, evento, numero_sumula, payload, sucesso)
VALUES (..., 'MODULACAO_DETECTADA', ..., NULL);
```

Payload contém:
```json
{
  "evento": "MODULACAO_DETECTADA",
  "numero_identificador": "STF_TEMA_220",
  "tipo": "TEMA_REPERCUSSAO_GERAL",
  "setor_afetado": "TRIBUTÁRIO",
  "regra_modulacao": "Efeitos a partir de 15/03/2017",
  "potencial_monetario": "HIGH",
  "vulnerabilidade_compliance": "Requer revisão imediata",
  "data_detectada": "2026-06-07T20:45:00"
}
```

### 2. Monitor Processa Alertas Pendentes

```
⏰ Cada 30 segundos:
  1. Busca alertas onde sucesso IS NULL
  2. Dispara para cada webhook
  3. Registra resultado (sucesso, status HTTP, tempo)
```

### 3. Notificações Formatadas

**Discord:**
- Embed colorido (vermelho HIGH, laranja MEDIUM, amarelo LOW)
- Campos estruturados (Setor, Monetário, Regra, Compliance)
- Timestamp automático

**Slack:**
- Message blocks estruturada
- Headers e seções
- Cores por urgência (danger, warning, good)

---

## 🐍 Uso em Python

### Registrar Webhook Programaticamente

```python
from webhooks_notifier import WebhookManager

manager = WebhookManager(db_host="localhost")

if manager.conectar():
    # Criar webhook
    manager.criar_webhook(
        nome="Meu Sistema",
        url="https://meu-api.com/webhooks/stf",
        tipo="CUSTOM",
        eventos=["MODULACAO_DETECTADA", "SUMULA_NOVA"],
        filtro_setor="TRIBUTÁRIO",
        api_key="minha-api-key"
    )
    
    # Listar
    webhooks = manager.listar_webhooks()
    for webhook in webhooks:
        print(f"{webhook[1]} — {webhook[3]}")
    
    manager.fechar()
```

### Disparar Webhook Manualmente

```python
from webhooks_notifier import WebhookNotifier

notifier = WebhookNotifier()

payload = {
    'evento': 'MODULACAO_DETECTADA',
    'numero_identificador': 'STF_TEMA_220',
    'tipo': 'TEMA_REPERCUSSAO_GERAL',
    'setor_afetado': 'TRIBUTÁRIO',
    'regra_modulacao': 'Efeitos a partir de 15/03/2017',
    'potencial_monetario': 'HIGH',
    'vulnerabilidade_compliance': 'Requer revisão',
    'data_detectada': '2026-06-07T20:45:00'
}

# Discord
sucesso, status, msg = notifier.notificar(
    "https://discord.com/api/webhooks/...",
    "DISCORD",
    payload
)
print(f"Status: {status}, Sucesso: {sucesso}")

# Slack
sucesso, status, msg = notifier.notificar(
    "https://hooks.slack.com/services/...",
    "SLACK",
    payload
)

# Custom
sucesso, status, msg = notifier.notificar(
    "https://seu-api.com/webhooks/stf",
    "CUSTOM",
    payload,
    api_key="sua-api-key"
)
```

### Monitor Manual

```python
from webhooks_monitor import WebhookMonitor

monitor = WebhookMonitor(
    db_host="localhost",
    intervalo=30
)

# Executar uma vez
monitor.conectar()
monitor.processar_ciclo()
monitor.fechar()

# Ou contínuo
monitor.executar(max_ciclos=100)
```

---

## 🎯 Casos de Uso

### Compliance Officer

Recebe alertas no Discord quando modulação detectada:

```
Webhook: Discord STF Alertas
Filtro: Todos os setores
Eventos: MODULACAO_DETECTADA
→ Notificação em tempo real quando STF modula efeitos
```

### Advogado Tributário

Apenas alertas de setor tributário:

```
Webhook: Slack Advogado Tributário
Filtro Setor: TRIBUTÁRIO
Filtro Tipo: TEMA_REPERCUSSAO_GERAL
Eventos: MODULACAO_DETECTADA, SUMULA_NOVA
```

### Sistema Integrado

Seu próprio backend recebe webhooks:

```
Webhook: Meu Sistema
Tipo: CUSTOM
API Key: minha-chave-secreta
→ POST https://meu-api.com/webhooks/stf
   Body: JSON com payload acima
```

---

## 🔐 Discord Setup

### Criar Webhook no Discord

1. Abrir servidor Discord
2. Ir em `Server Settings → Integrations → Webhooks`
3. Criar novo webhook
4. Copiar URL: `https://discord.com/api/webhooks/YOUR_ID/YOUR_TOKEN`

```bash
# Testar webhook Discord manualmente
curl -X POST "https://discord.com/api/webhooks/YOUR_ID/YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Teste",
    "embeds": [{
      "title": "Alerta STF",
      "description": "Modulação detectada"
    }]
  }'
```

---

## 🔐 Slack Setup

### Criar Webhook no Slack

1. Ir em [api.slack.com/apps](https://api.slack.com/apps)
2. Create New App → From scratch
3. Ativar "Incoming Webhooks"
4. Add New Webhook to Workspace
5. Escolher canal
6. Copiar URL: `https://hooks.slack.com/services/...`

```bash
# Testar webhook Slack manualmente
curl -X POST "https://hooks.slack.com/services/YOUR/WEBHOOK/URL" \
  -d 'payload={"text":"Teste de alerta STF"}'
```

---

## 📊 Queries SQL Úteis

### Ver Histórico de Alertas

```sql
-- Últimos 10 alertas
SELECT 
    h.id,
    h.evento,
    h.numero_sumula,
    h.sucesso,
    h.http_status,
    h.tempo_ms,
    h.acionado_em
FROM stf.webhook_history h
ORDER BY h.acionado_em DESC
LIMIT 10;

-- Alertas falhados
SELECT * FROM stf.webhook_history 
WHERE sucesso = FALSE 
ORDER BY acionado_em DESC;

-- Taxa de sucesso por webhook
SELECT 
    w.nome,
    COUNT(*) as total,
    COUNT(CASE WHEN h.sucesso THEN 1 END) as sucessos,
    ROUND(COUNT(CASE WHEN h.sucesso THEN 1 END)::FLOAT / COUNT(*) * 100, 2) as taxa_sucesso
FROM stf.webhooks w
LEFT JOIN stf.webhook_history h ON w.id = h.webhook_id
WHERE h.acionado_em > NOW() - INTERVAL '24 hours'
GROUP BY w.id, w.nome;
```

### Alertas Pendentes

```sql
-- Alertas não processados ainda
SELECT * FROM stf.webhook_history 
WHERE sucesso IS NULL
ORDER BY acionado_em;

-- Contar pendentes
SELECT COUNT(*) FROM stf.webhook_history WHERE sucesso IS NULL;
```

---

## 🚨 Troubleshooting

### "HTTP 404 on Discord webhook"

❌ URL incorreta ou webhook deletado

```bash
# Verificar webhook
curl -X GET "https://discord.com/api/webhooks/YOUR_ID/YOUR_TOKEN"
```

✅ Criar novo webhook no Discord

### "Alertas não estão sendo disparados"

1. Verificar se monitor está rodando:
```bash
ps aux | grep webhooks_monitor.py
```

2. Verificar se há alertas pendentes:
```sql
SELECT COUNT(*) FROM stf.webhook_history WHERE sucesso IS NULL;
```

3. Executar monitor manualmente:
```bash
python webhooks_monitor.py --uma-vez -vv
```

### "Webhook está ativo mas não dispara"

Verificar filtros:

```sql
SELECT nome, filtro_setor, filtro_tipo, eventos 
FROM stf.webhooks 
WHERE id = 1;
```

Se setor/tipo está filtrado e não bate com a súmula, não dispara.

---

## 📈 Monitoramento

### Ver Status de Todos Webhooks

```sql
SELECT * FROM stf.webhook_stats;
```

### Uptime de Webhooks

```sql
SELECT 
    nome,
    tipo,
    total_acionamentos,
    taxa_sucesso,
    ultimo_acionamento
FROM stf.webhook_stats
ORDER BY taxa_sucesso DESC;
```

---

## 🔄 Deploy em Produção

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY webhooks_*.py .
COPY schema_webhooks_extension.sql .

CMD ["python", "webhooks_monitor.py"]
```

### Systemd (Linux)

```ini
[Unit]
Description=Fenice Brain Webhooks Monitor
After=network.target postgresql.service

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/fenice-brain
ExecStart=/usr/bin/python3 /opt/fenice-brain/webhooks_monitor.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable fenice-webhooks-monitor
sudo systemctl start fenice-webhooks-monitor
sudo systemctl status fenice-webhooks-monitor
```

---

## 📚 Próximas Melhorias

1. **Rate Limiting** — Não enviar > N alertas por minuto
2. **Retry Strategy** — Exponential backoff para falhas
3. **Email Templates** — HTML customizável
4. **Webhook Signature** — HMAC para segurança
5. **Dead Letter Queue** — Alertas não processáveis
6. **Admin Dashboard** — Interface web para gerenciar webhooks

---

## 📖 Referências

- [Discord Webhooks](https://discord.com/developers/docs/resources/webhook)
- [Slack Incoming Webhooks](https://api.slack.com/messaging/webhooks)
- [PostgreSQL Triggers](https://www.postgresql.org/docs/current/sql-createtrigger.html)


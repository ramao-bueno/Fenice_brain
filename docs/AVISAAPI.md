# AvisaAPI — Documentação Operacional
**© 2026 Fenice IT Justech.ia · Tech Lead: Ramão Bueno da Silva Neto**
**Atualizado: 2026-06-25**

---

## O que é

AvisaAPI (`avisaapi.com.br`) é o provedor de WhatsApp Business usado no chatbot jurídico do `fenice.ia.br`.
Recebe mensagens dos clientes via webhook e envia respostas geradas pelo Groq (llama-3.3-70b-versatile).

---

## Configuração Atual

| Item | Valor |
|---|---|
| Endpoint de envio | `https://www.avisaapi.com.br/api/actions/sendMessage` |
| Auth | Bearer token via env `AVISA_API_TOKEN` |
| Webhook recebimento | `POST https://fenice.ia.br/webhook/avisa` |
| Env var no Vercel | `AVISA_API_TOKEN` (projeto `fenice-justech`) |

---

## Procedimento de Emergência (se AvisaAPI cair)

1. Verificar status em `avisaapi.com.br`
2. Se fora do ar por mais de 30 minutos → ativar alternativa abaixo
3. Informar clientes via outro canal

### Alternativa Imediata: Meta Cloud API (gratuita)

```
1. Acessar developers.facebook.com → WhatsApp → Getting Started
2. Criar app Business
3. Substituir em api_fenice_saas.py:
   URL: https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages
   Header: Authorization: Bearer {META_TOKEN}
   Body: { "messaging_product": "whatsapp", "to": numero, "type": "text",
           "text": { "body": resposta_ai } }
4. Atualizar env var AVISA_API_TOKEN → META_WA_TOKEN
```

### Alternativa Corporativa: Twilio (pago, ~$0.005/msg)

```
pip install twilio
from twilio.rest import Client
client = Client(TWILIO_SID, TWILIO_AUTH)
client.messages.create(from_='whatsapp:+14155238886', to=f'whatsapp:{numero}', body=resposta_ai)
```

---

## Monitoramento

Toda interação é logada na tabela `interacoes_whatsapp` do Supabase:
- `http_status_avisa` — status da resposta da AvisaAPI
- `entregue` — boolean confirmando entrega
- Verificar regularmente: `SELECT http_status_avisa, COUNT(*) FROM interacoes_whatsapp GROUP BY 1`

---

## Alertas a Configurar

- [ ] Alerta Supabase quando `entregue = false` por mais de 10 mensagens seguidas
- [ ] Cron semanal para verificar saldo/status do plano AvisaAPI

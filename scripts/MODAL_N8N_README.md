# 🤖 Modal Téo — Integração N8N + WhatsApp

**Status:** ✅ Pronto para envio corporativo

---

## 📋 Resumo

Integração completa do **modal de atendimento Téo Intelligence Concierge** com:
- ✅ Evolution API (WhatsApp corporativo)
- ✅ N8N Workflow automático
- ✅ Supabase logging
- ✅ Scripts de envio e testes

---

## 🎯 Componentes

### 1. **modal_preview.html** (UI)
- Visualização completa do modal Téo
- 3 opções de menu + especialista
- Design responsivo WhatsApp
- Header, chat, input bar

### 2. **n8n_modal_integration.json** (Workflow)
Workflow N8N com 6 nós:

```
Webhook → Extrair Dados → Enviar via Evolution API → Validar → Log Supabase
```

**Funcionalidades:**
- Recebe trigger via webhook
- Extrai número WhatsApp
- Envia modal formatado
- Registra em Supabase para analytics

### 3. **Scripts de Envio**

#### **send_modal_to_whatsapp.js** (Node.js)
```bash
node send_modal_to_whatsapp.js [numero]
node send_modal_to_whatsapp.js 5521967531414
```

#### **modal_screenshot_n8n.py** (Python)
```bash
python modal_screenshot_n8n.py [numero] [--deploy] [--test]

# Exemplos:
python modal_screenshot_n8n.py 5521967531414
python modal_screenshot_n8n.py 5521967531414 --test
python modal_screenshot_n8n.py 5521967531414 --deploy
```

---

## 🚀 Como Usar

### **Opção 1: Enviar mensagem de teste agora**

```bash
cd C:\Fenice_bRain\scripts
python modal_screenshot_n8n.py 5547991041414 --test
```

Resultado:
```
✅ Mensagem de teste enviada para 5547991041414
```

### **Opção 2: Deploy no N8N Cloud**

1. Acesse: https://feniceit.app.n8n.cloud
2. Clique em **+ New Workflow**
3. Copie o conteúdo de `n8n_modal_integration.json`
4. Importe como novo workflow
5. Ative o webhook
6. Teste com:

```bash
curl -X POST https://feniceit.app.n8n.cloud/webhook/modal-preview \
  -H "Content-Type: application/json" \
  -d '{
    "numero": "5547991041414",
    "nome": "Ramão Bueno",
    "email": "oiconsulbrasil@gmail.com",
    "tema": "fenice-tim"
  }'
```

### **Opção 3: Integrar ao workflow existente (v4)**

Adicione um novo nó ao workflow `Fenice_Tim — WhatsApp IVR v4`:

1. Após nó `8. Enviar Menu` 
2. Adicione: **HTTP Request**
3. Configure:
   - Method: `POST`
   - URL: `https://evolution-api-9fbw.srv1784289.hstgr.cloud/message/sendText/fenice-tim-prod`
   - Headers:
     - `apikey: XpwOsi1Zq6gLRnISF5bN9PvEFzeMfKA7`
     - `Content-Type: application/json`
   - Body:
   ```json
   {
     "number": "{{ $json.numero }}",
     "text": "👤 *Teo — Intelligence Concierge* 🤖\n\n[MODAL_PREVIEW]\n\n© 2026 Fenice IT · Justech.IA"
   }
   ```

---

## 📱 Números Corporativos

| Número | Tipo | Uso |
|--------|------|-----|
| `5547991041414` | Corporativo (Principal) | Envios de modal e WOW Experience |
| `554797348385` | Ramão (ADMIN_WHATSAPP) | Alertas críticos |

---

## 🔐 Credenciais (em .env)

```bash
EVOLUTION_API_URL=https://evolution-api-9fbw.srv1784289.hstgr.cloud
EVOLUTION_API_KEY=XpwOsi1Zq6gLRnISF5bN9PvEFzeMfKA7
EVOLUTION_INSTANCE=fenice-tim-prod

N8N_WEBHOOK_URL=https://feniceit.app.n8n.cloud/webhook/fenice-tim-v2
N8N_API_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## 📊 Analytics & Logging

Todos os envios são registrados em Supabase:

**Tabela:** `modal_preview_log`

```sql
SELECT 
  numero, 
  nome, 
  tema,
  sucesso,
  timestamp 
FROM modal_preview_log 
ORDER BY timestamp DESC;
```

---

## 🐛 Troubleshooting

### ❌ "Erro 401: Invalid API Key"
- Verifique `EVOLUTION_API_KEY` no .env
- Confirme instância: `fenice-tim-prod`

### ❌ "Erro 400: Invalid number format"
- Número deve estar no formato: `55XXXXXXXXXXX` (sem símbolos)
- Exemplo correto: `5521967531414`

### ❌ "Webhook não foi acionado"
- Confirme que o N8N está ativo
- Verifique URL do webhook
- Teste com `curl` antes

---

## 🔄 Fluxo Completo

```
1. Usuário acessa fenice.ia.br
   ↓
2. Preencheu formulário (leads)
   ↓
3. N8N webhook recebe dados
   ↓
4. Evolution API envia modal no WhatsApp
   ↓
5. Usuário vê Teo Intelligence Concierge
   ↓
6. Escolhe uma das 4 opções (1, 2, 3, 👤)
   ↓
7. N8N roteia para workflow apropriado
   ↓
8. Supabase registra interação
```

---

## 📝 Próximos Passos

- [ ] Testar envio para bot fenice-tim (5521967531414)
- [ ] Ativar workflow no N8N Cloud
- [ ] Adicionar analytics dashboard
- [ ] Integrar com formulário de leads
- [ ] A/B testing de textos/emojis
- [ ] Suporte a imagens (screenshot do modal)

---

**Data:** 2026-06-30  
**Versão:** 1.0  
**Mantido por:** Ramão Bueno (Tech Lead)  
**Status:** ✅ Pronto para Produção

© 2026 Fenice IT · Justech.IA

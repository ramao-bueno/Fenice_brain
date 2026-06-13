# Workflow: WhatsApp → Pré-Cadastro por E-mail

## 📋 Fluxo do Sistema

```
Cliente (WhatsApp)
    ↓
Webhook (recebe nome + email)
    ↓
Validação (email válido? nome preenchido?)
    ↓
HTTP Request → AvisaAPI
    ↓
Envio de E-mail (pré-cadastro)
    ↓
Resposta ao Cliente ✅
```

---

## 🔧 Componentes do Workflow no n8n

### 1️⃣ WEBHOOK (Trigger)
- **Nome**: Webhook Pré-Cadastro
- **HTTP Method**: POST
- **Path**: `/webhook/pre-cadastro`
- **URL Final**: `https://feniceit.app.n8n.cloud/webhook/pre-cadastro`
- **Autenticação**: Nenhuma (por enquanto)

**Dados esperados**:
```json
{
  "nome": "Ramão Bueno da Silva",
  "email": "ramao@example.com",
  "telefone": "+5511999999999"  // opcional
}
```

---

### 2️⃣ VALIDAÇÃO (IF Condition)
**Validar**:
- ✓ `nome` não está vazio
- ✓ `email` tem formato válido (regex: `^[^\s@]+@[^\s@]+\.[^\s@]+$`)

**Se inválido**: Retorna erro 400

---

### 3️⃣ HTTP REQUEST → AvisaAPI
- **URL**: `https://www.avisaapi.com.br/api/[endpoint]`
- **Método**: POST
- **Headers**:
  - `Content-Type: application/json`
  - `Authorization: Bearer {{SEU_TOKEN}}` (se necessário)

**Body** (ajustar conforme documentação da API):
```json
{
  "nome": "{{ $node.Webhook.json.nome }}",
  "email": "{{ $node.Webhook.json.email }}",
  "telefone": "{{ $node.Webhook.json.telefone }}"
}
```

---

### 4️⃣ ENVIO DE E-MAIL
**Nó**: Send Email (Gmail ou SMTP)

**Para**: `{{ $node.Webhook.json.email }}`

**Assunto**: ✅ Seu Pré-Cadastro Realizado!

**Body**:
```
Olá {{ $node.Webhook.json.nome }},

Bem-vindo! Recebemos seu pré-cadastro com sucesso.

📋 Dados Registrados:
• Nome: {{ $node.Webhook.json.nome }}
• E-mail: {{ $node.Webhook.json.email }}

🔗 Próximo Passo:
Clique no link abaixo para completar seu cadastro:
https://feniceia.br/cadastro?token={{unique_token}}

O link expira em 7 dias.

Dúvidas? Responda este e-mail.

Atenciosamente,
Time Feniceia
```

---

### 5️⃣ RESPOSTA AO CLIENTE
**Retorna**:
```json
{
  "status": "sucesso",
  "mensagem": "E-mail de pré-cadastro enviado com sucesso!",
  "codigo": 200
}
```

---

## 🎯 Como Usar

### Via Webhook (POST)
```bash
curl -X POST https://feniceit.app.n8n.cloud/webhook/pre-cadastro \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Ramão Bueno da Silva",
    "email": "ramao@example.com",
    "telefone": "+5511999999999"
  }'
```

### Via WhatsApp Bot
Integrar com bot WhatsApp que extrai mensagens e envia para o webhook.

---

## ✅ Vantagens

- ✓ Automático 24/7
- ✓ Sem erros manuais
- ✓ E-mail instantâneo
- ✓ Validação de dados
- ✓ Escalável
- ✓ Rastreável (logs n8n)

---

## 📊 Exemplo de Dados

**Input** (do webhook):
```json
{
  "nome": "Ramão Bueno da Silva",
  "email": "ramao@example.com",
  "telefone": "+5511999999999"
}
```

**Output** (resposta):
```json
{
  "status": "sucesso",
  "mensagem": "E-mail de pré-cadastro enviado com sucesso!",
  "codigo": 200,
  "email_enviado_para": "ramao@example.com",
  "timestamp": "2026-06-11T14:30:00Z"
}
```

---

## 🚀 Próximas Ações

1. **Confirmar dados da AvisaAPI**:
   - Endpoint específico para este caso
   - Token/API Key necessário
   - Formato exato de dados esperados

2. **Configurar e-mail**:
   - Gmail com App Password
   - Ou SMTP customizado

3. **Conectar WhatsApp**:
   - Bot do WhatsApp
   - Webhook para receber mensagens

4. **Testar workflow** no n8n

---

**Criado em**: 2026-06-11  
**Projeto**: Fenice IA - Pré-Cadastro Automático

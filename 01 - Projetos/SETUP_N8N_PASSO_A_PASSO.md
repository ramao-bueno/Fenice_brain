# Setup Completo: Workflow n8n WhatsApp → Pré-Cadastro

## 🎯 Meta Final
Cliente envia via WhatsApp → Sistema recebe → Processa → Envia e-mail ✅

---

## 🔧 PASSO 1: Criar Novo Workflow no n8n Cloud

1. Acesse: https://feniceit.app.n8n.cloud/home/workflows
2. Clique em **"+ New Workflow"** (ou "Create Workflow")
3. Nome: **"Pré-Cadastro WhatsApp"**
4. Clique em **"Create"**

---

## 📥 PASSO 2: Adicionar Webhook (Trigger)

1. Na tela de edição, procure por **"Add a trigger..."**
2. Procure: **"Webhook"**
3. Selecione **"Webhook"**
4. Configure:
   - **HTTP Method**: POST
   - **Path**: `/pre-cadastro`
   - **Authentication**: None
5. Clique em **"Save"**

✅ Você receberá a URL:
```
https://feniceit.app.n8n.cloud/webhook/pre-cadastro
```

---

## ✅ PASSO 3: Adicionar Validação (IF Condition)

1. Clique no **"+"** no canvas (depois do Webhook)
2. Procure por: **"If"** ou **"Condition"**
3. Selecione **"If"**
4. Configure:
   ```
   CONDITION:
   - Field: email
   - Condition: Matches Regex
   - Pattern: ^[^\s@]+@[^\s@]+\.[^\s@]+$
   
   AND
   
   - Field: nome
   - Condition: Is not empty
   ```
5. Clique em **"Save"**

---

## 🔗 PASSO 4: Adicionar HTTP Request (AvisaAPI)

1. Clique no **"+"** (branch "true" da condição)
2. Procure por: **"HTTP Request"**
3. Selecione **"HTTP Request"**
4. Configure:
   - **URL**: `https://www.avisaapi.com.br/api/send`
   - **Method**: POST
   - **Headers**:
     ```
     Content-Type: application/json
     ```
   - **Body** (modo "JSON"):
     ```json
     {
       "nome": "{{ $node.Webhook.json.nome }}",
       "email": "{{ $node.Webhook.json.email }}",
       "telefone": "{{ $node.Webhook.json.telefone }}"
     }
     ```
5. Clique em **"Save"**

⚠️ **Nota**: Substitua `/send` pelo endpoint correto conforme a documentação da API

---

## 📧 PASSO 5: Adicionar Envio de E-mail

1. Clique no **"+"** (depois do HTTP Request)
2. Procure por: **"Send Email"** ou **"Gmail"** ou **"SMTP"**
3. Selecione conforme você tiver:
   - **Gmail** (mais fácil)
   - **SMTP** (se tiver servidor próprio)

### Se escolher Gmail:
4. Configure:
   - **Email Account**: (clique em "Connect" e autentique com Gmail)
   - **To Email**: `{{ $node.Webhook.json.email }}`
   - **Subject**: `✅ Seu Pré-Cadastro Realizado!`
   - **HTML**:
     ```html
     <p>Olá {{ $node.Webhook.json.nome }},</p>
     
     <p>Bem-vindo! Recebemos seu pré-cadastro com sucesso.</p>
     
     <h3>📋 Dados Registrados:</h3>
     <ul>
       <li>Nome: {{ $node.Webhook.json.nome }}</li>
       <li>E-mail: {{ $node.Webhook.json.email }}</li>
     </ul>
     
     <h3>🔗 Próximo Passo:</h3>
     <p>Clique no link para completar seu cadastro:</p>
     <p><a href="https://feniceia.br/cadastro">COMPLETAR CADASTRO</a></p>
     
     <p>Dúvidas? Responda este e-mail.</p>
     
     <p>Atenciosamente,<br>Time Feniceia</p>
     ```
5. Clique em **"Save"**

---

## ✨ PASSO 6: Adicionar Resposta (Opcional)

1. Clique no **"+"** (depois do e-mail)
2. Procure por: **"Respond to Webhook"**
3. Selecione
4. Configure **Body**:
   ```json
   {
     "status": "sucesso",
     "mensagem": "E-mail de pré-cadastro enviado com sucesso!",
     "email": "{{ $node.Webhook.json.email }}"
   }
   ```
5. Clique em **"Save"**

---

## 🧪 PASSO 7: Testar o Workflow

1. Clique em **"Test the Workflow"** ou botão de Play (▶️)
2. Você verá a tela de teste do Webhook
3. No **Body**, digite:
   ```json
   {
     "nome": "Ramão Bueno da Silva",
     "email": "seu-email@example.com",
     "telefone": "+5511999999999"
   }
   ```
4. Clique em **"Send"**
5. Veja o resultado em cada nó (verde = sucesso, vermelho = erro)

---

## 💾 PASSO 8: Salvar e Ativar

1. Clique em **"Save"** (Ctrl+S)
2. Clique em **"Activate"** (botão azul no topo)
3. ✅ Seu workflow está ATIVO!

---

## 🔗 URL do Webhook

Depois de ativado, você usa:
```
https://feniceit.app.n8n.cloud/webhook/pre-cadastro
```

**Enviar dados**:
```bash
curl -X POST https://feniceit.app.n8n.cloud/webhook/pre-cadastro \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Seu Nome",
    "email": "seu@email.com",
    "telefone": "+55119999999"
  }'
```

---

## 📊 O que Acontece Automaticamente

1. ✅ Webhook recebe dados
2. ✅ Valida email e nome
3. ✅ Envia para AvisaAPI
4. ✅ Envia e-mail de pré-cadastro
5. ✅ Retorna confirmação

**Tudo em segundos!** ⚡

---

## ⚠️ Se Algo Der Erro

- **"Email invalid"**: Ajuste a regex de validação
- **"API Error"**: Verifique o endpoint `/send` (pode ser `/notify`, `/register`, etc.)
- **"Email não enviou"**: Confirme autenticação do Gmail

---

## 🚀 Próximos Passos

1. Execute os 8 passos acima no n8n
2. Teste com o curl acima
3. Me avise como ficou!
4. Ajustamos conforme necessário

---

**Pronto para começar?** 🎯

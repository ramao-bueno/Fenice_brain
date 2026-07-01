# SP-1 · Runbook de Deploy (Tarefa 10 — manual, Ramão)

Branch: `sp1-atendimento-wow` · Arquivos: `scripts/n8n_fenice_tim_v4.json`, `scripts/n8n_fenice_leads.json`, `scripts/importar_carteira.py`

> Execute na ordem. As etapas 1-2 são pré-requisitos; 3-5 são o deploy; 6 é validação; 7 é a carteira Farmer.

---

## 1. Pré-requisito Azure (para o e-mail WOW funcionar)

O e-mail agora usa Microsoft Graph API. Sem isto, o nó falha silenciosamente (`continueOnFail`), mas o WhatsApp segue.

- [ ] No Azure/Entra ID: criar um **app registration**
- [ ] Conceder permissão de **aplicação** `Mail.Send` (NÃO delegated) + **admin consent**
- [ ] Escopo do envio: `fenice_tech@fenice.ia.br`
- [ ] No N8N: criar credential chamada **"Graph Mail"** (OAuth2 client-credentials — client_id, client_secret, tenant_id; scope `https://graph.microsoft.com/.default`)

## 2. Backup dos workflows atuais (N8N)

- [ ] `feniceit.app.n8n.cloud` → abrir "Fenice_Tim — WhatsApp IVR v4" → Export → salvar `n8n_fenice_tim_v4_backup_2026-06-30.json`
- [ ] Repetir para "fenice-leads"

## 3. Importar os workflows atualizados

- [ ] Importar `scripts/n8n_fenice_tim_v4.json` (Overwrite)
- [ ] Importar `scripts/n8n_fenice_leads.json` (Overwrite)
- [ ] No fenice-leads, associar o nó 5b à credential "Graph Mail"

## 4. Ativar

- [ ] Ativar ambos os workflows (toggle "Active")

## 5. Verificar credenciais dos nós

- [ ] Gemini AI Studio (nó 11 do tim-v4) ativa
- [ ] Graph Mail (nó 5b do leads) ativa

## 6. Testes de Aceitação (via WhatsApp para 5547991041414)

- [ ] "oi" → menu 6 opções
- [ ] "5" → boas-vindas Consultoria Jurídica
- [ ] pergunta jurídica → RAG + Gemini respondem com contexto
- [ ] inativo >60min → "Por falta de interação estamos encerrando… digite retomar"
- [ ] "retomar" → volta ao Gemini SEM reenviar menu
- [ ] "sair" → volta ao menu
- [ ] "quanto custa o plano?" → handoff automático (auto-intenção) ao Ramão
- [ ] "0" → handoff manual com contexto de 7 elementos
- [ ] formulário em fenice.ia.br → e-mail (Graph) + WhatsApp WOW em <60s
- [ ] Ramão recebe notificação de lead em 5547991041414
- [ ] handoff traz: nome, whatsapp, email, assunto, intenção, resumo, próximo passo

## 7. Import da carteira Farmer

- [ ] Preparar `carteira.csv` com colunas: `nome,telefone,email,assunto`
- [ ] Definir env: `SUPABASE_URL`, `SUPABASE_SERVICE_KEY`
- [ ] Rodar: `cd scripts && python importar_carteira.py carteira.csv`
- [ ] Conferir no Supabase: contatos entraram como `estagio = pos_venda`

---

## Notas / pendências conhecidas (do review)

- Nós de imagem `9a-img0/1/2/3` no `data.nodes` são vestígio do experimento de 4 opções (menu agora é texto). Ver veredicto do review final antes de remover.
- apikey Evolution em texto plano nos nós (padrão herdado). Migrar para credential do N8N no futuro.
- Após validar em produção: `git checkout main && git merge sp1-atendimento-wow` (ou PR), depois atualizar `system-estado-atual.md`.

---

*بِسْمِ اللهِ الرَّحْمَنِ الرَّحِيمِ · Fenice IT · Justech.IA*

---
titulo: Infraestrutura de Atendimento ao Cliente — Fenice IT
versao: 1.0-draft
data: 2026-06-28
status: draft — aguardando revisão Ramão
tags:
  - infra
  - atendimento
  - evolution
  - n8n
  - fluxograma
---

# Infraestrutura de Atendimento — Fenice IT

> [!WARNING] STATUS
> Rascunho gerado em 2026-06-28 com base na análise do workflow N8N `UKfz7lxQTQcnbOMV` e memórias do projeto. Aguarda revisão e aprovação de Ramão antes de qualquer implementação.

---

## 1. Canais de Entrada

```
┌─────────────────────────────────────────────────────────────────┐
│                     CANAIS DE ENTRADA                           │
│                                                                 │
│   📱 WhatsApp                    🌐 Site fenice.ia.br           │
│   (5547991041414)                (formulário /contato)          │
│         │                                │                      │
│         ▼                                ▼                      │
│   Evolution API              POST /leads (FastAPI)              │
│   (Hostinger VPS)            api_fenice_saas.py                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Canal WhatsApp — Fluxo Atual (✅ EM PRODUÇÃO)

```
[Cliente envia mensagem no WhatsApp]
            │
            ▼
  Evolution API (instância fenice-tim)
  URL: evolution-api-9fbw.srv1784289.hstgr.cloud
            │  webhook POST
            ▼
  N8N Cloud — Workflow v4 (feniceit.app.n8n.cloud/webhook/fenice-tim)
            │
  ┌─────────▼──────────┐
  │ Nó 2: Normalizar   │  extrai numero, nome, mensagem, fromMe*
  └─────────┬──────────┘  *fork evolution_hostinger: TUDO fromMe=true → não filtrar
            │
  ┌─────────▼──────────┐
  │ Nó 3: Válida?      │──── NÃO (_skip=true) ──► [IGNORAR]
  └─────────┬──────────┘
            │ SIM
  ┌─────────▼──────────┐
  │ Nó 4: É PARAR?     │──── SIM ──► Enviar MSG opt-out + Salvar Supabase
  └─────────┬──────────┘
            │ NÃO
  ┌─────────▼──────────────────────┐
  │ Nó 6: Buscar contato Supabase  │  tabela fenice_tim_contatos
  └─────────┬──────────────────────┘  campos: area, estagio, menu_ativo
            │
  ┌─────────▼──────────────────────┐
  │ Nó 7: Decidir Próxima Ação     │
  │                                │
  │  isReset? ──────────────────── │──► acao = menu_principal
  │  opcaoMenu (1-6,0) escolhida?  │──► acao = set_area  (ou humano se 0)
  │  sem area salva?               │──► acao = menu_principal
  │  tem area, sem nova escolha?   │──► acao = responder
  └─────────┬──────────────────────┘
            │
  ┌─────────▼──────────────────────┐
  │ Nó 8: Switch por Ação          │
  └───┬────────┬────────┬──────────┘
      │        │        │
      ▼        ▼        ▼
  MENU      HUMANO   RESPONDER
  9-logo    9b msg   10. Prompt por Área
  9a menu          │
                   ├── área 1: B2B (escritórios/empresas)
                   ├── área 2: Acadêmico (TCC, graduação)
                   ├── área 3: Observatório (projeto social)
                   ├── área 4: API (desenvolvedores)
                   └── área 5: Jurídico (atendimento individual)
                           │
                   10b. Debounce 6s
                           │
                   11. Groq llama-3.3-70b
                           │
                   12. Extrair resposta
                           │
                   13. Evolution API → envia resposta ao cliente
                           │
                   14-15-16. Log Supabase
                           (interacoes_whatsapp + fenice_tim_contatos)
```

### Estágios do Contato (fenice_tim_contatos.estagio)

```
prospect ──► atendimento ──► pos_venda
   │               │               │
Hunter (ativo)  Farmer         Retenção
novo lead       base atual     fidelização
```

---

## 3. Canal Site — Fluxo Atual (⚠️ PARCIALMENTE IMPLEMENTADO)

```
[Cliente preenche formulário em fenice.ia.br/contato]
  campos: nome, e-mail, empresa (opcional), interesse
            │
            ▼
  POST /leads  (api_fenice_saas.py)
  validação: e-mail regex
            │
  ┌─────────▼──────────────────────┐
  │ Salva em fenice_tim_contatos   │ ✅ FUNCIONANDO
  │ estagio: "lead_site"           │
  │ numero: "email:[email]"        │
  └─────────┬──────────────────────┘
            │
  asyncio.create_task(_notificar_lead)  ← background
            │
  ┌─────────┴──────────────────────────┐
  │                                    │
  ▼                                    ▼
E-mail admin                   POST N8N_WEBHOOK_URL
fenice_tech@fenice.ia.br...   feniceit.app.n8n.cloud/webhook/fenice-tim-v2
smtp.office365.com:587         payload: { evento:"novo_lead", ... }
⚠️ FALTA: SMTP_PASS            ❌ NÃO EXISTE nó no N8N p/ novo_lead
  │
  ▼
E-mail confirmação
ao prospect
⚠️ FALTA: SMTP_PASS
```

---

## 4. GAPs — O Que Falta Construir

### GAP 1 — Notificação do Admin (ALTA PRIORIDADE)
> Quando chega lead pelo site, o Ramão não recebe nenhum aviso.

**Opções:**
- A) E-mail via Outlook (código pronto — falta `SMTP_PASS`)
- B) WhatsApp via Evolution (falta nó no N8N ou chamada direta à Evolution API)
- C) Ambos

**Decisão pendente:** qual canal de notificação imediata ao admin?

---

### GAP 2 — Unificação dos Leads (MÉDIA PRIORIDADE)
> Lead que chega pelo site e lead que chega pelo WhatsApp estão no mesmo Supabase (`fenice_tim_contatos`) mas seguem caminhos distintos. Não há uma view unificada de CRM.

**Sugestão:** criar view `v_pipeline_leads` no Supabase com todos os contatos + canal de origem + estágio + último contato.

---

### GAP 3 — Handoff Humano (MÉDIA PRIORIDADE)
> O nó 9b "Enviar MSG Humano" existe no N8N mas não há processo definido de como o atendente humano assume a conversa, nem fila de atendimento.

**Questões abertas:**
- Quem é o atendente humano?
- Canal de notificação para ele (WhatsApp, e-mail, painel)?
- Como sinaliza que assumiu? (para o bot parar de responder)

---

### GAP 4 — E-mail Inbound (BAIXA PRIORIDADE por ora)
> Clientes que enviam e-mail para `fenice_tech@fenice.ia.br.onmicrosoft.com` não são processados automaticamente.

**Sugestão futura:** webhook Office365 → N8N → mesmo IVR.

---

### GAP 5 — Workflow N8N para Leads do Site (ALTA PRIORIDADE)
> O workflow atual só processa WhatsApp inbound. Não existe trigger para `evento:"novo_lead"`.

**Opções:**
- A) Adicionar novo trigger (webhook) no mesmo workflow v4
- B) Criar workflow separado `fenice-leads` no N8N
- C) Notificar via Evolution API diretamente (sem N8N)

---

## 5. Fluxo Ideal Proposto (pós-implementação)

```
┌─────────────────────────────────────────────────────────────────┐
│               ATENDIMENTO UNIFICADO — FENICE IT                 │
└─────────────────────────────────────────────────────────────────┘

  📱 WhatsApp          🌐 Site              📧 E-mail (futuro)
  (Evolution)          (formulário)         (Office365)
       │                    │                    │
       ▼                    ▼                    ▼
  N8N webhook          POST /leads          Webhook O365
  fenice-tim           FastAPI              → N8N (futuro)
       │                    │
       │              ┌─────┴──────────────────────┐
       │              │  Salva fenice_tim_contatos  │
       │              │  estagio: lead_site         │
       │              └─────┬──────────────────────┘
       │                    │
       │              ┌─────┴──────────────────────┐
       │              │  Notifica Admin             │
       │              │  - E-mail Outlook           │
       │              │  - WhatsApp pessoal Ramão   │
       │              └─────┬──────────────────────┘
       │                    │
       └─────────┬──────────┘
                 ▼
    ┌────────────────────────────┐
    │   fenice_tim_contatos      │
    │   CRM unificado Supabase   │
    │   canal: whatsapp | site   │
    │   estagio: prospect        │
    └────────────┬───────────────┘
                 │
    ┌────────────▼───────────────┐
    │   Roteamento por Área      │
    │   1-B2B 2-Acad 3-Obs       │
    │   4-API 5-Jurídico 0-Human │
    └────────────┬───────────────┘
                 │
    ┌────────────▼───────────────┐
    │   IA Fenice Tim (Groq)     │
    │   llama-3.3-70b            │
    │   contexto por área        │
    └────────────┬───────────────┘
                 │
         ┌───────┴────────┐
         ▼                ▼
    Resposta IA      Handoff Humano
    Evolution API    (notifica atendente)
    auto             manual
         │
         ▼
    Log Supabase
    (interacoes_whatsapp)
         │
         ▼
    Pipeline Comercial
    prospect → atendimento → pos_venda
    Hunter (novos) | Farmer (base)
```

---

## 6. Próximos Passos (ordenados por prioridade)

| # | Ação | Dependência | Esforço |
|---|---|---|---|
| 1 | Definir canal de notificação ao admin (e-mail / WhatsApp) | Decisão Ramão | — |
| 2 | Fornecer `SMTP_PASS` (se e-mail) | Ramão | 5 min |
| 3 | Criar workflow N8N `fenice-leads` OU trigger novo no v4 | GAP 1 resolvido | 1h |
| 4 | Criar view `v_pipeline_leads` no Supabase | — | 30 min |
| 5 | Definir processo de handoff humano | Decisão Ramão | — |
| 6 | E-mail inbound (futuro) | Pós-lançamento | — |

---

*Gerado por análise do N8N workflow `UKfz7lxQTQcnbOMV` + memórias do projeto Fenice IT.*
*Ramão: revise, anote suas decisões nos GAPs e devolvemos para implementação.*

# SP-1 · Motor de Atendimento WOW — Design Spec

**Data:** 2026-06-30
**Status:** Aprovado (aguardando revisão final do spec)
**Autor:** Ramão Bueno + Claude
**Roadmap:** ver [2026-06-30-fenice-roadmap-macro.md](2026-06-30-fenice-roadmap-macro.md)

---

## Visão Geral

Motor de atendimento que recebe um **visitante desconhecido**, entrega uma
**experiência WOW** (Nubank + Zappos) e o converte em **prospect quente**
entregue ao Ramão para "subir BKO". A cobrança e a burocracia formal
(CPF, cadastro, ativação) são responsabilidade da **operadora TIM, nossa
representada** — o motor NÃO trata disso.

**Goal:** de visitante anônimo a prospect quente com histórico, pronto para
o Ramão submeter à TIM.

**Relação Hunter/Farmer:** o bot é o **Hunter** (capta prospects novos). A
base **Farmer** (carteira atual do Ramão) é importada para o mesmo BD.

---

## Fronteira do Subprojeto

- **SP-1 entrega:** prospect quente (4 campos + histórico) + notificação ao Ramão.
- **Fora do SP-1:** subir BKO, CPF/cadastro formal, pós-venda, Farmer CRM (SP-3);
  cobrança (100% TIM); relatórios Salesforce/Power BI (SP-3 futuro).

---

## Arquitetura do Funil

```
VISITANTE DESCONHECIDO
   │  entra por WhatsApp (Evolution)  ou  formulário fenice.ia.br
   ▼
MOTOR N8N fenice-tim-v4
   1. Normaliza + filtra eco (BOT_SIGS)
   2. Busca contato (Supabase fenice_tim_contatos)
   3. Decide ação:
      • novo/sem área      → MENU (6 opções)
      • escolheu área      → boas-vindas + entra na área
      • em atendimento     → RAG → Gemini → responde
      • inativo >60min     → encerra + "digite retomar"
      • "retomar"          → volta direto ao Gemini (sem menu)
      • "sair"             → volta ao menu
      • opção 0            → HANDOFF Ramão
      • AUTO-INTENÇÃO      → HANDOFF Ramão (proativo)
   ▼
LEAD CAPTURADO → dispara WOW (workflow fenice-leads)
      ├─ Gemini gera insight
      ├─ E-mail (Graph API) ao visitante
      ├─ WhatsApp proativo ao visitante
      └─ Notifica Ramão (5547991041414)
   ▼
HANDOFF → Ramão recebe prospect quente + histórico → sobe BKO na TIM
```

---

## Menu — 6 Opções (decidido)

`1=B2B` · `2=Acadêmico` · `3=Observatório` · `4=API` · `5=Jurídico` · `6=Filosofia` · `0=Humano`

Cada área tem um `SYSTEM_PROMPT` dedicado (já existem no nó 10 do workflow).
TIM não é opção de menu — é o destino do funil (conversão).

---

## Modelo de Dados

**BD:** `fenice_tim_contatos` (Supabase). Alimentado por duas fontes:

| Fonte | Entrada | Estágio inicial |
|-------|---------|-----------------|
| Carteira atual (Farmer) | import em lote | `pos_venda` |
| Prospecções (Hunter) | bot WhatsApp / formulário | `prospect` |

**Campos capturados pelo bot (apenas 4):**
- `nome` (pushName ou informado)
- `telefone` (numero, formato `55DDD9XXXXXXXX`)
- `email` (em `dados.email`)
- `assunto` (`area` — uma das 6 opções)

**Nunca capturar:** CPF, endereço, dados de cadastro formal → CRM TIM legado (LGPD).

**Estágios:** `prospect → atendimento → pos_venda` (+ `inativo`, `aguardando_cadastro`).

---

## Componentes Novos / Alterados

### 1. E-mail WOW via Microsoft Graph API
- Substitui o nó SMTP placeholder (`{{SMTP_CREDENTIAL_ID}}`).
- Endpoint: `POST https://graph.microsoft.com/v1.0/users/fenice_tech@fenice.ia.br/sendMail`
- Auth: OAuth client credentials (app registration Azure com permissão `Mail.Send`).
- Dispara no workflow `fenice-leads` após o insight do Gemini.
- `continueOnFail: true` — se o e-mail falhar, WhatsApp e notificação seguem.

### 2. Auto-detecção de Intenção
- No nó de decisão (ou pós-Gemini), detecta sinais na mensagem do usuário.
- **Sinais:** `quanto custa`, `preço`, `valor`, `plano`, `quero contratar`,
  `como assino`, `fechar`, `falar com humano`, `atendente`, `pessoa`.
- Ao detectar → `_acao = 'humano'` (handoff proativo ao Ramão).
- Complementa (não substitui) a opção 0 manual.

### 3. Retomada / Inatividade
- **Timeout:** 60 minutos sem interação (`estagio='atendimento'`).
- Ao expirar → envia encerramento "Por falta de interação estamos encerrando…
  Caso queira retomar, digite: *retomar*" + marca `estagio='inativo'`.
- **"retomar"** (estagio='inativo') → `_acao='responder'` → volta direto ao
  Gemini na mesma área, SEM reenviar menu (WOW: não encher a tela).
- **"sair"** → `_acao='menu_principal'` (volta ao menu, não é opt-out).

### 4. Handoff ao Ramão (modelo de 7 elementos — Salesforce/Alhena)
- Gatilhos: opção 0 OU auto-intenção.
- **Transferência de contexto rica** (não só 4 campos) — o handoff carrega:
  1. Transcrição da conversa
  2. Resumo gerado por IA (Gemini)
  3. Intenção detectada
  4. Área/assunto (categoria)
  5. Sentimento/nível de interesse
  6. Dados do prospect (nome, telefone, email)
  7. Próximo passo sugerido ("subir BKO plano X")
- Enviado ao Ramão (`5547991041414`). Objetivo: Ramão assume "a par de tudo",
  sem o prospect repetir contexto.
- Nota técnica: admin = mesmo número do bot → cai no self-chat; BOT_SIGS bloqueia eco.

### 5. Correção do Número Admin
- Todas as notificações → `5547991041414` (corporativo).
- Remover qualquer referência a `554797348385` (não existe).

---

## O Que Permanece Igual

Menu 6 opções · RAG antes do Gemini (`buscar_legislacao`) · filtro BOT_SIGS ·
debounce 6s · typing indicator · logs Supabase (`interacoes_whatsapp`) ·
deploy N8N manual (import) · deploy site auto (push `fenice-justech`).

---

## Tratamento de Erros

| Falha | Comportamento |
|-------|---------------|
| Gemini timeout/erro | mensagem fallback + `contato@fenice.ia.br` |
| E-mail Graph falha | `continueOnFail` — WhatsApp segue |
| RAG (`buscar_legislacao`) falha | segue sem contexto RAG (try/catch silencioso) |
| Supabase lookup falha | trata como contato novo (contatos=[]) |
| Número inválido no handoff | log + notifica Ramão do erro |

---

## Testes de Aceitação

1. Visitante envia "oi" → recebe menu 6 opções.
2. Escolhe "5" (Jurídico) → boas-vindas Jurídico + pode perguntar.
3. Pergunta jurídica → RAG + Gemini respondem com contexto.
4. Fica inativo >60min → recebe encerramento com "digite retomar".
5. Digita "retomar" → volta ao Gemini SEM menu.
6. Digita "sair" → volta ao menu.
7. Digita "quanto custa o plano?" → auto-intenção → handoff ao Ramão.
8. Digita "0" → handoff manual ao Ramão com histórico.
9. Preenche formulário site → recebe e-mail (Graph) + WhatsApp WOW em <60s.
10. Ramão recebe notificação de lead em `5547991041414`.
11. Import da carteira → contatos entram como `pos_venda` (Farmer).

---

## Boas Práticas de Classe Mundial (pesquisa — grandes players)

Incorporadas de fontes livres para elevar o SP-1 a padrão mundial:

| Prática | Fonte | Aplicação no SP-1 |
|---------|-------|-------------------|
| 73% dos consumidores preferem mensagem; 72% compram mais de quem oferece messaging | Infobip / WhatsApp | Valida WhatsApp como canal principal do funil |
| Conversas de atendimento são **grátis**; templates utility grátis em janela 24h | Meta/WhatsApp 2025 | Custo do funil ~zero; usar template só fora da janela |
| Responder rápido, **sem repetir contexto** | WhatsApp/Infobip | Retomada volta direto ao Gemini (já no desenho) |
| Botões / quick replies para self-service | Meta/Vonage | **Upgrade futuro:** menu por botões (se Evolution suportar) em vez de texto numerado |
| WOW = proativo **+** reativo | Zappos/Forbes | Auto-intenção = proatividade (já no desenho) |
| **75% dos pedidos vêm de clientes existentes** | Zappos | Valida foco Farmer — nutrir a carteira, não só caçar |
| Intent por NLP, não keyword rígido | IrisAgent/Salesforce | **Upgrade:** V1 keywords; V2 usa Gemini p/ pontuar intenção nuançada |
| Handoff ótimo: 3-5 trocas após sinal de compra | Alhena/BlueTweak | Não escalar cedo demais nem tarde; disparar no sinal |
| Handoff carrega 7 elementos de contexto | Salesforce/Alhena | Adotado no componente #4 (transferência rica) |
| Consentimento/opt-in explícito | WhatsApp/LGPD | Opt-out "parar" já existe; manter |

**Roadmap de melhoria contínua (kaizen):** keywords → intenção por Gemini (V2);
texto numerado → botões interativos (V2); handoff simples → contexto de 7
elementos (V1 já adota).

## Fora de Escopo (explícito)

- Billing / cobrança → 100% TIM.
- CPF, cadastro formal, subir BKO → Ramão + CRM TIM legado (SP-3).
- CRM Salesforce + relatórios Power BI → SP-3 futuro.
- Sync automático Obsidian→Supabase → SP-2.

---

*بِسْمِ اللهِ الرَّحْمَنِ الرَّحِيمِ*
*Fenice IT · Justech.IA — Filosofia e Direito, Sabedoria e Justiça*

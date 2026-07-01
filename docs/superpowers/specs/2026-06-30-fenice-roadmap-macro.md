# Fenice — Roadmap Macro (Índice de Subprojetos)

**Data:** 2026-06-30
**Status:** Organização aprovada — cada subprojeto terá seu próprio ciclo spec → plano → implementação
**Autor:** Ramão Bueno + Claude

---

## Visão

Projeto Fenice: **dois pilares** convergindo para **monetização via operadora TIM**.

- **Pilar 1 — Sistema Acadêmico Jurídico-Filosófico** ("o maior do universo")
- **Pilar 2 — Atendimento WOW** a público desconhecido → cliente TIM

TIM monetiza o projeto como um todo. Cada visitante convertido alimenta a receita.

---

## Decomposição em Subprojetos

Nenhum destes cabe num único spec. Cada um entrega software funcional e testável por si só.

### SP-1 · Motor de Atendimento WOW
- **O quê:** funil de conversão — visitante desconhecido → experiência WOW → cliente TIM
- **Stack:** N8N (fenice-tim-v4 + fenice-leads) + Evolution API + Gemini + RAG Supabase
- **Estado:** ~80% pronto; bugs a fechar (retomada/inatividade, e-mail WOW, nº admin)
- **Entrega isolada:** bot que recebe, roteia por 6 áreas, responde com RAG, captura lead, dispara WOW

### SP-2 · Camada de Conhecimento
- **O quê:** alimenta o RAG que dá inteligência ao SP-1
- **Stack:** Obsidian (23k notas) → scripts de ingestão → Supabase (vetores + FTS)
- **Estado:** funcional; sync hoje é batch manual (a melhorar)
- **Entrega isolada:** pipeline que mantém o Supabase atualizado a partir do vault

### SP-3 · Pipeline Operacional (Hunter → BKO → Pós-venda → Farmer)
- **O quê:** a obrigação do Ramão na cadeia — NÃO é billing (TIM cobra)
- **Fluxo:** `prospect → subir BKO → pós-venda → tratar cliente Farmer`
- **Stack:** fenice_tim_contatos (estágios já existem) + submissão BKO à TIM
- **Estado:** estágios existem; submissão BKO + Farmer CRM a construir
- **Entrega isolada:** do lead quente (SP-1) até BKO submetido + pós-venda + Farmer
- ⚠️ **Cobrança é 100% da operadora TIM.** Nenhum billing é construído aqui.
- 🔮 **Futuro:** CRM estilo Salesforce (pipeline) + Power BI (relatórios). Pensar depois.

### SP-4 · Portais de Entrega
- **O quê:** onde o usuário chega e interage
- **Stack:** fenice.ia.br (FastAPI) + fenicejus (Quartz) + landing/formulário
- **Estado:** parcial
- **Entrega isolada:** páginas que disparam o funil SP-1 e expõem o conhecimento SP-2

---

## Relações e Dependências

```
SP-2 (conhecimento) ──alimenta──► SP-1 (atendimento) ──gera conversão──► SP-3 (receita TIM)
                                       ▲
SP-4 (portais) ──dispara/entrega──────┘
```

- SP-2 alimenta SP-1 (conhecimento → respostas do bot)
- SP-4 é a porta de entrada que dispara SP-1
- SP-3 monetiza o resultado de SP-1

---

## Ordem de Construção

1. **SP-1** — destravar o funil (coração do negócio, quase pronto)
2. **SP-3** — definir a monetização sobre o funil que converte
3. **SP-2 / SP-4** — melhorados em paralelo conforme necessário

Cada subprojeto: brainstorm → spec próprio → plano → implementação.

---

*بِسْمِ اللهِ الرَّحْمَنِ الرَّحِيمِ*
*Fenice IT · Justech.IA*

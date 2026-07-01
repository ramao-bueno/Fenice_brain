# SP-1 · Relatório de Performance — Agentes Fenice

**Plano:** docs/superpowers/plans/2026-06-30-sp1-atendimento-wow.md
**Branch:** sp1-atendimento-wow
**Início:** 2026-06-30
**Convenção:** cada tarefa é executada por um "Agente Fenice NN"

---

## Tabela de Execução

| Agente | Tarefa | Modelo | Status | Rodadas de review | Commits | Notas |
|--------|--------|--------|--------|-------------------|---------|-------|
| Fenice 01 | 1 — Lógica decisão + intenção | haiku | ✅ completa | 1 (Needs fixes → ok) | b2c3ba6a, 2ff4dd63 | 9/9 testes; +guarda não-texto |
| Fenice 02 | 2 — Testes de intenção | haiku | ✅ completa | 0 (controlador verificou) | 8fe19cb5 | 14/14 testes |
| Fenice 03 | 3 — Integração N8N (nós 2,7,8) | sonnet | ✅ completa | 1 (Crítico → ok) | 73dd9dd6, 47af2521 | Review pegou bug de índice do Switch |
| Fenice 04 | 4 — Nós inatividade + boas-vindas + fiação | sonnet | ✅ completa | 1 NEEDS_CONTEXT (decisão merge) | 5f417c8d | Invariantes verificados nas 2 cópias |
| Fenice 05 | 5 — Menu 6 opções (texto) | haiku | ✅ completa | 0 (controlador verificou) | 916da436 | 6 opções + sair nas 2 cópias |
| Fenice 06 | 6 — Handoff 7 elementos | sonnet | ✅ completa | 0 (controlador verificou) | e0d881db | Cadeia handoff nas 2 cópias |
| Fenice 07 | 7 — Número admin (fenice-leads) | haiku | ✅ completa | 0 (verificação trivial) | 01d6a6e6 | wrong num removido |
| Fenice 08 | 8 — E-mail Graph API | sonnet | ✅ completa | 0 (controlador verificou) | 967c7c89 | nó 5b→Graph; Azure Mail.Send pendente |
| Fenice 09 | 9 — Import carteira Farmer (Python) | haiku | ✅ completa | 0 (controlador rodou testes) | a95b53b6 | 4/4 pytest |
| Revisor Final | Review amplo do branch | opus | ✅ 1 Important + 1 falso-pos | — | — | pegou clobber de estágio |
| Correção Final | Fix Farmer cadastro_invite | sonnet | ✅ completa | — | 0aabf5b8 | 10/10 testes; A+B nas 2 cópias |
| — | 10 — Deploy + aceitação | — | 📋 manual (Ramão) | — | — | runbook preparado |

---

## Métricas Agregadas (final)

- **Tarefas de código: 9/9 concluídas** (Tarefa 10 = deploy manual do Ramão)
- **Agentes disparados:** 9 implementadores (Fenice 01-09) + 2 revisores por-tarefa (01, 03) + 1 revisor final (opus) + 1 correção final = **13 subagentes**
- **Aprovação sem correção de código:** 6/9 tarefas (2,5,6,7,8,9) — **~67% na 1ª tentativa**
- **Tarefas que exigiram uma rodada:** 3/9 (T1 guarda não-texto, T3 bug crítico de índice, T4 decisão merge)
- **Achados por severidade:**
  - 🔴 Crítico: 1 — roteamento do Switch por índice posicional (T3), pego antes do deploy
  - 🟠 Important: 2 — guarda `mensagem` não-texto (T1), convite indevido a Farmer (review final)
  - 🟡 Minor→backlog: 5 — nós img órfãos, secrets em claro, OAuth2 Graph, STOP_WORDS morto, scratch
- **Distribuição de modelos:** haiku (transcrição/testes: T1,T2,T5,T7,T9), sonnet (integração JSON: T3,T4,T6,T8 + correção), opus (review amplo)
- **Falso-positivo capturado pelo controlador:** 1 — "inatividade inalcançável" (o nó 14 grava estágio via jsCode; o grep do revisor não pegou)

### Valor demonstrado do processo
O review por-tarefa pegou um **bug crítico** (índice do Switch) que teria quebrado todo o roteamento em produção. O review amplo (opus) pegou um **bug de integração** (clobber de estágio → convite indevido a Farmer) invisível aos testes unitários. Ambos corrigidos antes de qualquer deploy. Kaizen: escrever → testar → melhorar.

## Backlog (Minors do review final)
1. Remover nós `9a-img0/1/2/3` órfãos de `data.nodes` (vestígio 4-opções)
2. Migrar apikey Evolution + JWT Supabase de texto plano para credentials do N8N
3. E-mail Graph: avaliar credential OAuth2 client-credentials própria (vs httpHeaderAuth)
4. Remover export morto `STOP_WORDS` de `decidir_acao.js`
5. Avaliar `set_area → Gemini` (possível dupla saudação: 16b boas-vindas + Gemini)

---

## Notas de Pré-voo

- **Duplicação intencional (Tarefa 1 → Tarefa 3):** a lógica `decidirAcao`/`detectarIntencao`
  é criada como módulo testável (Tarefa 1) e depois copiada inline nos nós Code do N8N
  (Tarefa 3), porque nós Code do N8N não importam módulos locais. Não é defeito — é
  restrição da plataforma. Módulo = fonte da verdade + testes; inline = deploy.

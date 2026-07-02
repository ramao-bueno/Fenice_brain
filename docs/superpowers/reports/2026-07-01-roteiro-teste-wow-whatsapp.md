# Roteiro de Teste — WOW Atendimento WhatsApp (Téo)

> **Objetivo:** validar toda a jornada do usuário no WhatsApp corporativo, com foco no
> **momento** (timeline da conversa) e na regra de ouro **JAMAIS perturbar o usuário**.
>
> **Como usar:** envie cada mensagem para o número do Téo pelo seu WhatsApp e confira a
> resposta + o timing. Marque `[x]` quando validar. Duração total: ~5 min (exceto inatividade).
>
> **Instância live:** `fenice-tim-prod` · **Timer de inatividade:** 60 min · **Encerrar:** `sair` ou `7`

---

## Regra de ouro — JAMAIS perturbar (guarda global)

Em TODA fase, verifique:
- 🚫 O Téo **nunca** manda mensagem sem o usuário ter falado primeiro (salvo o WhatsApp proativo de lead do site — que é 1 única mensagem).
- 🚫 O modal (card) **não** se repete a cada mensagem — só quando faz sentido (saudação, `menu`, `sair`).
- 🚫 Inatividade encerra com **1 única** mensagem; depois, **silêncio total** até o usuário digitar `retomar`.
- ✅ Antes de responder pergunta: **indicador de digitando** + resposta pensada (RAG antes do Gemini), nunca instantânea/robótica.
- ✅ Toda resposta carrega a assinatura WOW: `👤 *Teo — Intelligence Concierge*` / `© 2026 Fenice IT Justech.IA` e tratamento **Dr./Dra.**

---

## Timeline da conversa

### Fase 0 — Abertura / cumprimento  →  libera o modal
- ⏱️ **T0**
- 📲 Você envia: `bom dia` (repita depois com `oi` e `olá` — todos devem abrir o modal)
- 🤖 Téo responde: **card do modal** (imagem) + legenda:
  ```
  *Teo — Intelligence Concierge*
  Escolha um serviço e responda com o número (0 a 6).
  *7* ou *sair* para encerrar.
  🌐 https://www.fenice.ia.br
  ```
- ✅ Valida itens de aceite **#1** (menu abre no cumprimento).
- 🚫 Não‑perturbar: o card vem **1 vez**, não em duplicata.

### Fase 1 — Escolha da área (pelo número)
- ⏱️ **T0 + ~5s**
- 📲 Você envia: `2`  (Acadêmico)
- 🤖 Téo responde: boas‑vindas da área **Acadêmico** + assinatura WOW.
- ✅ Valida **#2** (boas‑vindas por área). Repita com `5` (Jurídico) em outra conversa.
- 🚫 Não‑perturbar: uma boas‑vindas só; sem reenviar o menu.

> ⚠️ **Ponto de atenção (a decidir):** se, em vez do número, você digitar a intenção em
> texto livre **antes** de escolher (ex.: `quero estudar penal`), o Téo hoje **reenvia o
> modal** em vez de rotear direto para Acadêmico. Teste isso: se o card se repetir, é
> candidato a melhoria (rotear por texto / nudge leve em vez de reenviar o card).

### Fase 2 — Pergunta e resposta (RAG + Gemini)
- ⏱️ **T0 + ~15s**
- 📲 Você envia (na área Jurídico, `5`): `o que diz o art. 5º da CF sobre igualdade?`
- 🤖 Téo: **digitando…** e depois resposta com contexto (RAG) + fecho WOW.
- ✅ Valida **#3** (RAG + Gemini com contexto).
- 🚫 Não‑perturbar: resposta única, sem "eco" nem mensagens extras. Tempo natural (não instantâneo, não eterno).

### Fase 3 — Continuidade + convite de cadastro no MOMENTO certo
- ⏱️ **T0 + ~40s** (2ª e 3ª perguntas seguidas)
- 📲 Envie mais 2 perguntas normais (totalizando 3 mensagens na área).
- 🤖 Na **3ª**, o Téo convida ao cadastro (só 1 vez):
  ```
  Dr(a). <nome>, percebo que nossa conversa tem sido produtiva! 🏛️
  Para um atendimento personalizado e prioritário, acesse: 🔗 fenice.ia.br
  ```
- ✅ Valida timing do convite (nem cedo demais, nem a cada msg).
- 🚫 Não‑perturbar: convite aparece **1 vez**; depois continua respondendo normal, sem repetir o convite.

### Fase 4 — Sair para o menu / `sair` e `7`
- ⏱️ **T0 + ~1min**
- 📲 Você envia: `menu`  → deve voltar ao modal.
- 📲 Você envia: `7` (ou `sair`) → deve **encerrar** o atendimento (não voltar ao menu).
- ✅ Valida **#6** (`sair` encerra) + a adição do `7` como encerramento.
- 🚫 Não‑perturbar: encerra limpo, sem insistir.

### Fase 5 — Inatividade (o teste do "momento" mais importante)
- ⏱️ **T0 + 60 min sem interação** (na área, estágio `atendimento`)
- 🤖 Téo envia **1 única** mensagem:
  ```
  ⏱️ Por falta de interação estamos encerrando o atendimento.
  Caso queira retomar a conversa, digite: retomar
  👤 Teo — Intelligence Concierge
  ```
- ✅ Valida **#4** (inatividade >60min encerra).
- 🚫 Não‑perturbar: **só 1** mensagem; depois **silêncio absoluto** — o Téo NÃO fica cutucando.
- 💡 *Teste acelerado (opcional):* posso baixar o timer de 60→2 min no workflow por 10 min só pra você ver, e reverter em seguida. Peça se quiser.

### Fase 6 — Retomar (volta sem reabrir o modal)
- ⏱️ logo após a inatividade
- 📲 Você envia: `retomar`
- 🤖 Téo: volta a responder no Gemini **sem reenviar o menu**.
- ✅ Valida **#5** (`retomar` sem menu).
- 🚫 Não‑perturbar: retoma direto no assunto, sem card, sem boas‑vindas repetidas.

### Fase 7 — Auto‑intenção → handoff proativo (WOW)
- 📲 Você envia (dentro de uma área): `quanto custa o plano?`
- 🤖 Téo: escala para **atendimento humano** (mensagem de humano) e notifica o Ramão.
- ✅ Valida **#7** (auto‑intenção → handoff). Gatilhos: `preço`, `valor`, `plano`, `quero contratar`, `falar com humano/atendente`.

### Fase 8 — Handoff manual `0` → contexto de 7 elementos
- 📲 Você envia: `0`
- 🤖 Téo: confirma handoff ao usuário; e **você (Ramão) recebe em 5547991041414** o contexto:
  nome · whatsapp · e‑mail · assunto · intenção · resumo · próximo passo.
- ✅ Valida **#8** e **#11** (7 elementos).

### Fase 9 — Acessar o site (fecho da jornada)
- Em qualquer resposta/encerramento, o link `🌐 fenice.ia.br` deve estar presente e clicável.
- 📲 Fluxo do site (paralelo): preencha o formulário em **fenice.ia.br**.
- 🤖 Em <60s: **e‑mail** (Graph, de `fenice_tech@fenice.ia.br`) **+ WhatsApp proativo** do Téo ao lead + **notificação a você** em 5547991041414.
- ✅ Valida **#9** e **#10** (já validados no E2E — reconfirme na prática).
- 🚫 Não‑perturbar: o proativo é **1 única** mensagem calorosa; nada de sequência de mensagens.

---

## Mapa fase → item de aceite

| Fase | Item(ns) | Como |
|---|---|---|
| 0 | #1 | `oi`/`olá`/`bom dia` → modal |
| 1 | #2 | `2`/`5` → boas‑vindas |
| 2 | #3 | pergunta → RAG+Gemini |
| 3 | (timing convite) | 3 msgs → convite 1x |
| 4 | #6 | `sair`/`7` encerra |
| 5 | #4 | 60min → 1 msg + silêncio |
| 6 | #5 | `retomar` sem menu |
| 7 | #7 | `preço` → handoff |
| 8 | #8, #11 | `0` → 7 elementos |
| 9 | #9, #10 | site → e‑mail + WhatsApp |

> Itens #4–#8 já têm cobertura de **teste unitário** (10/10 + 5/5). Este roteiro valida o
> comportamento **vivo** (mensagens reais, timing, e a regra de não perturbar).

*بِسْمِ اللهِ الرَّحْمَنِ الرَّحِيمِ · Fenice IT · Justech.IA*

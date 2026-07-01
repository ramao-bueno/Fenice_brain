---
tipo: spec
modulo: fenice-tim
titulo: "Modal Téo — Cartão Visual Único (WhatsApp)"
status: aprovado-design
autor: Ramão Bueno (Tech Lead) + Fenice IA (Claude & Open IA)
created: '2026-07-01'
tags: [fenice-tim, modal, whatsapp, evolution, n8n, design-visual, teo]
---

# Modal Téo — Cartão Visual Único (WhatsApp)

> Redesenho do menu de atendimento do Téo: de emojis-texto para um **cartão visual único**,
> amigável, alegre e comunicativo — corrigindo de vez as imagens que nunca funcionaram em produção.

---

## 1. Problema

O modal atual (nó `9a` do workflow `Fenice_Tim IVR v4`) envia um **menu em texto com emojis** +
**4 imagens separadas**. Dois bugs impedem as imagens de funcionar em produção:

1. **Endpoint errado:** os nós `9a-img*` usam `/message/sendImage/` — inexistente nesta versão do
   Evolution (retorna 404). O correto é `/message/sendMedia/`.
2. **Hospedagem quebrada:** as imagens apontam para `https://fenice.ia.br/modal/*.jpg`, que
   retorna 404 (nunca foram publicadas nessa URL).

Resultado: em produção o cliente vê só o texto; as imagens falham silenciosamente.

Além disso, o usuário quer elevar a experiência: substituir os emojis-botão por **logos reais** e
tornar o modal "amigável, interativo, alegre e comunicativo".

---

## 2. Restrição de plataforma (decisão-âncora)

**O WhatsApp não tem botões-com-imagem nativos** e **listas/botões nativos via Evolution
(Baileys) são instáveis** no WhatsApp atual. Portanto, a forma robusta de entregar um "modal com
logos" é um **cartão visual único** (uma imagem composta) + **seleção por número** no texto.

Abordagem escolhida: **Cartão visual único** (aprovada pelo usuário).

---

## 3. Design do cartão

### Layout — lista vertical (retrato ~1080×1440)
```
╭───────────────────────────────╮
│ [avatar Téo]  Téo             ◉ │  ◉ = logo Fenice (canto sup. dir.)
│               Intelligence Concierge │
├───────────────────────────────┤
│ [logo]  1 · TIM br              │
│ [logo]  2 · Acadêmico & Pesquisa │
│ [logo]  3 · Observatório da Mulher SFS │
│ [logo]  4 · API & Desenvolvedores │
│ [logo]  5 · Consultoria Jurídica │
│ [logo]  6 · Filosofia & Teologia │
│ [logo]  0 · Falar com Especialista │
├───────────────────────────────┤
│  Digite o número · ou *sair*    │
│  👤 Teo — Intelligence Concierge │
│  © 2026 Fenice IT Justech.IA     │
│  by Tech Lead Ramão Bueno        │
╰───────────────────────────────╯
```

### Estilo
- Fundo **preto brilhante** + acentos **dourado/laranja** (identidade Fenice).
- Fontes Adobe (`skeena-display`, `acumin-pro`); tiles arredondados para unificar os logos
  heterogêneos; brilho sutil no topo.
- Tom alegre, mas sóbrio e profissional.

### Mapeamento de itens → assets
Assets em `C:\Fenice_site\TIM\`:

| Nº | Label | Asset | Rota (inalterada) |
|---|---|---|---|
| **1** | TIM br *(era "B2B Corporativo")* | `emoji tim.jpeg` | b2b |
| **2** | Acadêmico & Pesquisa | `Acadêmico Ciências Jurídicas.jpeg` | academico |
| **3** | Observatório da Mulher SFS | `mulheres.jpeg` | observatorio |
| **4** | API & Desenvolvedores | `api e desenvolvedores.jpeg` | api |
| **5** | Consultoria Jurídica | `consultoria jurídica.jpeg` | juridico |
| **6** | Filosofia & Teologia | `filosofia.jpeg` | filosofia |
| **0** | Falar com Especialista | `especialista.jpeg` | humano |
| header | Avatar do Téo | `téo.jpeg` | — |
| topo-dir. | Logo Fenice | `logo fenice emoji.jpeg` | — |
| rodapé | Ícone "sair" (opcional) | `saida.jpeg` | reset/sair |

> **Sem mudança de fluxo:** a numeração permanece `1–6` + `0` (Especialista continua `0`). O
> `MENU_OPCOES` do workflow **não muda**. Alteração é puramente visual + rename do label do item 1.

### Rodapé — assinatura padrão (obrigatória)
```
👤 Teo — Intelligence Concierge
© 2026 Fenice IT Justech.IA
by Tech Lead Ramão Bueno
```

---

## 4. Entrega (pipeline)

```
HTML template ─(Playwright headless)→ card.png ─┬─ base64 → Evolution sendMedia   (teste imediato)
                                                └─ upload → Supabase Storage (URL) → nó 9a → produção
```

1. **Construir** o cartão em HTML (um arquivo autocontido, imagens embutidas em base64).
2. **Renderizar** para imagem via **Playwright headless** (`file://` URL — método já usado no
   projeto), saída PNG/JPG a 1080×1440.
3. **Teste:** enviar ao corporativo `5547991041414` via `sendMedia` **base64** (sem depender de
   hospedagem) → usuário aprova visualmente.
4. **Hospedar:** subir o cartão único num **bucket público do Supabase Storage** (confiável,
   instantâneo; evita o rebuild lento do Quartz e o path 404 do `fenice.ia.br/modal`).
5. **Workflow:** alterar o nó `9a` para **`sendMedia`** com a URL do cartão + legenda curta;
   **remover** os 4 nós `9a-img1/2/3/0` (substituídos pelo cartão único). Re-push via API N8N
   (ver [[project-modal-n8n-import-gap]] para a receita do PUT).

### Legenda do `sendMedia` (nó 9a)
```
👤 *Teo — Intelligence Concierge*

Escolha uma opção — digite o número (0–6). Para sair, digite *sair*.

© 2026 Fenice IT Justech.IA
by Tech Lead Ramão Bueno
```

---

## 5. Tratamento de erros
- **Render falha:** abortar antes de qualquer envio; nunca enviar cartão vazio/quebrado.
- **Upload Supabase falha:** manter o nó `9a` na versão anterior (backup do workflow) até a URL
  estar válida; validar a URL com um GET antes do re-push.
- **`sendMedia` 500 (AxiosError 404):** sinal de URL de mídia inacessível — revalidar hospedagem.
- **Eco/loop:** legenda contém `© 2026` → o filtro de eco do v4 já ignora (sem loop).

---

## 6. Testes / critérios de aceite
- [ ] Cartão renderiza a 1080×1440 com todos os 7 logos + Téo + logo Fenice legíveis.
- [ ] Rodapé traz a assinatura padrão completa (Téo + © 2026 + by Tech Lead Ramão Bueno).
- [ ] Item 1 exibe "TIM br"; numeração `1–6` + `0` preservada.
- [ ] Envio de teste ao `5547991041414` chega como **imagem** (não 404).
- [ ] Após re-push, o nó `9a` usa `sendMedia` e os nós `9a-img*` foram removidos.
- [ ] Cliente real recebe o cartão ao acionar o menu; seleção por número roteia correto.

---

## 7. Fora de escopo
- Mudança na lógica de roteamento do IVR (numeração e rotas ficam iguais).
- Listas/botões nativos do WhatsApp (descartados por instabilidade).
- Limpeza do subsistema AvisaAPI no FastAPI (Metade B — trilha separada).

---

*© 2026 Fenice IT Justech.IA — by Tech Lead Ramão Bueno — com o auxílio das maiores plataformas de IA — CLAUDE & Open IA.*

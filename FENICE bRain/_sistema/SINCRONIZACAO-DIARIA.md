---
name: sincronizacao-diaria
description: Guia prático — como sincronizar Fenice bRain com planalto.gov.br diariamente
type: sistema
---

# 📅 Sincronização Diária — Fenice bRain

Procedimento operacional para manter Fenice bRain atualizado com as mudanças legislativas de planalto.gov.br.

## ⏰ Fluxo Diário (Seg-Sex, ~15 min)

### 09:00 — Verificação da Noite

Douglas abre Fenice bRain e verifica:

```
1. Abrir: Fenice bRain → 00-Portal → INDEX.md
2. Ir em: "Últimas Atualizações"
3. Clicar em: "planalto-links.md"
```

### 09:05 — Prioridade Alta (3 links)

Procure por "Alterado pela Lei nº" ou "Revogado":

| Link | Frequency | Tempo |
|------|-----------|-------|
| [[Código Civil]][02-Civil] | 2x/semana (seg, qua) | 3 min |
| [[Código Penal]][03-Penal] | 2x/semana (ter, qui) | 3 min |
| [[Direito Tributário]][06-Tributario] | 3x/semana (seg, qua, sex) | 3 min |

### 09:15 — Prioridade Média (3 links)

| Link | Frequency | Tempo |
|------|-----------|-------|
| [[CLT]][04-Trabalho] | 1x/semana (ter) | 2 min |
| [[CDC]][05-Consumidor] | 1x/semana (qui) | 2 min |
| [[Constituição]][01-Constitucional] | 1x/mês (primeira seg) | 2 min |

### 09:25 — Prioridade Baixa (4 links)

| Link | Frequency | Tempo |
|------|-----------|-------|
| [[Lei Administrativa]][07-Administrativo] | 1x/mês | — |
| [[CPC]][08-Processual-Civil] | 1x/mês | — |
| [[CPP]][09-Processual-Penal] | 1x/mês | — |
| [[Direito Comercial]][10-Comercial] | 1x/mês | — |

## 📝 Se Encontrar uma Alteração

### Passo 1: Confirmar
- Leia a alteração **completa** no planalto.gov.br
- Verifique a data de vigência
- Identifique artigos afetados

### Passo 2: Documentar
Crie uma nova nota em **Fenice bRain → [Área] → Atualizações/**

**Nome do arquivo**: `YYYY-MM-DD-[Lei]-[O-que-mudou].md`

**Exemplo**: `2026-06-15-Codigo-Civil-Art-1º-Capacidade.md`

### Passo 3: Preencher
Use o template:

```
---
tags: [novo, alteracao, planalto, lei-x]
created: 2026-MM-DD
lei: Código Civil
artigos_afetados: [Art. 1º, Art. 5º]
vigencia: 2026-MM-DD
fonte: https://www.planalto.gov.br/...
---

# [Data] — Alteração: [Lei]

## O que Mudou
[Descrição clara]

## Antes
[Texto original]

## Depois
[Texto novo]

## Impacto
- Advogados: ...
- Empresas: ...
- Cidadãos: ...

## Links
- [[Art. 1º]] — link à nota do artigo original
```

### Passo 4: Vincular
Edite a nota do artigo original e adicione:

```
## Atualizações Recentes
- [[2026-06-15-Codigo-Civil-Art-1º-Capacidade]]
```

### Passo 5: Registrar
Atualize `_sistema/changelog.md`:

```
| 2026-06-15 | Código Civil | Art. 1º, Art. 5º | Alteração na capacidade | ✅ | [[Atualizacoes/2026-06-15...]] |
```

### Passo 6: Alertar Equipe
Se relevante (impacto alto), registre em `memory-log.md`:

```
## 2026-06-15 — Alteração Legislativa Importante

**Lei**: Código Civil  
**Artigos**: Art. 1º, Art. 5º  
**Impacto**: Alto — Afeta contratos e competência jurídica  
**Ação**: Revisar contratos em andamento  
**Notificação**: Equipe + Notion + Slack (se integrado)
```

---

## 🔍 Sinais de Alteração a Procurar

Quando visitando planalto.gov.br, procure por:

| Sinal | Exemplo | Ação |
|-------|---------|------|
| "Alterado pela" | "Alterado pela Lei nº 14.620/2023" | Documentar nova lei |
| "Revogado" | "Revogado pelo Art. 3º da Lei nº 14.450/2022" | Marcar como inativo |
| "Acrescentado" | "Acrescentado parágrafo §5º" | Documentar novo parágrafo |
| "Entra em vigor" | "Entra em vigor em AAAA-MM-DD" | Registrar vigência |
| "Sancionada" | "Sancionada em 2026-06-15" | Aguardar vigência |

---

## 📊 Checklist Semanal

**Toda segunda-feira:**

- [ ] Verificar Código Civil (2x/semana)
- [ ] Verificar Código Penal (2x/semana)
- [ ] Verificar Tributário (3x/semana)
- [ ] Atualizar changelog
- [ ] Revisar Atualizações pendentes
- [ ] Comunicar mudanças relevantes

**Toda quinta-feira:**

- [ ] Verificar CLT
- [ ] Verificar CDC
- [ ] Revisar Atualizações da semana

**Primeira segunda-feira de cada mês:**

- [ ] Verificar Constituição
- [ ] Revisar Administrativo/CPC/CPP/Comercial
- [ ] Compilar relatório mensal

---

## 🤖 Automação (Futuro)

### Opção 1: RSS Feed (Mais fácil)
Planalto oferece RSS de novas leis. Possíveis integrações:
- Feedly, Inoreader, Pocket
- Encaminhar para email/Slack

### Opção 2: API Planalto (Futuro)
Se disponível, poderia fazer sync automática via Python script.

### Opção 3: Notificação Claude Code
Adicionar hook em `.claude/settings.local.json`:

```json
{
  "hooks": {
    "SessionStart": [{
      "type": "command",
      "command": "echo '📜 Lembrete: Verificar planalto.gov.br hoje? (Fenice bRain)'"
    }]
  }
}
```

---

## 🚨 Emergências Legislativas

Se houver mudança legislativa **urgente/impactante**:

1. Documente imediatamente em Fenice bRain
2. Registre no memory-log com tag `#urgente`
3. Comunique equipe via Notion/Slack
4. Crie página no Notion database "📣 Conteúdo" com status "Urgente"

**Exemplo urgência**: Nova lei penal, alteração tributária, EC (Emenda Constitucional)

---

**Última revisão**: 2026-06-02  
**Próxima revisão**: 2026-06-09  
**Frequência de sincronização**: Diária (seg-sex)  
**Tempo estimado por dia**: 15 min

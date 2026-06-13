---
name: config-atualizacao
description: Configuração do sistema de atualização automática — Planalto.gov.br
type: sistema
---

# Configuração — Sistema de Atualização Automática

Como manter Fenice bRain sincronizado com planalto.gov.br.

## Fluxo de Atualização

```
Planalto.gov.br
    ↓ (diariamente)
Verificação manual / Automática
    ↓ (se houver mudança)
Lê alteração no Planalto
    ↓
Cria nota em Fenice bRain
    ↓
Vincula aos artigos afetados
    ↓
Atualiza changelog
    ↓
Registra no memory-log
```

## Responsabilidades

| Tarefa | Frequência | Responsável |
|--------|-----------|-------------|
| Verificar Constituição | 1x/mês | Claude |
| Verificar Código Civil | 3x/semana | Douglas |
| Verificar Código Penal | 3x/semana | Douglas |
| Verificar CLT | 4x/semana | Claude |
| Verificar CDC | 2x/semana | Claude |
| Verificar Tributário | 4x/semana | Claude |
| Atualizar changelog | Diariamente | Claude |
| Revisar jurisprudência | Semanal | Douglas |

## Ferramentas

### 1. Monitoramento Manual (Agora)

Visite os links em `planalto-links.md` e procure por "Alterações Recentes" ou use a busca do site.

**Exemplos de mudanças a procurar:**
- "Alterado pela Lei nº X/AAAA"
- "Revogado pelo artigo Y"
- "Acrescentado parágrafo §X"
- "Entra em vigor em AAAA-MM-DD"

### 2. Email / Newsletter Planalto (Futuro)

Cadastre-se em planalto.gov.br para receber notificações de novas leis.

### 3. RSS Feed (Futuro)

Planalto oferece RSS de leis/decretos. Pode ser integrado a um leitor.

### 4. API Planalto (Futuro)

Se disponível, poderia automatizar completamente a sincronização.

## Template para Nova Alteração

Sempre use: `_sistema/template-atualizacao.md`

Campos essenciais:
- Data da alteração
- Lei afetada
- Artigos alterados
- Texto antes/depois
- Vigência
- Impacto prático
- Links relacionados

## Integração com Notion

Quando há alteração importante:
1. Crie a nota em Fenice bRain (Obsidian)
2. Publica no Notion database "📣 Conteúdo" com tag `#legislacao-nova`
3. Equipe (Sofia Próvision) recebe notificação

## Histórico de Verificações

| Data | Verifi... | Lei | Resultado | Notas |
|------|-----------|-----|-----------|-------|
| 2026-06-02 | Inicial | Todas | Setup OK | Sistema novo |

---

## Agendamento Automático

**Para ativar notificações no Claude Code:**

Edite `.claude/settings.local.json` e adicione um hook:

```json
{
  "hooks": {
    "SessionStart": [{
      "type": "command",
      "command": "echo '📜 Lembrete: Verificar planalto.gov.br hoje?'",
      "statusMessage": "Verificando atualização legislativa..."
    }]
  }
}
```

> Nota: Isto exibe um lembrete ao abrir a sessão. Não é automático (ainda).

---

**Última verificação**: 2026-06-02  
**Próxima verificação agendada**: Diária (início de sessão)  
**Status**: 🟢 Sistema operacional — aguardando primeiras atualizações

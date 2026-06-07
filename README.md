---
tags: [sistema, guia]
---

# 🧠 Fenice Brain — Vault de Conhecimento Jurídico

Bem-vindo ao seu vault pessoal de conhecimento jurídico. Este é seu segundo cérebro para armazenar, organizar e recuperar informações legais estruturadas.

## 📁 Estrutura do Vault

```
Fenice brain/
├── 00 - Inbox/                    # Captura rápida — tudo novo entra aqui
├── 01 - Projetos/                 # Projetos ativos (p. ex.: casos, pesquisas)
├── 02 - Áreas/                    # Áreas permanentes (Tributário, Penal, etc.)
├── 03 - Recursos/                 # Material de referência, tutoriais, docs
├── 04 - Arquivo/                  # Projetos concluídos, notas antigas
├── 05 - Templates/                # Templates para criar novas notas
├── 06 - NotebookLM/               # Documentos estruturados para análise IA
│   ├── sources/                   # Documentos pra enviar ao NotebookLM
│   └── exports/                   # Resumos/insights do NotebookLM
├── _sistema/                      # Configurações e metadados
│   ├── memory-log.md              # Log de decisões e contexto
│   ├── tags-index.md              # Índice centralizado de tags
│   └── notion-config.md           # Configuração de integração com Notion
└── FENICE bRain/                  # Seu conteúdo jurídico existente
    ├── 00_CONSTITUIÇÃO_FEDERAL/
    ├── 02_DIREITO_CIVIL/
    ├── 03_CÓDIGO_PENAL/
    └── ... (outros)
```

## 🎯 Como Usar Cada Pasta

### 00 - Inbox
**Propósito**: Captura rápida de ideias, notas e informações
- Tudo novo vai aqui primeiro, sem preocupação com organização
- Revise regularmente e mova para a pasta correta
- Use quando estiver aprendendo algo novo ou capturando uma ideia

### 01 - Projetos
**Propósito**: Documentação de projetos ativos
- Cada projeto tem uma pasta própria com `_index.md`
- Exemplo: `01 - Projetos/case-fulano/`, `01 - Projetos/pesquisa-lei-x/`
- Use template: `template-projeto.md`

### 02 - Áreas
**Propósito**: Conhecimento permanente de áreas jurídicas
- Exemplos: `02 - Áreas/Direito Civil/`, `02 - Áreas/Direito Penal/`
- Crescem organicamente à medida que você acumula conhecimento
- Integre seu conteúdo jurídico existente aqui

### 03 - Recursos
**Propósito**: Material de referência, tutoriais, legislação
- Documentações técnicas
- Leis comentadas
- Jurisprudência compilada
- Material de estudo

### 04 - Arquivo
**Propósito**: Manutenção histórica
- Projetos concluídos
- Notas antigas ou obsoletas
- Mantenha a história, não delete

### 05 - Templates
**Propósito**: Templates prontos para novas notas
- `template-nota.md` — Nota genérica
- `template-projeto.md` — Novo projeto
- `template-decisao.md` — Decisão importante
- `template-recurso-juridico.md` — Conteúdo jurídico

### 06 - NotebookLM
**Propósito**: Integração com NotebookLM para análise
- **sources/**: Documentos estruturados para análise
- **exports/**: Resultados gerados pelo NotebookLM

### _sistema
**Propósito**: Sistema e metadados
- `memory-log.md` — Log entre sessões do Claude
- `tags-index.md` — Todas as tags disponíveis
- `notion-config.md` — Integração com Notion

## 🏷️ Sistema de Tags

Todas as notas usam tags no frontmatter para organização. Consulte `_sistema/tags-index.md` para a lista completa.

**Exemplo**:
```markdown
---
tags: [projeto, direito-civil, em-progresso]
created: 2026-06-03
---
```

### Tags Principais
- **Tipo**: `#nota`, `#projeto`, `#recurso`, `#ideia`, `#decisão`
- **Status**: `#rascunho`, `#em-progresso`, `#revisão`, `#pronto`, `#arquivado`
- **Área Jurídica**: `#direito-civil`, `#direito-penal`, `#direito-tributário`, etc.
- **Operacional**: `#pendente`, `#importante`, `#revisar`

## 📝 Fluxo de Trabalho Padrão

### Ao capturar uma ideia
1. Crie uma nota em `00 - Inbox/`
2. Adicione tags básicas
3. Escreva o pensamento rapidamente
4. Revise e organize mais tarde

### Ao criar um projeto
1. Crie pasta em `01 - Projetos/nome-projeto/`
2. Crie `_index.md` com `template-projeto.md`
3. Vincule documentos relacionados
4. Atualize status conforme progride

### Ao documentar uma decisão
1. Use `template-decisao.md`
2. Registre data, opções, escolha e racional
3. Adicione ao memory-log

### Ao organizar (semanal)
1. Revise `00 - Inbox/`
2. Mova notas para pastas corretas
3. Atualize tags conforme necessário
4. Arquivo notas obsoletas

## 🔗 Integração com Notion

O vault está configurado para sincronizar com o workspace **Sofia Próvision HQ** no Notion.

**Consulte**: `_sistema/notion-config.md`

Fluxo:
1. Notas amadurecem no Obsidian (vault pessoal)
2. Quando prontas, publicam para Notion (equipe)
3. Notion é a fonte de verdade para execução
4. Obsidian é a fonte de verdade para conhecimento

## 💡 Boas Práticas

✅ **Faça**:
- Use wikilinks `[[assim]]` para conectar ideias
- Mantenha notas atômicas (um conceito por nota)
- Revise o memory-log regularmente
- Arquivo notas antigas, não delete

❌ **Não faça**:
- Não coloque dados sensacionais/privados sem tag `#privado`
- Não publique no Notion sem revisar primeiro
- Não misture múltiplos tópicos em uma nota
- Não ignore o sistema de tags

## 🚀 Primeiros Passos

1. **Explore os templates** em `05 - Templates/`
2. **Leia** `_sistema/memory-log.md` para contexto
3. **Consulte** `_sistema/tags-index.md` para tags disponíveis
4. **Crie sua primeira nota** usando um template
5. **Configure Notion** quando estiver pronto (`_sistema/notion-config.md`)

## 📞 Suporte

Para dúvidas sobre organização, integração com Notion ou uso de tags, consulte:
- [[memory-log]] — Decisões passadas e contexto
- [[tags-index]] — Todas as tags do sistema
- [[notion-config]] — Integração com equipe

---

**Vault criado**: 2026-06-03
**Última atualização**: 2026-06-03
**Status**: Pronto para usar

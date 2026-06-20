---
tags:
  - ferramentas
  - referencia
  - vscode
  - claude
  - obsidian
  - comandos
tipo: guia-referencia
status: vigente
criado: 2026-06-20
---

# Guia de Comandos — VS Code · Claude Code · Obsidian

> [!abstract] Sobre este guia
> Referência rápida dos principais comandos (verbos de ação) do ambiente de desenvolvimento.
> Organizado por ferramenta, com atalho, descrição e contexto de uso.

---

## 1. Visual Studio Code

### Paleta de Comandos
| Atalho | Verbo / Ação | Descrição |
|---|---|---|
| `Ctrl+Shift+P` | **Executar Comando** | Abre a paleta de todos os comandos disponíveis |
| `Ctrl+P` | **Abrir Arquivo** | Busca e abre arquivo por nome |
| `Ctrl+Shift+N` | **Nova Janela** | Abre nova instância do VS Code |
| `Ctrl+W` | **Fechar Aba** | Fecha o arquivo/aba ativa |
| `Ctrl+Shift+W` | **Fechar Janela** | Fecha a janela inteira |

### Edição
| Atalho | Verbo / Ação | Descrição |
|---|---|---|
| `Ctrl+X` | **Recortar Linha** | Recorta a linha inteira sem seleção |
| `Ctrl+C` | **Copiar Linha** | Copia a linha inteira sem seleção |
| `Ctrl+V` | **Colar** | Cola o conteúdo da área de transferência |
| `Ctrl+Z` | **Desfazer** | Reverte a última ação |
| `Ctrl+Y` | **Refazer** | Reaplica a última ação desfeita |
| `Ctrl+D` | **Selecionar Próxima Ocorrência** | Seleciona a próxima ocorrência da palavra |
| `Ctrl+Shift+L` | **Selecionar Todas as Ocorrências** | Seleciona todas as ocorrências no arquivo |
| `Alt+↑ / Alt+↓` | **Mover Linha** | Move a linha atual para cima ou para baixo |
| `Shift+Alt+↓` | **Duplicar Linha** | Copia a linha atual abaixo |
| `Ctrl+/` | **Comentar/Descomentar** | Alterna comentário na linha ou seleção |
| `Shift+Alt+F` | **Formatar Documento** | Formata todo o arquivo com o formatter ativo |
| `Ctrl+K Ctrl+F` | **Formatar Seleção** | Formata apenas o trecho selecionado |
| `F2` | **Renomear Símbolo** | Renomeia variável/função em todo o projeto |
| `Ctrl+.` | **Ação Rápida** | Abre sugestões de correção/refatoração |

### Navegação
| Atalho | Verbo / Ação | Descrição |
|---|---|---|
| `Ctrl+G` | **Ir para Linha** | Navega para um número de linha específico |
| `Ctrl+Shift+O` | **Ir para Símbolo** | Lista funções/classes do arquivo atual |
| `F12` | **Ir para Definição** | Vai até onde o símbolo é definido |
| `Alt+F12` | **Espiar Definição** | Mostra a definição em popup inline |
| `Shift+F12` | **Ver Referências** | Lista todos os usos do símbolo |
| `Ctrl+Tab` | **Alternar Aba** | Navega entre abas abertas |
| `Ctrl+Home / End` | **Início / Fim do Arquivo** | Vai para o início ou fim do documento |
| `Ctrl+[` / `Ctrl+]` | **Recuar / Avançar Indentação** | Ajusta indentação da linha/seleção |

### Busca e Substituição
| Atalho | Verbo / Ação | Descrição |
|---|---|---|
| `Ctrl+F` | **Buscar** | Busca texto no arquivo atual |
| `Ctrl+H` | **Substituir** | Busca e substitui no arquivo atual |
| `Ctrl+Shift+F` | **Buscar no Projeto** | Busca em todos os arquivos do workspace |
| `Ctrl+Shift+H` | **Substituir no Projeto** | Substitui em todos os arquivos |

### Terminal Integrado
| Atalho | Verbo / Ação | Descrição |
|---|---|---|
| `` Ctrl+` `` | **Abrir Terminal** | Abre/fecha o terminal integrado |
| `Ctrl+Shift+`  `` | **Novo Terminal** | Abre nova instância de terminal |
| `Ctrl+C` | **Interromper Processo** | Cancela o processo em execução |
| `! <comando>` | **Executar no Chat** | Roda comando diretamente no terminal do Claude Code |

### Explorador e Git
| Atalho | Verbo / Ação | Descrição |
|---|---|---|
| `Ctrl+Shift+E` | **Abrir Explorador** | Mostra/oculta o painel de arquivos |
| `Ctrl+Shift+G` | **Abrir Git** | Mostra painel de controle de versão |
| `Ctrl+Shift+X` | **Abrir Extensões** | Gerencia extensões instaladas |
| `Ctrl+Shift+D` | **Abrir Debug** | Painel de depuração |

### Janelas e Painéis
| Atalho | Verbo / Ação | Descrição |
|---|---|---|
| `Ctrl+B` | **Alternar Barra Lateral** | Mostra/oculta o painel lateral |
| `Ctrl+J` | **Alternar Painel Inferior** | Mostra/oculta terminal/output/problemas |
| `Ctrl+\` | **Dividir Editor** | Abre segundo editor lado a lado |
| `Ctrl+K Z` | **Modo Zen** | Modo de foco total, sem painéis |
| `F11` | **Tela Cheia** | Alterna modo tela cheia |

---

## 2. Claude Code (Anthropic CLI)

### Comandos de Sessão (Slash Commands)
| Comando | Verbo / Ação | Descrição |
|---|---|---|
| `/help` | **Ajudar** | Lista todos os comandos disponíveis |
| `/clear` | **Limpar** | Limpa o histórico da conversa atual |
| `/compact` | **Compactar** | Resume o contexto da conversa para economizar tokens |
| `/memory` | **Memorizar** | Acessa e gerencia o sistema de memória persistente |
| `/init` | **Inicializar** | Cria o arquivo CLAUDE.md no projeto atual |
| `/bug` | **Reportar Bug** | Abre o formulário de report de bug |
| `/feedback` | **Enviar Feedback** | Envia feedback para a Anthropic |
| `/login` | **Autenticar** | Faz login na conta Anthropic |
| `/logout` | **Desautenticar** | Faz logout da conta |
| `/doctor` | **Diagnosticar** | Verifica o estado do ambiente Claude Code |

### Comandos de Modo
| Comando | Verbo / Ação | Descrição |
|---|---|---|
| `/plan` | **Planejar** | Entra no modo de planejamento (sem executar ações) |
| `/fast` | **Acelerar** | Alterna para modo rápido (Claude Opus com output mais veloz) |
| `/review` | **Revisar** | Inicia revisão de código do branch atual |
| `/code-review ultra` | **Revisão Profunda** | Revisão multi-agente do branch ou PR |

### Atalhos de Teclado no Chat
| Atalho | Verbo / Ação | Descrição |
|---|---|---|
| `↑` | **Recuperar Histórico** | Navega para o último comando digitado |
| `Ctrl+C` | **Cancelar** | Interrompe a geração ou a ação em curso |
| `Ctrl+L` | **Limpar Tela** | Limpa o terminal (equivale a `/clear`) |
| `Tab` | **Completar** | Autocompleta nomes de arquivos e comandos |
| `! <cmd>` | **Executar Shell** | Roda o comando no terminal sem sair do chat |

### Permissões e Segurança
| Comando / Ação | Verbo | Descrição |
|---|---|---|
| Aprovar ferramenta | **Autorizar** | Permite que Claude execute uma ferramenta específica |
| Negar ferramenta | **Bloquear** | Impede a execução da ferramenta solicitada |
| `--dangerously-skip-permissions` | **Ignorar Restrições** | Modo autônomo sem prompts (uso avançado) |

### Skills Disponíveis neste Vault
| Skill | Verbo / Ação | Quando Usar |
|---|---|---|
| `atomizar-juridico` | **Atomizar** | Converte texto jurídico bruto em notas atômicas Obsidian |
| `systematic-debugging` | **Depurar** | Diagnóstico sistemático de bugs (Fase 1→4) |

---

## 3. Obsidian

### Navegação e Arquivos
| Atalho | Verbo / Ação | Descrição |
|---|---|---|
| `Ctrl+O` | **Abrir Nota** | Quick Switcher — busca e abre qualquer nota |
| `Ctrl+N` | **Nova Nota** | Cria uma nova nota vazia |
| `Ctrl+Shift+N` | **Nova Nota na Pasta** | Cria nota na pasta selecionada no explorador |
| `Ctrl+P` | **Paleta de Comandos** | Lista todos os comandos disponíveis |
| `Ctrl+W` | **Fechar Aba** | Fecha a nota/aba ativa |
| `Ctrl+Tab` | **Próxima Aba** | Navega para a próxima aba aberta |
| `Alt+←` / `Alt+→` | **Voltar / Avançar** | Navega no histórico de notas visitadas |

### Edição
| Atalho | Verbo / Ação | Descrição |
|---|---|---|
| `Ctrl+E` | **Alternar Modo** | Alterna entre edição e visualização |
| `Ctrl+B` | **Negrito** | Aplica formatação **negrito** |
| `Ctrl+I` | **Itálico** | Aplica formatação *itálico* |
| `Ctrl+K` | **Inserir Link** | Insere link Markdown `[texto](url)` |
| `Ctrl+Z` | **Desfazer** | Reverte a última ação |
| `Ctrl+F` | **Buscar na Nota** | Busca texto na nota atual |
| `Ctrl+H` | **Substituir na Nota** | Busca e substitui na nota atual |
| `Ctrl+Shift+F` | **Buscar no Vault** | Busca em todas as notas |

### Visualização e Layout
| Atalho | Verbo / Ação | Descrição |
|---|---|---|
| `Ctrl+G` | **Abrir Grafo** | Abre o Graph View do vault |
| `Ctrl+Shift+I` | **DevTools** | Abre o inspetor de elementos (console JS) |
| `Ctrl+,` | **Configurações** | Abre o painel de configurações |

### Plugin — Fenice Buscar Artigo (v19)
| Atalho | Verbo / Ação | Descrição |
|---|---|---|
| `Ctrl+Shift+B` | **Buscar Artigo** | Inicia busca por código jurídico + número de artigo |
| `Ctrl+Shift+I` | **Info do Artigo** | Mostra InfoModal do artigo atualmente aberto |

**Fluxo Ctrl+Shift+B:**
```
iniciarBusca()
  → console.clear() + copilot:new-chat (se painel aberto)
  → CodigoModal (selecionar código: CC, CPC, CF, CP…)
  → ArtigoModal (digitar número do artigo)
  → InfoModal (texto legal + análise técnica + correlatos + jurisprudência)
```

**Dentro do InfoModal:**
| Ação | Verbo | Resultado |
|---|---|---|
| Clicar em correlato `[[Art. N — CF]]` | **Navegar** | Abre InfoModal do artigo destino (cross-code) |
| Clicar em "Nova Busca" | **Reiniciar** | CLS + volta ao CodigoModal |
| Clicar em "Fechar" / ESC | **Fechar** | Fecha o InfoModal |

### Plugin — Copilot (v3.3.3)
| Atalho / Comando | Verbo / Ação | Descrição |
|---|---|---|
| Ícone na sidebar | **Abrir Chat** | Abre o painel de chat do Copilot |
| `copilot:new-chat` | **Limpar Chat** | Inicia novo chat (CLS do Copilot) |
| `copilot:chat-toggle-window` | **Alternar Painel** | Mostra/oculta o painel Copilot |
| `copilot:load-copilot-chat-conversation` | **Carregar Conversa** | Abre conversa salva anterior |
| `copilot:index-vault-to-copilot-index` | **Indexar Vault** | Atualiza o índice semântico do vault |
| `copilot:force-reindex-vault-to-copilot-index` | **Reindexar** | Força reindexação completa |
| `copilot:clear-local-copilot-index` | **Limpar Índice** | Remove o índice local |

**Modelos ativos no Copilot:**
| Modelo | Provider | Status |
|---|---|---|
| `claude-sonnet-4-6` | Anthropic | ✅ padrão |
| `google/gemini-2.5-flash` | OpenRouter | ✅ ativo |
| `gemini-2.5-flash` | Google direto | ✅ ativo |

### Plugin — QuickAdd (v2.12.3)
| Atalho | Verbo / Ação | Descrição |
|---|---|---|
| Ícone ribbon | **Executar Macro** | Executa uma macro ou template configurado |
| `quickadd:run-quickadd` | **Acionar** | Dispara o QuickAdd via paleta de comandos |

### Plugin — Templater (v2.20.5) — *desabilitado*
| Atalho | Verbo / Ação | Descrição |
|---|---|---|
| `Alt+T` | **Inserir Template** | Insere template no arquivo atual *(requer habilitar)* |

---

## Referência Rápida — Configurações do Vault

| Item | Valor |
|---|---|
| Vault path | `C:\Fenice_bRain` |
| Git branch | `main` |
| Plugin ativo principal | Fenice v19 |
| Modelo Copilot padrão | `claude-sonnet-4-6` \| Anthropic |
| Skill de atomização | `atomizar-juridico` |
| Backup Git | automático (backup.ps1) |

---

*Fenice bRain · Referência de Ferramentas · 2026-06-20*

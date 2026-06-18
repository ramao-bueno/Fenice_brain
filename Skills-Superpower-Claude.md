# Skills Superpower — Claude Code
**Tech Lead:** Ramão Bueno da Silva Neto | FeniceTech
**Atualizado:** 2026-06-18

---

## MCP Integrations (Superpower — Apps Externos)

| Integração | Acesso | Status |
|---|---|---|
| **Obsidian** | Leitura e escrita no vault `C:\Fenice_bRain` | ✅ Ativo |
| **Adobe Creative** | Imagens, vídeos, design, Express, Firefly | ✅ Ativo |
| **Gamma** | Apresentações e documentos com IA | ✅ Ativo |
| **Gmail** | E-mails, rascunhos, labels | ✅ Ativo |
| **Google Calendar** | Eventos, agendamento, sugestão de horários | ✅ Ativo |
| **Google Drive** | Arquivos, docs, permissões | ✅ Ativo |
| **Microsoft 365** | Teams, SharePoint, Outlook, Calendário | ✅ Ativo |
| **Slack** | Mensagens, canais, canvas, threads | ✅ Ativo |
| **Notion** | Pages, databases, comentários, views | ✅ Ativo |

---

## Agentes Especializados (Superpower — Inteligência)

| Agente | Quando usar |
|---|---|
| `Explore` | Busca profunda em código e arquivos |
| `Plan` | Arquitetar planos de implementação |
| `vercel:ai-architect` | Projetar apps com IA no Vercel |
| `vercel:performance-optimizer` | Otimização de performance e Core Web Vitals |
| `vercel:deployment-expert` | Deploy, CI/CD, rollback, domínios |

---

## Skills — Vercel Infraestrutura e Deploy

| Skill | Função |
|---|---|
| `/vercel:deploy` | Deploy para preview ou produção |
| `/vercel:status` | Status de deployments e projeto |
| `/vercel:env` | Gerenciar variáveis de ambiente |
| `/vercel:env-vars` | Guia avançado de variáveis de ambiente |
| `/vercel:deployments-cicd` | CI/CD, pipelines, rollback, promote |
| `/vercel:bootstrap` | Inicializar projeto com recursos Vercel vinculados |
| `/vercel:vercel-cli` | Guia completo do Vercel CLI |
| `/vercel:vercel-agent` | Agente Vercel para reviews e investigações |
| `/vercel:vercel-firewall` | Configuração de firewall e segurança |
| `/vercel:verification` | Verificação de domínios e configurações |
| `/vercel:knowledge-update` | Correções de conhecimento desatualizado sobre Vercel |

---

## Skills — Vercel Frontend e Framework

| Skill | Função |
|---|---|
| `/vercel:nextjs` | Guia Next.js no Vercel |
| `/vercel:next-upgrade` | Migração entre versões do Next.js |
| `/vercel:next-forge` | Boilerplate Next.js avançado |
| `/vercel:next-cache-components` | Cache Components, PPR, use cache |
| `/vercel:react-best-practices` | Boas práticas React |
| `/vercel:shadcn` | Componentes UI com shadcn/ui |
| `/vercel:turbopack` | Configuração e uso do Turbopack |
| `/vercel:routing-middleware` | Middleware e roteamento |
| `/vercel:microfrontends` | Arquitetura de microfrontends |

---

## Skills — Vercel Backend e Plataforma

| Skill | Função |
|---|---|
| `/vercel:vercel-functions` | Funções serverless no Vercel |
| `/vercel:vercel-storage` | Blob, bancos de dados, storage |
| `/vercel:vercel-sandbox` | Execução de código em sandbox |
| `/vercel:runtime-cache` | Estratégias de cache em runtime |
| `/vercel:marketplace` | Integrações do Vercel Marketplace |
| `/vercel:workflow` | Workflows e automações |

---

## Skills — Vercel IA e APIs

| Skill | Função |
|---|---|
| `/vercel:ai-sdk` | AI SDK — chat, agentes, streaming, tools |
| `/vercel:ai-gateway` | AI Gateway — roteamento de modelos, fallback |
| `/vercel:ai-architect` | Arquitetura de apps com IA |
| `/vercel:chat-sdk` | Chat SDK — bots Slack, Teams, Telegram |
| `/vercel:auth` | Autenticação — Clerk, Auth0, Descope |
| `/claude-api` | API Claude/Anthropic — modelos, preços, streaming |

---

## Skills — Qualidade e Código

| Skill | Função |
|---|---|
| `/code-review` | Revisão de código (low / medium / high / ultra) |
| `/code-review ultra` | Revisão multi-agente profunda em cloud ☁️ |
| `/simplify` | Simplificação e limpeza de código |
| `/security-review` | Revisão de segurança |
| `/verify` | Verificar se uma mudança funciona na prática |

---

## Skills — Projeto e Execução

| Skill | Função |
|---|---|
| `/run` | Rodar o projeto localmente |
| `/init` | Inicializar CLAUDE.md com documentação |
| `/review` | Revisar um pull request |
| `/loop` | Rodar um comando em intervalo recorrente |
| `/schedule` | Agendar tarefas automáticas em cloud |

---

## Skills — Configuração do Ambiente

| Skill | Função |
|---|---|
| `/update-config` | Configurar settings.json, hooks, permissões |
| `/keybindings-help` | Personalizar atalhos de teclado |
| `/fewer-permission-prompts` | Reduzir prompts de permissão |

---

## Mapeamento por Contexto (Uso Proativo)

| Contexto | Skills a invocar automaticamente |
|---|---|
| **Fenice Brain / Next.js** | `/vercel:nextjs`, `/vercel:ai-sdk`, `/code-review` |
| **Deploy produção** | `/vercel:deploy`, `/vercel:status` |
| **Novo site / landing page** | `/vercel:shadcn`, `/run`, `/code-review` |
| **Variáveis de ambiente** | `/vercel:env` |
| **IA / chat / agentes** | `/vercel:ai-architect`, `/vercel:ai-sdk` |
| **Revisão de código** | `/code-review ultra` |
| **Teste local** | `/run` |
| **Projeto novo** | `/vercel:bootstrap`, `/init` |
| **Notas / documentação** | Obsidian MCP |
| **Apresentações** | Gamma MCP |
| **E-mails / agenda** | Gmail + Google Calendar MCP |
| **Comunicação time** | Slack / Teams MCP |

---

## Vault Obsidian

- **Caminho:** `C:\Fenice_bRain`
- **MCP:** `mcp-obsidian` (configurado em `.claude.json`)
- **Capacidades:** Ler notas, criar notas, buscar conteúdo, editar arquivos `.md`

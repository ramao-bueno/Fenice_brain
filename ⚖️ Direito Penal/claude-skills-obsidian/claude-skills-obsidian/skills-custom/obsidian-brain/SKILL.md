---
name: obsidian-brain
description: >
  Sistema de gestão de conhecimento pessoal + hub operacional da equipe Próvision,
  integrando Obsidian (cérebro pessoal do Douglas), NotebookLM (estudo/análise) e
  Notion (execução em equipe). Use esta skill SEMPRE que o usuário mencionar: Obsidian,
  vault, notas, segundo cérebro, PKM, base de conhecimento, NotebookLM, memória do Claude,
  "o que eu já escrevi sobre", "onde eu anotei", organizar notas, criar nota, capturar
  ideia, gerar conteúdo a partir das notas, exportar para NotebookLM, resumo das notas,
  buscar no vault, tags, templates, daily notes, ou qualquer referência a "lembrar" algo
  de sessões anteriores. Também ative quando o usuário mencionar: Notion, workspace da
  equipe, Sofia Próvision HQ, sincronizar com equipe, publicar no Notion, tarefas da
  equipe, kanban, databases do Notion, dashboard executivo, "mandar pro time", "colocar
  no Notion", ou qualquer fluxo de handoff entre o trabalho pessoal do Douglas e a
  operação da equipe Próvision. Também ative quando o usuário pedir conteúdo de marketing,
  posts para redes sociais ou blog, se o contexto indicar que deve vir da base de
  conhecimento. Se houver dúvida, ative — é melhor consultar o vault e não precisar do
  que precisar e não consultar.
---

# Obsidian Brain — Conhecimento Pessoal + Hub da Equipe Próvision

Você é o cérebro por trás do vault do Obsidian do Douglas **e a ponte dele com a equipe da Próvision no Notion**. Seu papel é quádruplo:

1. **Memória persistente** — O vault é sua memória de longo prazo. Antes de responder perguntas sobre projetos, decisões passadas ou contexto pessoal, consulte o vault. Isso evita respostas genéricas e garante continuidade entre sessões.

2. **Organizador inteligente** — Você mantém o vault estruturado, cria notas no padrão certo, aplica tags, conecta ideias com links internos, e mantém tudo encontrável.

3. **Motor de conteúdo** — Você transforma conhecimento bruto em outputs úteis: resumos para NotebookLM, posts para redes sociais, documentação técnica, relatórios.

4. **Ponte com a equipe (Notion)** — Você traduz o trabalho pessoal do Douglas no vault em itens acionáveis para a equipe da Próvision no workspace "Sofia Próvision HQ" no Notion. O vault é privado e bagunçado (do jeito que o Douglas pensa); o Notion é público para a equipe, limpo e estruturado. Ver seção "Módulo: Integração com Notion" no final desta skill.

## Estrutura do Vault

O vault segue esta organização. Ao criar notas, sempre respeite esta estrutura:

```
Obsidian Vault/
├── 00 - Inbox/              # Captura rápida — tudo entra aqui primeiro
├── 01 - Projetos/           # Projetos ativos (cada um com sua pasta)
│   ├── guilherme/
│   ├── aired-provision/
│   └── ...
├── 02 - Áreas/              # Áreas permanentes da vida
│   ├── Financeiro/
│   ├── Saúde/
│   ├── Aprendizado/
│   └── Marketing/
├── 03 - Recursos/           # Material de referência
│   ├── Tutoriais/
│   ├── Documentações/
│   └── Snippets/
├── 04 - Arquivo/            # Projetos concluídos, notas antigas
├── 05 - Templates/          # Templates de notas
├── 06 - NotebookLM/         # Pacotes prontos para exportar ao NotebookLM
│   ├── sources/             # Documentos formatados para upload
│   └── exports/             # Conteúdo gerado a partir do NotebookLM
└── _sistema/                # Configurações e metadados do sistema
    ├── memory-log.md        # Log de decisões e contexto entre sessões
    └── tags-index.md        # Índice centralizado de tags
```

### Regras de organização

- Notas novas sem contexto claro vão para `00 - Inbox/`
- Mova notas do Inbox para o local correto assim que o contexto ficar claro
- Cada projeto em `01 - Projetos/` tem um `_index.md` com status e links
- Prefixe notas com data quando relevante: `2026-04-09 - Título da nota.md`

## Formato Padrão de Notas

Toda nota criada deve seguir este template (adaptando conforme o tipo):

```markdown
---
tags: [tag1, tag2]
created: YYYY-MM-DD
type: nota|projeto|recurso|ideia|decisão
status: ativo|em-progresso|concluído|arquivado
related: [[Link para nota relacionada]]
---

# Título

## Contexto
Por que esta nota existe, o que motivou.

## Conteúdo
O conteúdo principal.

## Próximos Passos
O que fazer com essa informação (se aplicável).

## Links
- [[Notas relacionadas]]
```

### Tipos de nota e quando usar cada um

- **nota**: Informação geral, anotação de algo aprendido
- **projeto**: Documentação de um projeto específico
- **recurso**: Tutorial, documentação, referência técnica
- **ideia**: Algo a explorar no futuro
- **decisão**: Registro de uma decisão tomada e o raciocínio por trás

## Memória Persistente — Como Funcionar como "Memória Infinita"

Este é o recurso mais importante. O vault funciona como sua memória de longo prazo.

### Quando consultar o vault

SEMPRE que o usuário:
- Perguntar algo sobre um projeto ("como tá o guilherme?")
- Referir a uma decisão passada ("a gente já decidiu sobre X?")
- Pedir contexto ("o que eu já sei sobre Y?")
- Iniciar uma nova sessão de trabalho (leia `_sistema/memory-log.md` primeiro)

### Como consultar

1. Use `Grep` para buscar termos-chave no vault
2. Use `Glob` para encontrar notas por nome/pasta
3. Leia as notas relevantes com `Read`
4. Sintetize o que encontrou antes de responder

### Memory Log

O arquivo `_sistema/memory-log.md` é o diário do Claude. Ao final de cada sessão produtiva ou quando decisões importantes forem tomadas, registre:

```markdown
## YYYY-MM-DD — Resumo da Sessão

### O que foi feito
- Item 1
- Item 2

### Decisões tomadas
- Decisão X: razão Y

### Contexto importante para próxima sessão
- Ponto pendente 1
- Ponto pendente 2

### Notas criadas/modificadas
- [[nota1]]
- [[nota2]]
```

## Integração com NotebookLM

O NotebookLM não tem API direta. A integração funciona assim:

### Exportar para NotebookLM

1. O usuário pede para preparar conteúdo sobre um tema
2. Claude busca notas relacionadas no vault
3. Consolida tudo em um documento bem estruturado em `06 - NotebookLM/sources/`
4. Se o Google Drive estiver disponível, faz upload via MCP do Google Drive
5. O usuário abre o NotebookLM e adiciona o documento como source

O formato ideal para fontes do NotebookLM:
- Markdown ou PDF
- Bem estruturado com headers claros
- Máximo ~50.000 palavras por documento (limite do NotebookLM)
- Inclua contexto suficiente — o NotebookLM funciona melhor com documentos ricos

### Importar do NotebookLM

Quando o usuário trouxer insights ou resumos do NotebookLM:
1. Crie uma nota no vault com type: `recurso`
2. Adicione tag `#notebooklm`
3. Vincule às notas originais que foram usadas como fonte
4. Registre no memory-log

### Pacotes temáticos

Para temas recorrentes, crie "pacotes" — conjuntos de notas organizadas por assunto que podem ser atualizadas e re-exportadas facilmente:

```
06 - NotebookLM/sources/
├── vibe-coding-fundamentos.md
├── provision-estrategia.md
├── supabase-reference.md
└── marketing-digital-base.md
```

## Geração de Conteúdo

Quando o usuário pedir conteúdo de marketing, posts, ou qualquer output público:

1. **Busque no vault primeiro** — Não invente do zero. Use o conhecimento acumulado
2. **Respeite a voz** — Douglas é direto, técnico mas acessível, sem corporativês
3. **Salve o output** — Crie uma nota em `02 - Áreas/Marketing/` com o conteúdo gerado
4. **Registre a fonte** — Vincule às notas que serviram de base

### Formatos comuns

- **Post LinkedIn/Twitter**: Curto, direto, com hook forte. Salve como nota com tag `#content/social`
- **Blog post**: Mais profundo, com exemplos práticos. Salve em `02 - Áreas/Marketing/Blog/`
- **Documentação técnica**: Clara, com exemplos de código. Salve em `03 - Recursos/`

## Setup Inicial do Vault

Se o vault estiver vazio ou desorganizado, execute o setup:

1. Crie a estrutura de pastas conforme definida acima
2. Mova notas existentes para os locais corretos
3. Crie o `_sistema/memory-log.md` inicial
4. Crie o `_sistema/tags-index.md` com as tags base
5. Crie os templates em `05 - Templates/`
6. Crie `_index.md` para cada projeto existente

### Tags base do sistema

```
#projeto     — Relacionado a um projeto
#ideia       — Ideia a explorar
#decisão     — Decisão registrada
#recurso     — Material de referência
#aprendizado — Algo aprendido
#content/social — Conteúdo para redes
#content/blog   — Conteúdo para blog
#notebooklm    — Veio do ou vai pro NotebookLM
#pendente      — Precisa de ação
#arquivado     — Não é mais relevante
```

## Fluxos de Trabalho

### Fluxo 1: Captura rápida
```
Usuário diz algo → Crie nota no Inbox → Aplique tags → Sugira local definitivo
```

### Fluxo 2: Sessão de trabalho
```
Início da sessão → Leia memory-log → Contextualize-se → Trabalhe → Atualize memory-log
```

### Fluxo 3: Preparar estudo no NotebookLM
```
Tema definido → Busque notas → Consolide em documento → Salve em NotebookLM/sources → Suba ao Drive se possível
```

### Fluxo 4: Gerar conteúdo
```
Tema/briefing → Busque conhecimento no vault → Gere conteúdo → Salve nota com output → Vincule fontes
```

### Fluxo 5: Revisão periódica
```
Revise Inbox → Mova notas → Atualize tags-index → Identifique notas órfãs → Sugira conexões
```

## Importante

- **Nunca responda sobre projetos ou contexto passado sem consultar o vault primeiro.** Isso é a diferença entre ser um chatbot genérico e ser o segundo cérebro do Douglas.
- **Sempre registre decisões importantes.** Se o Douglas decidir mudar uma abordagem, escolher uma tecnologia, ou definir uma estratégia, isso vira nota com type: `decisão`.
- **Prefira links internos.** Use `[[nome da nota]]` sempre que referir outra nota. Isso cria a rede de conhecimento.
- **Mantenha o memory-log atualizado.** É o que garante continuidade entre sessões.

## Módulo: Produção de Cursos — Simulador Imobiliário Próvision

O simulador de viabilidade (`simulador.html`) é a ferramenta central do app Guilherme. Os cursos serão uma aba dentro do app, voltados para **incorporadores imobiliários, contadores e profissionais do mercado imobiliário**. O objetivo é duplo: Douglas aprende o domínio enquanto produz o material que será oferecido na plataforma.

### Domínio do Simulador

O simulador cobre:

- **DRE do empreendimento**: Receita bruta (VGV), custos de terreno, obra, taxas (ITBI, INSS, emolumentos, alvará, habite-se), juros de financiamento, comissão de vendas, impostos. Calcula margem bruta e lucro líquido.
- **Fluxo de caixa mensal**: Desembolsos (equity terreno, obra linear, amortização) vs receitas (30% na planta, 40% durante obra, 30% na entrega). Suporta SAC e PRICE.
- **TIR e VPL**: Taxa Interna de Retorno mensal sobre o fluxo de equity. VPL com TMA padrão de 0,8% a.m.
- **Payback**: Mês em que o saldo acumulado vira positivo.
- **Análise tributária**: Lucro Presumido (IRPJ + CSLL + PIS + COFINS) vs SPE + RET 4% (ou RET 1% para MCMV). A Sofia (copilot IA) ajuda a otimizar.
- **Modalidades de financiamento**: Plano Empresário, Home Equity, Consórcio, MCMV/Caixa, sem financiamento. Cada uma com taxa, prazo e dinâmica própria.
- **What-If / Sensibilidade**: Simula impacto de variações no preço do terreno, preço de venda, número de unidades.
- **Estudo geográfico**: Mapa com Leaflet para análise de localização e área do terreno.

### Estrutura de Cursos no Vault

Organizar o material em `02 - Áreas/Cursos/` com subpastas por módulo:

```
02 - Áreas/Cursos/
├── _index.md                          # Ementa geral, ordem dos módulos
├── 01-Viabilidade-Financeira/
│   ├── _index.md                      # Objetivos, tópicos, público
│   ├── aula-01-o-que-e-viabilidade.md
│   ├── aula-02-dre-do-empreendimento.md
│   ├── aula-03-fluxo-de-caixa.md
│   ├── aula-04-tir-vpl-payback.md
│   └── exercicios/
├── 02-Tributacao-Imobiliaria/
│   ├── _index.md
│   ├── aula-01-lucro-presumido.md
│   ├── aula-02-spe-ret-afetacao.md
│   ├── aula-03-mcmv-tributacao.md
│   └── exercicios/
├── 03-Financiamento-de-Obra/
│   ├── _index.md
│   ├── aula-01-plano-empresario.md
│   ├── aula-02-consorcio-home-equity.md
│   ├── aula-03-juros-impacto-no-projeto.md
│   └── exercicios/
├── 04-Tutorial-Simulador/
│   ├── _index.md
│   ├── aula-01-primeiros-passos.md
│   ├── aula-02-interpretando-resultados.md
│   ├── aula-03-what-if-sensibilidade.md
│   └── exercicios/
├── 05-Analise-de-Mercado/
│   ├── _index.md
│   ├── aula-01-estudo-de-localizacao.md
│   ├── aula-02-precificacao-e-vgv.md
│   └── exercicios/
└── assets/
    ├── scripts-video/                 # Roteiros para vídeos
    └── infograficos/                  # Textos-base para infográficos
```

### Fluxo de Produção de Conteúdo para Cursos

#### 1. Aprender o conceito
- Douglas pede: "quero entender como funciona a TIR num empreendimento imobiliário"
- Claude pesquisa, explica de forma acessível, e salva a nota de aprendizado no vault
- Se NotebookLM for útil, prepara um pacote de estudo

#### 2. Produzir o material da aula
- Douglas pede: "agora transforma isso numa aula pro curso, com roteiro de vídeo e pontos pro infográfico"
- Claude gera:
  - **Nota da aula** (conceitos, exemplos, exercícios) → salva em `Cursos/Módulo/`
  - **Roteiro de vídeo** (falas, timing, o que mostrar na tela) → salva em `assets/scripts-video/`
  - **Pontos para infográfico** (dados-chave, fluxos visuais, comparações) → salva em `assets/infograficos/`

#### 3. Conectar com o simulador
- Cada aula deve ter exemplos práticos usando o simulador
- Incluir: quais campos preencher, quais resultados observar, o que interpretar
- Exemplos com números reais (terreno de R$X, Y unidades, preço de R$Z)

### Formato de Nota de Aula

```markdown
---
tags: [curso, módulo-N, aula]
created: YYYY-MM-DD
type: recurso
status: rascunho|revisão|pronto
modulo: Nome do Módulo
aula_numero: N
publico: incorporadores, contadores
formato: video, infografico
---

# Aula N: Título

## Objetivo da Aula
O que o aluno vai saber fazer ao final.

## Conceitos-Chave
Os fundamentos explicados de forma acessível.

## Exemplo Prático com o Simulador
Passo a passo usando o simulador com números reais.

## Pontos para Infográfico
- Dado visual 1
- Comparação A vs B
- Fluxo ou diagrama sugerido

## Roteiro de Vídeo
### Abertura (30s)
### Explicação (3-5 min)
### Demonstração no Simulador (3-5 min)
### Resumo (30s)

## Exercícios
1. Exercício prático usando o simulador
2. Pergunta conceitual

## Links
- [[Conceito relacionado]]
- [[Aula anterior]]
- [[Aula seguinte]]
```

### Formato de Roteiro de Vídeo

```markdown
---
tags: [curso, video-script]
created: YYYY-MM-DD
aula: [[Aula N - Título]]
duracao_estimada: X min
---

# Roteiro: Título do Vídeo

## [00:00] Abertura
**Visual**: Logo Próvision + título da aula
**Fala**: "Hoje vamos entender..."

## [00:30] Contexto
**Visual**: Infográfico com dados do mercado
**Fala**: "Quando um incorporador avalia..."

## [02:00] Demonstração
**Visual**: Tela do simulador, campo por campo
**Fala**: "Vamos preencher juntos..."
**Ação**: Mostrar input → resultado → interpretação

## [06:00] Resumo
**Visual**: Slide com 3 pontos-chave
**Fala**: "Resumindo: 1) ... 2) ... 3) ..."

## [07:00] CTA
**Visual**: Próxima aula
**Fala**: "Na próxima aula, vamos ver como..."
```

### Glossário Imobiliário

Manter um glossário em `03 - Recursos/Documentações/glossario-imobiliario.md` com os termos técnicos que aparecem no simulador e nos cursos. Isso serve tanto pro aprendizado do Douglas quanto como referência para os alunos. Termos essenciais:

- **VGV**: Valor Geral de Vendas (preço unitário × nº de unidades)
- **DRE**: Demonstração do Resultado do Exercício — P&L do empreendimento
- **TIR**: Taxa Interna de Retorno — retorno mensal sobre o equity investido
- **VPL**: Valor Presente Líquido — valor do projeto em reais de hoje
- **TMA**: Taxa Mínima de Atratividade — benchmark de comparação (padrão: 0,8% a.m.)
- **Payback**: Mês em que o saldo acumulado vira positivo
- **SPE**: Sociedade de Propósito Específico — entidade jurídica do empreendimento
- **RET**: Regime Especial de Tributação — alíquota única (4% ou 1% MCMV)
- **Lucro Presumido**: Regime tributário com presunção de 8% de lucro
- **Plano Empresário**: Financiamento de obra via banco, liberado por medições
- **SAC**: Sistema de Amortização Constante
- **PRICE**: Tabela Price — parcelas fixas
- **ITBI**: Imposto de Transmissão de Bens Imóveis
- **Habite-se**: Certificado de conclusão de obra
- **MCMV**: Minha Casa Minha Vida — programa habitacional com condições especiais
- **Patrimônio de Afetação**: Separação do patrimônio do empreendimento do incorporador

---

## Módulo: Integração com Notion — Hub da Equipe Próvision

O Notion é o **hub operacional da equipe Próvision**. Enquanto o vault do Obsidian é o cérebro pessoal do Douglas (bagunçado, exploratório, cheio de rascunhos), o workspace do Notion é a vitrine limpa e acionável onde a equipe (Douglas + Sofia Próvision + colaboradores futuros) executa o trabalho.

**Workspace alvo**: `Sofia Próvision HQ` (team id: `3352f4bd-67f8-81b3-8d28-00426aace8cf`).

### Princípio Fundamental — Obsidian ≠ Notion

Não sincronize tudo. Cada ferramenta tem seu papel:

| Obsidian (vault) | Notion (Sofia Próvision HQ) |
|---|---|
| Cérebro **pessoal** do Douglas | Hub **operacional** da equipe |
| Notas cruas, rascunhos, ideias | Itens prontos, acionáveis, revisados |
| Wikilinks, tags livres, formato flexível | Databases estruturados, propriedades fixas |
| Fonte da verdade para conhecimento | Fonte da verdade para execução |
| Nunca compartilhado | Compartilhado com a equipe |
| Memory-log pessoal do Claude | Log de decisões público pra equipe |

**Regra de ouro**: conhecimento nasce no Obsidian, amadurece lá, e **só vai pro Notion quando está pronto para a equipe agir ou consultar**. Nunca o contrário.

### Databases que devem existir no Notion

A estrutura canônica do workspace são **5 databases principais**. Se não existirem ao iniciar a integração, crie-os usando `mcp__notion-create-database` (ver "Setup Inicial" abaixo):

#### 1. 📂 Projetos
Database mestre dos projetos ativos da Próvision.

| Propriedade | Tipo | Valores / Descrição |
|---|---|---|
| Nome | title | Nome do projeto |
| Status | select | Ideia, Planejamento, Em andamento, Pausado, Concluído, Arquivado |
| Tipo | select | Produto, Cliente, Interno, Curso, Marketing |
| Owner | people | Responsável principal |
| Próxima ação | rich_text | O que precisa acontecer a seguir |
| Prazo | date | Deadline ou marco |
| Tags | multi_select | Tags livres |
| Link Obsidian | url | Caminho da nota original no vault |
| Atualizado em | last_edited_time | Auto |

Origem no vault: `01 - Projetos/<nome>/_index.md`

#### 2. ✅ Tarefas
Todas as tarefas acionáveis da equipe.

| Propriedade | Tipo | Valores / Descrição |
|---|---|---|
| Tarefa | title | Descrição da tarefa |
| Status | status | A fazer, Em progresso, Revisão, Feito, Bloqueado |
| Projeto | relation → 📂 Projetos | Projeto ao qual pertence |
| Prioridade | select | Alta, Média, Baixa |
| Responsável | people | Quem faz |
| Prazo | date | Deadline |
| Origem | select | Obsidian, Notion, Reunião, Cliente |
| Notas | rich_text | Contexto adicional |

Origem no vault: linhas `> [!TODO]` e listas `- [ ]` dentro das notas de projetos, além do `memory-log.md`.

#### 3. 🧠 Decisões
Log público de decisões tomadas.

| Propriedade | Tipo | Valores / Descrição |
|---|---|---|
| Decisão | title | Título curto da decisão |
| Data | date | Quando foi decidida |
| Projeto | relation → 📂 Projetos | Projeto impactado |
| Contexto | rich_text | Por que precisava decidir |
| Opções consideradas | rich_text | Alternativas avaliadas |
| Decisão tomada | rich_text | O que foi decidido |
| Racional | rich_text | Por que essa e não outra |
| Revisar em | date | Opcional — quando revisitar |

Origem no vault: notas com `type: decisão` e entradas de "Decisões tomadas" no memory-log.

#### 4. 📣 Conteúdo
Pipeline de conteúdo (marketing, social, blog, cursos).

| Propriedade | Tipo | Valores / Descrição |
|---|---|---|
| Título | title | Título do conteúdo |
| Tipo | select | Post LinkedIn, Post Twitter, Blog, Aula, Roteiro vídeo, Infográfico |
| Status | status | Rascunho, Em revisão, Aprovado, Agendado, Publicado |
| Canal | multi_select | LinkedIn, Twitter, Instagram, Blog, YouTube, Curso |
| Data de publicação | date | Quando vai ao ar |
| Autor | people | Quem escreveu |
| Tema | multi_select | Tributação, Viabilidade, Vibe Coding, IA, Real Estate |
| Corpo | rich_text | Rascunho ou link |

Origem no vault: `02 - Áreas/Marketing/`, `02 - Áreas/Cursos/*/`, `assets/scripts-video/`.

#### 5. 📚 Cursos (opcional, só se o escopo de cursos crescer)
Database de aulas e módulos.

| Propriedade | Tipo | Valores / Descrição |
|---|---|---|
| Aula | title | Título da aula |
| Módulo | select | 01-Viabilidade, 02-Tributação, 03-Financiamento, 04-Simulador, 05-Mercado |
| Número | number | Ordem dentro do módulo |
| Status | status | Rascunho, Revisão, Gravado, Publicado |
| Público | multi_select | Incorporadores, Contadores, Advogados |
| Roteiro | url | Link pro arquivo de roteiro |
| Duração (min) | number | Estimada |

Origem no vault: `02 - Áreas/Cursos/<módulo>/aula-*.md`

### Setup Inicial — Primeira vez usando a integração

Quando o Douglas pedir "configura a integração Notion" ou for a primeira vez que você usa o Notion nesta skill, execute:

1. **Verifique acesso**: `mcp__notion-get-teams` — confirme que `Sofia Próvision HQ` aparece.
2. **Busque databases existentes**: `mcp__notion-search` com query `"Projetos"`, depois `"Tarefas"`, etc. Se já existirem, use os existentes. Se não, crie.
3. **Crie os databases faltantes** usando `mcp__notion-create-database`. Sempre crie dentro do team `Sofia Próvision HQ` (parent).
4. **Anote os IDs** dos databases criados em `_sistema/notion-config.md` no vault:
   ```markdown
   # Notion Config — Sofia Próvision HQ
   team_id: 3352f4bd-67f8-81b3-8d28-00426aace8cf
   databases:
     projetos: <id>
     tarefas: <id>
     decisoes: <id>
     conteudo: <id>
     cursos: <id>
   ultimo_sync: YYYY-MM-DD HH:MM
   ```
5. **Crie a página "Dashboard"** no workspace com views dos databases principais (kanban de Tarefas por Status, galeria de Projetos por Status, linha do tempo de Conteúdo por Data).
6. **Registre o setup no memory-log** do vault.

> **Importante**: Se a busca por páginas voltar vazia mesmo com o team visível, significa que a integração MCP ainda não tem acesso às páginas. O Douglas precisa ir no Notion, abrir o workspace e dar permissão à integração "Notion MCP" via Settings → Connections. Avise claramente se isso acontecer.

### Fluxos de Sincronização

Todos os fluxos seguem a direção **Obsidian → Notion** por padrão. Notion → Obsidian só quando explicitamente pedido (ver Fluxo 5).

#### Fluxo 1: Publicar um projeto no Notion
Gatilho: "manda o projeto X pro Notion" / "cria o projeto X pra equipe"

1. Leia `01 - Projetos/<nome>/_index.md` e todas as notas relevantes do projeto
2. Extraia: nome, status, tipo, próxima ação, prazo, tags
3. Use `mcp__notion-create-pages` dentro do database 📂 Projetos
4. O corpo da página deve conter um resumo executivo (não o rascunho cru do vault)
5. Crie tarefas associadas automaticamente (ver Fluxo 2)
6. Volte ao `_index.md` do vault e adicione o link do Notion no frontmatter: `notion_url: <url>`
7. Registre no memory-log

#### Fluxo 2: Publicar tarefas no Notion
Gatilho: "publica essas tarefas pra equipe" / automático ao publicar um projeto

1. Colete tarefas do vault: todas as linhas `- [ ]` e blocos `> [!TODO]` da nota fonte
2. Para cada tarefa, crie uma página no database ✅ Tarefas com:
   - Título = texto da tarefa
   - Status = "A fazer"
   - Projeto = relation ao projeto no Notion (use o id guardado no notion-config.md)
   - Origem = "Obsidian"
3. No vault, marque a tarefa como publicada usando um sufixo: `- [ ] fazer X <!-- notion:<page_id> -->`
4. Isso evita duplicar na próxima sincronização

#### Fluxo 3: Publicar uma decisão
Gatilho: nota com `type: decisão` é criada ou "registra essa decisão pra equipe"

1. Leia a nota de decisão do vault
2. Extraia: título, data, projeto relacionado, contexto, opções, escolha, racional
3. Crie página no database 🧠 Decisões
4. Vincule ao projeto via relation
5. Adicione link do Notion no frontmatter da nota do vault
6. Registre no memory-log

#### Fluxo 4: Publicar conteúdo
Gatilho: rascunho de post/aula/blog pronto no vault

1. Leia a nota em `02 - Áreas/Marketing/` ou `02 - Áreas/Cursos/`
2. Identifique o tipo (post, blog, aula, roteiro)
3. Crie página no database 📣 Conteúdo com status "Rascunho"
4. Cole o corpo estruturado da nota (não o rascunho cru — limpe quebras e wikilinks internos)
5. Wikilinks do vault viram menções no Notion (se a página relacionada já existir) ou texto simples
6. Adicione link do Notion no frontmatter do vault

#### Fluxo 5: Puxar do Notion pro Obsidian (reverso)
Gatilho: "o que mudou no Notion?" / "traz as atualizações da equipe pro vault"

Este fluxo é **delicado**. Nunca sobrescreva o vault automaticamente.

1. Use `mcp__notion-fetch` nos databases principais filtrando por `Atualizado em > último_sync`
2. Para cada item alterado:
   - Se é novo (não tem correspondente no vault): crie nota em `00 - Inbox/` com tag `#from-notion` e peça ao Douglas onde organizar
   - Se é edição de item que já existe no vault: mostre o diff e pergunte se quer atualizar
3. Atualize `ultimo_sync` no `notion-config.md`
4. Registre no memory-log

#### Fluxo 6: Status report semanal
Gatilho: "me dá um status da semana pra equipe" / "prepara o report"

1. Leia o memory-log dos últimos 7 dias
2. Leia tarefas no Notion com status "Feito" nesse período (`mcp__notion-fetch`)
3. Leia projetos com status alterado
4. Monte um resumo em markdown:
   ```markdown
   ## Semana YYYY-WW — Próvision
   ### Entregas
   - ...
   ### Em andamento
   - ...
   ### Decisões
   - ...
   ### Bloqueios / atenção
   - ...
   ```
5. Salve como nota no vault em `02 - Áreas/Reports/YYYY-WW.md`
6. Publique como comentário no dashboard do Notion ou crie uma página filha do Dashboard

### Regras de Governança

Coisas que **nunca** devem ir do vault pro Notion automaticamente:

- Notas em `00 - Inbox/` (não estão prontas)
- Notas com tag `#privado`, `#dossiê-pessoal` ou status `rascunho`
- Conteúdo do `Dados Pessoais/`
- Memory-log completo (apenas extratos revisados)
- Rascunhos de decisão que ainda não foram tomadas
- Placeholders vazios (0 bytes)

Coisas que **sempre** devem ir do vault pro Notion:

- Decisões com `type: decisão` e status `tomada`
- Projetos com status `em-progresso` ou `planejamento`
- Tarefas com marcador `#equipe` ou listadas em projetos publicados
- Conteúdo com status `aprovado` ou `pronto para publicação`

### Uso do MCP do Notion — Ferramentas disponíveis

Você tem acesso a estas ferramentas via MCP. Use-as ativamente em vez de pedir pro Douglas fazer manualmente:

- `mcp__notion-get-teams` — lista workspaces/teams acessíveis
- `mcp__notion-search` — busca páginas/databases por texto
- `mcp__notion-fetch` — lê o conteúdo de uma página ou database por id
- `mcp__notion-create-database` — cria database novo
- `mcp__notion-create-pages` — cria uma ou mais páginas (em database ou workspace)
- `mcp__notion-update-page` — edita propriedades/conteúdo de uma página
- `mcp__notion-update-data-source` — altera schema de um database existente
- `mcp__notion-move-pages` — move páginas entre parents
- `mcp__notion-duplicate-page` — duplica template
- `mcp__notion-create-view` / `update-view` — cria e edita views (kanban, tabela, galeria)
- `mcp__notion-create-comment` / `get-comments` — colabora nas páginas
- `mcp__notion-get-users` — lista membros do workspace (útil pra atribuir tarefas)

**Sempre prefira batch** (criar múltiplas páginas de uma vez com `create-pages`) em vez de chamadas individuais. É mais rápido e mais barato em tokens.

### Frontmatter do vault estendido — campos Notion

Quando uma nota do vault foi sincronizada com o Notion, adicione estes campos ao frontmatter para manter a rastreabilidade:

```markdown
---
tags: [projeto, equipe]
created: 2026-04-09
type: projeto
status: em-progresso
notion_id: <page_id>
notion_url: https://www.notion.so/...
notion_sincronizado_em: 2026-04-09T13:45
notion_db: projetos
---
```

Isso permite:
- Identificar rapidamente se uma nota já está no Notion
- Fazer sincronização incremental (só atualiza o que mudou)
- Voltar à página do Notion com um clique

### Checklist antes de sincronizar qualquer coisa com o Notion

- [ ] A nota/conteúdo tem status adequado (não é rascunho cru)?
- [ ] Não tem tags de privacidade (`#privado`, `#dossiê-pessoal`)?
- [ ] O `notion-config.md` existe e tem os ids dos databases?
- [ ] O database alvo está no workspace correto (Sofia Próvision HQ)?
- [ ] Se for update de item existente, já li a versão atual no Notion pra não sobrescrever cegamente?
- [ ] Vou registrar no memory-log depois?

### Fluxo 7: Setup da primeira sincronização (one-shot)

Quando o Douglas pedir "configura tudo de uma vez" ou "faz o setup completo":

1. Rode o Setup Inicial (criar databases, salvar ids)
2. Liste todos os projetos ativos em `01 - Projetos/` — execute o Fluxo 1 pra cada um
3. Liste todas as tarefas abertas (linhas `- [ ]` sem marcador `<!-- notion:... -->`) — execute o Fluxo 2
4. Liste notas `type: decisão` com status `tomada` — execute o Fluxo 3
5. Liste conteúdo em `02 - Áreas/Marketing/` e `02 - Áreas/Cursos/` com status pronto — execute o Fluxo 4
6. Crie a página Dashboard com os widgets/views
7. Gere um relatório no final: "X projetos, Y tarefas, Z decisões, W conteúdos publicados no Notion"
8. Salve o relatório no memory-log

Este fluxo pode levar várias chamadas MCP. Não pule etapas, mas **confirme com o Douglas antes** se forem mais de ~30 itens pra publicar — melhor dividir em lotes que ele revise.

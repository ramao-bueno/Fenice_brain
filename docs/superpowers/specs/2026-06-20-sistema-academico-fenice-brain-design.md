# Design Spec — Sistema Acadêmico Fenice_bRain
## Ciências Jurídicas e Filosóficas

**Data:** 2026-06-20  
**Status:** Aprovado pelo usuário — aguardando writing-plans  
**Vault:** `C:\Fenice_bRain`  
**Princípio fundador:** Pirâmide Normativa de Kelsen + Sistema Epistêmico Jurídico-Filosófico

---

## 1. Visão e Escopo

Transformar o vault `Fenice_bRain` em uma plataforma acadêmica completa de Ciências Jurídicas e Filosóficas, com:

- Toda a legislação brasileira vigente organizada pela hierarquia kelseniana
- 1+ jurisconsulto por área do direito (Pontes, Mirabete, Godinho, etc.)
- Todos os filósofos do direito relevantes desde Montesquieu
- Plugin de navegação em dois níveis: domínio → código → artigo
- Módulo de ensino acadêmico (Univille) com método 60/30/10
- Eliminação de todas as redundâncias atuais (3 cópias paralelas → 1 estrutura canônica)
- `Fenice_Estudos` permanece vault separado e copiável por qualquer usuário

---

## 2. Arquitetura de Pastas (aprovada)

```
C:\Fenice_bRain\
│
├── _SISTEMA/                     meta: templates, guias, OAB, projetos, arquivo
│   ├── Templates/
│   ├── OAB/
│   ├── Projetos/
│   └── Arquivo/
│
├── 00_APEX/                      CF88 + emendas + princípios constitucionais
│   ├── CF88/
│   ├── Emendas/
│   └── Principios/
│
├── 01_PRIVADO/                   Direito Civil + Processual Civil + Consumidor
│   ├── Codigos/
│   │   ├── CC/                   L10406 — Código Civil (6.420 artigos)
│   │   ├── CPC/                  L13105 — CPC 2015 (3.693 artigos)
│   │   └── CDC/                  L8078 — Código de Defesa do Consumidor
│   ├── Jurisprudencia/           STJ + STF civil
│   ├── Doutrina/
│   └── Revisao/                  60/30/10 flashcards + mapas
│
├── 02_PENAL/                     Direito Penal + Processual Penal
│   ├── Codigos/
│   │   ├── CP/                   DEL2848 — Código Penal (363 artigos atomizados)
│   │   │   └── DEL2848/          artigos individuais (DEL2848 Art. N.md)
│   │   ├── CPP/                  DEL3689 — Código Processo Penal
│   │   └── Especial/             L7210 (LEP), L9099, L13964 (Anticrime), L13869
│   ├── Jurisprudencia/
│   ├── Doutrina/
│   └── Revisao/
│
├── 03_PUBLICO/                   Admin + Tributário + Previdenciário + Ambiental
│   ├── Codigos/
│   │   ├── Admin/                L8112, L9784, L8429 (Improbidade)
│   │   ├── Tributario/           CTN (L5172)
│   │   ├── Previdenciario/       L8213, L8742
│   │   └── Ambiental/            L9605, L12651
│   ├── Jurisprudencia/
│   ├── Doutrina/
│   └── Revisao/
│
├── 04_TRABALHO/                  CLT + Processo Trabalhista + Previdência
│   ├── Codigos/
│   │   ├── CLT/                  DEL5452
│   │   └── ProcessualTrabalhista/
│   ├── Jurisprudencia/           TST
│   ├── Doutrina/
│   └── Revisao/
│
├── 05_ESPECIAL/                  Microssistemas legislativos
│   ├── Codigos/
│   │   ├── ECA/                  L8069
│   │   ├── LGPD/                 L13709
│   │   ├── MariadaPenha/         L11340
│   │   ├── StatutoIdoso/         L10741
│   │   └── Anticorrupcao/        L12846
│   ├── Jurisprudencia/
│   └── Revisao/
│
├── 06_JURISCONSULTOS/            Doutrinadores por área — modal próprio (Ctrl+Shift+J)
│   ├── PRIVADO/
│   │   ├── Pontes-de-Miranda/    Francisco Cavalcanti Pontes de Miranda
│   │   ├── Caio-Mario/           Caio Mário da Silva Pereira
│   │   └── Orlando-Gomes/        Orlando Gomes
│   ├── PENAL/
│   │   ├── Mirabete/             Julio Fabbrini Mirabete
│   │   ├── Rogerio-Sanches/      Rogério Sanches Cunha
│   │   └── Nucci/                Guilherme de Souza Nucci
│   ├── PUBLICO/
│   │   ├── Celso-Mello/          Celso Antônio Bandeira de Mello
│   │   └── Hely-Lopes/           Hely Lopes Meirelles
│   ├── TRABALHO/
│   │   ├── Godinho/              Maurício Godinho Delgado
│   │   └── Volia-Bomfim/         Vólia Bomfim Cassar
│   └── METODOLOGIA/
│       └── Zendelski/            Método PKM jurídico
│
├── 07_FILOSOFIA/                 Fundamentos filosóficos — modal próprio (Ctrl+Shift+F)
│   ├── Antigos/
│   │   ├── Aristoteles/
│   │   └── Cicero/
│   ├── Iluministas/              séc. XVII–XVIII
│   │   ├── Montesquieu/          Do Espírito das Leis
│   │   ├── Locke/                Dois Tratados do Governo
│   │   ├── Rousseau/             Contrato Social
│   │   └── Voltaire/
│   ├── Modernos/                 séc. XIX
│   │   ├── Kant/                 Metafísica dos Costumes
│   │   ├── Hegel/
│   │   └── Marx/
│   ├── Contemporaneos/           séc. XX–XXI
│   │   ├── Kelsen/               Teoria Pura do Direito
│   │   ├── Hart/                 O Conceito de Direito
│   │   ├── Dworkin/              Levando os Direitos a Sério
│   │   ├── Rawls/                Uma Teoria da Justiça
│   │   └── Habermas/             Direito e Democracia
│   └── Penalistas/               Escola Clássica + Positivista
│       ├── Beccaria/             Dos Delitos e das Penas (já em Fenice_Estudos)
│       ├── Ferri/                Sociologia Criminal
│       └── Garofalo/             Criminologia
│
├── 08_ENSINO/                    Academia — estrutura copiável
│   └── Univille/
│       ├── _Curriculo.md         grade completa: concluídas + pendentes
│       ├── Semestre-01_Concluido/
│       │   └── [materia]/
│       │       ├── _60-Questoes/
│       │       ├── _30-Teoria/
│       │       └── _10-Revisao/
│       ├── Semestre-02_Concluido/
│       ├── Semestre-03_Em-Curso/
│       └── Semestre-XX_Futuro/
│
├── 09_FENICE_BRAIN/              Sistema PKM + metodologia + Graph
│   ├── Metodologia/
│   ├── Templates/
│   └── Sistema/
│
└── scripts/                      extratores, backup, pipeline Planalto
    ├── backend-python/
    ├── backup/
    └── jurisprudencia/
```

---

## 3. Plugin — Navegação em Dois Níveis (aprovada)

### Fluxo principal (Ctrl+Shift+B)

```
[Ctrl+Shift+B]
    └── DomainModal
        ├── 🏛️  00 · Constituição Federal
        ├── 📘  01 · Direito Privado        → CodigoModal (CC, CPC, CDC)
        ├── 🔒  02 · Direito Penal          → CodigoModal (CP, CPP, Especial)
        ├── 🏢  03 · Direito Público        → CodigoModal (Admin, CTN, Prev)
        ├── 💼  04 · Direito do Trabalho    → CodigoModal (CLT)
        └── 🛡️  05 · Legislação Especial    → CodigoModal (ECA, LGPD, ...)
            └── NumeroModal → InfoModal (sem mudança)
```

### Novos atalhos

| Atalho | Modal | Destino |
|---|---|---|
| `Ctrl+Shift+B` | DomainModal → CodigoModal | artigos jurídicos |
| `Ctrl+Shift+I` | InfoModal atual | mantém comportamento v21 |
| `Ctrl+Shift+J` | JurisconsultoModal | área → doutrinador → INDEX.md |
| `Ctrl+Shift+F` | FilosofoModal | era → filósofo → INDEX.md |

### JurisconsultoModal e FilosofoModal

Dois níveis: categoria → seleção → `openFile(INDEX.md)` + inject Copilot context.  
Mesmo mecanismo do v21 (`getLeaf(false).openFile(found)`).

---

## 4. Migração — Estratégia (aprovada)

### Redundâncias identificadas

| Localização | Arquivos | Decisão |
|---|---|---|
| `Fenice bRain/` (subfolder) | 13.645 | ✅ Fonte canônica — mover para nova estrutura |
| `⚖️ Direito Civil/` + raiz | ~4.900 | ⚠️ Mesclar exclusivos → eliminar |
| `02 - Áreas/Base Jurídica/` | 4.059 | ⚠️ Subconjunto → eliminar após mescla |

### Fases

```
FASE 1  Criar estrutura de pastas nova (sem mover nada)
FASE 2  Mover Fenice bRain/ → domínios (fonte canônica)
FASE 3  Mesclar pastas ⚖️ raiz (verificar exclusivos → mover → deletar)
FASE 4  Consolidar 02 - Áreas/ → deletar
FASE 5  Consolidar pastas numeradas (00-Inbox a 06-NotebookLM) → _SISTEMA/
FASE 6  Atualizar plugin: array CODIGOS em main.js (novos paths)
FASE 7  Atualizar scripts: paths de extratores e backup
FASE 8  git commit estrutural
FASE 9  Verificar wikilinks no Obsidian (Graph View + broken links)
FASE 10 Testar plugin completo (DomainModal + todos os códigos)
```

### Risco de wikilinks

Obsidian resolve por **nome de arquivo**, não por path. Arquivos com nomes únicos  
(ex: `DEL2848 Art. 121.md`) sobrevivem à migração sem quebra. Arquivos genéricos  
(`INDEX.md`, `README.md`) precisam de verificação manual na Fase 9.

---

## 5. Método 60/30/10 no Módulo Ensino

Cada matéria dentro de `08_ENSINO/Univille/Semestre-N/[materia]/` segue:

| Pasta | % | Conteúdo |
|---|---|---|
| `_60-Questoes/` | 60% | Questões da banca, lei seca, jurisprudência aplicada |
| `_30-Teoria/` | 30% | Doutrina, videoaulas resumidas, PDFs processados |
| `_10-Revisao/` | 10% | Flashcards, mapas mentais, resumos próprios |

---

## 6. Fenice_Estudos — Vault Pessoal Copiável

- Permanece em `C:\Fenice_Estudos\` como vault Obsidian separado
- Segue a mesma estrutura de navegação (plugin instalado com DomainModal)
- Qualquer usuário pode clonar e criar sua instância pessoal
- Conteúdo de Beccaria/Filosofia Penal já existe (14 notas copiadas em 2026-06-20)
- Conteúdo Univille migra de `Fenice_Estudos/` para `08_ENSINO/Univille/` no vault principal

---

## 7. Skills Necessárias para Implementação

| Skill | Propósito |
|---|---|
| `superpowers:writing-plans` | Plano de implementação detalhado por fase |
| `superpowers:subagent-driven-development` | Executar fases em paralelo (migração) |
| `superpowers:systematic-debugging` | Debugging do plugin durante refactoring |
| `atomizar-juridico` (projeto) | Geração de notas atômicas para novos conteúdos |
| `superpowers:verification-before-completion` | Verificar cada fase antes de avançar |

---

## 8. Decisões Abertas (para próxima sessão)

1. **Nomenclatura de arquivos INDEX** — usar `INDEX.md` ou `_INDEX.md` para evitar conflito de wikilinks?
2. **Versão do plugin** — DomainModal = v22? Ou numeração semântica (v2.0.0)?
3. **Pipeline Planalto** — após migração, scripts de extração precisam de novos paths. Prioridade?
4. **Jurisconsultos — conteúdo inicial** — gerar notas atômicas para Pontes, Mirabete, Kelsen nas primeiras 3 áreas?
5. **Graph View** — filtro padrão após migração (sugestão: `path:02_PENAL` para testes iniciais)

---

*Spec elaborada em sessão 2026-06-20 — aprovada pelo usuário para avançar ao writing-plans.*

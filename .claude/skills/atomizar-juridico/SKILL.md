---
name: atomizar-juridico
description: Use sempre que o usuário colar um texto jurídico bruto (julgado do STF/STJ, capítulo de doutrina — Zendelski, Reale, Pontes de Miranda —, Instrução Normativa, ou artigo de lei) e pedir para "atomizar", "transformar em notas", "processar para o vault" ou "gerar notas do Fenice bRain". Converte o bruto em notas atômicas interligadas no padrão Obsidian, prontas para salvar no vault FENICE bRain.
---

# Atomizador Jurídico — Motor de Arquitetura de Conhecimento do Fenice bRain

Você atua como o motor de arquitetura de conhecimento do **Fenice bRain**: processa dados brutos do
ecossistema jurídico brasileiro (doutrina, jurisprudência, leis secas, instruções normativas) e os
transforma em estruturas de conhecimento atômicas, hiperconectadas e prontas tanto para consumo
acadêmico (Obsidian/PKM, método [[project_fenice_metodologia_pkm|Zendelski]]) quanto algorítmico (RAG/Supabase).

## Antes de gerar o output: pondere as 4 variáveis

Analise o texto bruto sob a perspectiva de interdependência total do direito:

1. **Nível de abstração** — Dogmática Pura (Princípios), Lei Seca (Regra), Processual (Rito) ou
   Administrativo (Operação/IN)?
2. **Entidades acessórias** — Quem é o autor/jurisconsulto ou tribunal emissor? Qual o peso
   político/doutrinário desta posição?
3. **Co-dependência obrigatória** — Esta regra ou tese existe no vácuo? (Ex.: uma tese
   previdenciária depende de qual rito do CPC? Uma IN regulamenta qual artigo do CC ou de qual
   Lei Federal?)
4. **Impacto comercial/pragmático** — Como essa tese ou regra altera o fluxo de caixa de uma
   empresa, o risco de um processo ou a captação de um lead?

## Output: estruture em 3 seções modulares (The Atomic Vault)

Gere o conteúdo simulando arquivos Markdown prontos para o Obsidian, usando `[[Links]]` —
sempre em **notas atômicas** (1 conceito = 1 nota, nunca um bloco com vários dispositivos).

### 1. Notas Atômicas (The Micro-Concepts)
Quebre o texto em conceitos únicos. Cada um vira o nome de uma nota individual:

```
#### [[Nome_da_Nota]]
- **Conceito Direto:** definição em frase simples e pragmática
- **Fundamentação Positiva:** artigo da lei, súmula ou IN exata que ancora isso
- **Anotação de Jurisconsulto:** (se aplicável) como o pensador X expande ou critica este ponto
```

### 2. Mapeamento Relacional (The Zendelski Graph)
Crie os cabos de conexão — linke as notas criadas com os blocos fundamentais do Direito Brasileiro:
- **Conexão de Direito Material:** como isso se conecta com `[[Código Civil]]`,
  `[[Direito Previdenciário]]`, `[[CDC]]` etc.
- **Conexão de Direito Processual:** como isso é levado a juízo via `[[CPC]]`,
  `[[Juizados Especiais Federais]]`?
- **Conexão Operacional:** qual `[[Instrução Normativa]]` ou sistema (`[[INSS]]`,
  `[[ComprasGov]]`...) rege a operação prática disso?

### 3. Vetor de Negócio e Risk Assessment
A tradução em dinheiro e segurança:
- **Ação Comercial:** como um advogado ou empresa usa essa nota para gerar receita ou se
  defender imediatamente?
- **Gatilho de Automação:** qual lógica IF/ELSE essa nota gera num sistema de software
  (ex.: "Se data do fato > X, então prazo é Y")?

## Onde salvar no vault (mapeamento de destino)

Depois de gerar o conteúdo, oriente o usuário (ou salve, se solicitado) seguindo a árvore atual:

| Tipo de conteúdo | Destino sugerido |
|---|---|
| Lei seca (artigo de código) | `0X_.../<RAMO>/Artigos/` correspondente ao código |
| Jurisprudência (julgado, tese, súmula) | `03_PROCESSO_CIVIL/JURISPRUDENCIA/` ou `STF_SUMULAS/` |
| Doutrina / nota de jurisconsulto | `09_REFERENCIAS/MAESTROS/<Nome-do-Jurista>/` |
| Instrução Normativa / operacional | pasta do ramo afetado, com tag `instrucao-normativa` |

## Por que isso importa (não repita ao usuário, é o racional do método)

- **Pronto para RAG:** conceitos isolados sem ruído entram limpos para vetorização/busca semântica.
- **Automação de arquivos:** o output pode ser cuspido direto em `.md` no vault (via n8n ou script).
- **Escalável para jurisconsultos:** ao processar Pontes de Miranda, Reale, Zendelski etc., a tese
  de cada um se amarra diretamente ao artigo de lei seca ou IN já mapeados — fortalecendo o
  Graph View ("cérebro digital") em vez de só organizar pastas.

## Lembrete de padrão (frontmatter YAML)

Ao gerar notas atômicas completas (não apenas o esqueleto acima), inclua frontmatter no padrão
do vault: `tags`, `relacionados` (lista que vira wikilinks) e, quando for jurisprudência/súmula,
o campo de vigência temporal (`status: vigente|superada|modulada`, `vigencia_inicio`,
`vigencia_fim`, `norma_sucessora`) — esse é o gap de "leis vivas no tempo" que o projeto ainda
não resolveu estruturalmente.

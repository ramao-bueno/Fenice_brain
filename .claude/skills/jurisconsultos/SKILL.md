---
name: jurisconsultos
description: Use when analyzing any legal topic, drafting arguments, or producing legal content — grounds every analysis in the thinking of the jurisconsultos registered in the Fenice bRain vault, automatically selecting the right scholar for the area of law being discussed.
---

# Jurisconsultos — Análise Jurídica Fundamentada nos Mestres do Vault

## Princípio

Toda análise jurídica produzida no Fenice bRain deve ser ancorada no pensamento dos
jurisconsultos registrados no vault. Não se analisa uma norma no vácuo: ela é lida
através dos olhos de quem a construiu, criticou ou sistematizou.

**Regra de ouro:** para cada tema jurídico abordado, identificar o jurisconsulto mais
relevante da área, ler seu perfil no vault (`06_JURISCONSULTOS/`) e fundamentar a
análise no seu PENSAMENTO CENTRAL.

---

## Mapa de Jurisconsultos por Área

### Direito Constitucional
| Jurisconsulto | Pensamento central | Vault |
|---|---|---|
| **Luís Roberto Barroso** | Neoconstitucionalismo, ponderação de princípios, ativismo judicial moderado | `06_JURISCONSULTOS/Constitucional/Luís Roberto Barroso.md` |
| **Gilmar Mendes** | Controle de constitucionalidade, proporcionalidade, mandado de injunção | `06_JURISCONSULTOS/Constitucional/Gilmar Mendes.md` |
| **José Afonso da Silva** | Positivismo constitucional clássico, força normativa da CF/88 | `06_JURISCONSULTOS/Constitucional/José Afonso da Silva.md` |
| **Alexandre de Moraes** | Democracia, direitos fundamentais, Direito Constitucional dogmático | `06_JURISCONSULTOS/Constitucional/Alexandre de Moraes.md` |

### Direito Civil
| Jurisconsulto | Pensamento central | Vault |
|---|---|---|
| **Pontes de Miranda** | Três planos (existência/validade/eficácia), fatos jurídicos, pandectismo | `06_JURISCONSULTOS/Civil/Pontes de Miranda.md` |
| **Caio Mário da Silva Pereira** | Direito civil sistemático, responsabilidade civil, contratos | `06_JURISCONSULTOS/Civil/Caio Mário da Silva Pereira.md` |
| **Maria Helena Diniz** | Positivismo normativo, teoria das normas, conflito de leis | `06_JURISCONSULTOS/Civil/Maria Helena Diniz.md` |
| **Orlando Gomes** | Contratos, obrigações, modernização do direito civil | `06_JURISCONSULTOS/Civil/Orlando Gomes.md` |
| **Clóvis Beviláqua** | CC/1916, positivismo oitocentista, raízes do direito civil brasileiro | `06_JURISCONSULTOS/Civil/Clóvis Beviláqua.md` |

### Direito Penal
| Jurisconsulto | Pensamento central | Vault |
|---|---|---|
| **Rogério Greco** | Finalismo, garantismo, direito penal mínimo, teoria tripartida | `06_JURISCONSULTOS/PENAL/Rogério Greco.md` |
| **Guilherme de Souza Nucci** | Prática penal, dosimetria, processo penal integrado | `06_JURISCONSULTOS/PENAL/Guilherme de Souza Nucci.md` |
| **Nelson Hungria** | Dogmática clássica, CP/1940, comentários históricos | `06_JURISCONSULTOS/PENAL/Nelson Hungria.md` |
| **Damásio E. de Jesus** | Teoria bipartida, direito penal concursos, difusão doutrinária | `06_JURISCONSULTOS/PENAL/Damásio E. de Jesus.md` |
| **Fernando Capez** | Direito penal objetivo, prova processual penal, concursos | `06_JURISCONSULTOS/PENAL/Fernando Capez.md` |

### Direito Processual Civil
| Jurisconsulto | Pensamento central | Vault |
|---|---|---|
| **Fredie Didier Jr.** | CPC/2015, processo cooperativo, teoria geral do processo | `06_JURISCONSULTOS/Processual/Fredie Didier Jr..md` |
| **Cândido Rangel Dinamarco** | Instrumentalidade do processo, acesso à justiça | `06_JURISCONSULTOS/Processual/Cândido Rangel Dinamarco.md` |
| **Humberto Theodoro Jr.** | Processo civil clássico, execução, tutela de urgência | `06_JURISCONSULTOS/Processual/Humberto Theodoro Jr..md` |

### Direito Tributário
| Jurisconsulto | Pensamento central | Vault |
|---|---|---|
| **Roque Antonio Carrazza** | ICMS, legalidade tributária, competência tributária | `06_JURISCONSULTOS/Tributario/Roque Antonio Carrazza.md` |
| **Sacha Calmon Navarro Coêlho** | Obrigação tributária, CTN, tributação e direitos fundamentais | `06_JURISCONSULTOS/Tributario/Sacha Calmon Navarro Coêlho.md` |

### Teoria Geral / Filosofia do Direito
| Jurisconsulto | Pensamento central | Vault |
|---|---|---|
| **Hans Kelsen** | Positivismo puro, norma fundamental, hierarquia normativa | `06_JURISCONSULTOS/Teoria Geral/Hans Kelsen.md` |
| **Miguel Reale** | Teoria tridimensional (fato/valor/norma), base filosófica do CC/2002 | `06_JURISCONSULTOS/Teoria Geral/Miguel Reale.md` · `07_FILOSOFIA/MAESTROS/Miguel-Reale/` |
| **Mateus Zendelski** | Método PKM jurídico, grafo de conhecimento, epistemologia aplicada | `06_JURISCONSULTOS/Teoria Geral/Mateus Zendelski.md` · `07_FILOSOFIA/MAESTROS/Mateus-Zendelski/` |

---

## Protocolo de Análise Fundamentada

Ao analisar qualquer tema jurídico com esta skill ativa:

1. **Identificar a área** — de qual ramo do direito se trata
2. **Selecionar o(s) jurisconsulto(s)** — usar o mapa acima; temas interdisciplinares usam 2–3 autores
3. **Ler o perfil no vault** — `mcp__mcpvault__read_note` no caminho correspondente
4. **Fundamentar no PENSAMENTO CENTRAL** — a análise nasce da teoria do autor, não de generalidades
5. **Citar com precisão** — obra + edição + posição doutrinária

### Formato de output para análise com jurisconsulto

```markdown
## Análise sob a ótica de [Nome do Jurisconsulto]

> [!QUOTE] [Nome] — [Obra principal, ed.]
> "[citação ou paráfrase fiel da tese]"

**Aplicação ao caso:**
[Como a teoria do autor incide sobre o problema concreto]

**Ponto de tensão com a posição majoritária:**
[Se houver divergência doutrinária relevante]

**Conexões no vault:**
[[Artigo X]] · [[Obra Y]] · [[Jurisconsulto Z]]
```

---

## Combinação com Outras Skills

| Situação | Combinar com |
|---|---|
| Análise com lente filosófica (Kelsen, Gadamer...) | [[SuperpowerFenice-05]] `/fenice-ia-02` |
| Gerar citação ABNT da obra do jurisconsulto | [[SuperpowerFenice-07]] `/fenice-ia-04` |
| Atomizar trecho de obra para o vault | [[SuperpowerFenice-03]] `/atomizar-juridico` |
| Detectar se a tese entra em conflito com norma | [[SuperpowerFenice-06]] `/fenice-ia-03` |

---

## Quando há divergência doutrinária

Se dois jurisconsultos do vault sustentam posições opostas sobre o mesmo tema:

```markdown
> [!TIP] Posição majoritária
> [Autor A] defende que... (fundamento)

> [!WARNING] Posição minoritária / divergente
> [Autor B] critica, argumentando que... (fundamento)

> [!NOTE] Posição do STF/STJ
> O tribunal segue... (súmula ou acórdão paradigmático)
```

---

## Adicionar novo jurisconsulto ao vault

Quando encontrar obra nova relevante, salvar usando o frontmatter padrão:

```yaml
---
nome: Nome Completo
area: [constitucional | civil | penal | processual | tributario | teoria-geral]
periodo: "AAAA–AAAA ou AAAA–"
obra_principal: "Título da obra principal"
tags: [jurisconsulto, area-do-direito]
created: AAAA-MM-DD
---
```

Destino: `06_JURISCONSULTOS/[Área]/Nome Completo.md`
Após salvar, rodar gatekeeping com `python scripts/llm-wiki/check_source.py`

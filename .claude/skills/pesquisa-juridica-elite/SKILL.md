---
name: pesquisa-juridica-elite
description: Framework de pesquisa jurídica de ponta — tiers de qualidade de fontes, mapeamento US/BR, protocolo GIGO para o LLM Wiki e antídoto ao falso empirismo jurídico
---

# Pesquisa Jurídica de Ponta — Framework Fenice bRain

## Propósito

Garantir que toda ingestão de conhecimento jurídico no vault e no LLM Wiki passe pelo mesmo
crivo de qualidade que os grandes players internacionais adotam. A análise abaixo mapeia o
estado da arte americano para o contexto brasileiro e define os tiers de fontes aceitas no
Fenice bRain.

## Quando usar

- Antes de ingerir qualquer fonte no LLM Wiki (`06_JURISCONSULTOS/`, `07_FILOSOFIA/`)
- Ao recomendar fontes de pesquisa para o usuário
- Ao avaliar a qualidade de um argumento jurídico ou doutrinário
- Ao construir prompts de grounding para os endpoints `/analisar` e `/hermeneutica`

---

## Mapa de Mercado — US vs Brasil

### Tier 1 — Pesquisa Primária (custo alto, qualidade máxima)

| Plataforma US             | Equivalente BR                        | Diferencial                                         |
|---------------------------|---------------------------------------|-----------------------------------------------------|
| **Westlaw Precision**     | LexML + Diário Oficial                | West Key Number System → Classificação sistemática |
| **Lexis+**                | JusBrasil Pro / Migalhas Premium      | Analytics preditivo, fluxo de trabalho integrado   |
| **Bloomberg Law**         | — (sem equivalente pleno)             | Integra dados de mercado + pesquisa jurídica        |

> **Regra operacional:** Para o Fenice bRain, o equivalente ao Tier 1 é **Supabase FTS sobre
> legislação federal** + **STJ/STF em PDF canônico**. Trata como fonte primária somente o
> texto oficial (Planalto, DOU, Portal STF/STJ).

### Tier 2 — Estudo Estruturado (foco educacional/analítico)

| Plataforma US | Equivalente BR              | Uso no Fenice bRain                            |
|---------------|-----------------------------|------------------------------------------------|
| **Quimbee**   | Gran Cursos / Estratégia    | Case briefs → Resumos de jurisprudência OAB    |
| LII Cornell   | Planalto + IDP open         | Livre, confiável para legislação e conceitos   |
| Justia        | JusBrasil free / Conjur     | Agregador de jurisprudência com sumários       |

> **Atenção:** Quimbee e equivalentes BR são ótimas para UX de estudo rápido, mas **não são
> fontes primárias**. Nunca citar como doutrina. Usar como índice para localizar a fonte
> canônica.

---

## Tiers de Qualidade para o LLM Wiki (GIGO Protocol)

### ACEITO — Fontes canônicas

```
Tier A — Primária:
  ✅ Obra doutrinária completa (Kelsen, Pontes, Barroso) com ISBN
  ✅ Texto legal oficial (Planalto, Diário Oficial, DOJ)
  ✅ Voto paradigmático do STF/STJ na íntegra (PDF oficial)
  ✅ Artigo revisado por pares (RT, RBDP, Doutrinas Essenciais)
  ✅ Verbete da Stanford Encyclopedia of Philosophy ou IEP

Tier B — Comentário qualificado:
  ✅ Prefácio/apresentação de obra canônica por especialista identificado
  ✅ Manual universitário com ISBN (Didier, Marinoni, Alexandrino & Paulo)
  ✅ Súmula STJ/STF (já no vault — 674 STJ + 736 STF)
```

### REJEITADO — Fontes GIGO

```
  ❌ Resumos de cursinho (OAB/concurso) — simplificam, omitem nuances, erro frequente
  ❌ Apostilas sem autoria identificável — sem validação editorial
  ❌ Posts de blog sem referência à fonte primária
  ❌ Transcrições de videoaulas — ruído alto, repetição, informalidade
  ❌ Wikipedia para teses doutrinárias (ok para dados biográficos)
  ❌ "Frases famosas" descontextualizadas — frequentemente apócrifas
  ❌ Podcasts / transcrições de áudio — perda de precisão conceitual
  ❌ PDFs sem autoria ou data — origem não rastreável
```

---

## Protocolo de Gatekeeping (checklist antes de ingerir)

Antes de rodar qualquer ingestão no LLM Wiki, verificar **todos** os itens:

1. **Autoria verificável?**
   - Nome completo + filiação institucional OU ISBN/DOI publicado
   - Se não → `status: rejeitado`

2. **Tipo de fonte declarado?**
   - Primária (obra do próprio jurista/filósofo)
   - Comentário qualificado (especialista reconhecido comentando a obra)
   - Compilação editorial (aceita com reservas — marcar como `tipo: compilacao`)

3. **Trecho ou obra completa?**
   - Trecho → registrar como `cobertura: parcial` no `log.md`
   - Obra completa → `cobertura: canonica`

4. **Já foi ingerido?**
   - Conferir `log.md` do módulo
   - Duplicação cria drift no wiki → `status: duplicado`

5. **Relevância para o módulo?**
   - `06_JURISCONSULTOS/` → direito brasileiro, teoria e prática
   - `07_FILOSOFIA/` → filosofia do direito, ética, epistemologia jurídica
   - Se não pertence → indicar módulo correto

---

## Aplicação no Fenice bRain — Grounding Jurídico

Quando construir prompts para `/analisar` ou `/hermeneutica`, priorizar fontes na seguinte ordem:

```
1. Legislação federal indexada (Supabase FTS) — fonte primária nacional
2. Súmulas STJ/STF do vault — jurisprudência consolidada
3. Doutrina Tier A ingerida no LLM Wiki — teoria fundamentada
4. Doutrina Tier B como apoio — contextualização
```

**Nunca** injetar como contexto de grounding materiais Tier rejeitado. O LLM amplifica o que
entra — GIGO produz respostas com ar de autoridade e base frágil.

---

## Análise de Inteligência de Mercado (visão para o produto Fenice)

Para desenvolvimento de ferramentas de IA ou engenharia jurídica, o que o mercado US ensina:

- **Westlaw e LexisNexis** ditam o padrão técnico de dados da indústria
  → Fenice equivalente: FTS sobre base oficial Planalto + STJ/STF
- **Quimbee** dita a melhor UX para consumo rápido de conhecimento
  → Fenice equivalente: landing page + endpoint `/buscar` gratuito
- **LII Cornell** prova que o modelo open-source é viável e confiável
  → Fenice equivalente: vault Obsidian público + API free tier

O diferencial competitivo do Fenice está na **integração** desses três modelos:
acervo canônico (Westlaw-like) + UX de consumo rápido (Quimbee-like) + base open (LII-like).

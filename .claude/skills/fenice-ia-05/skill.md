---
name: fenice-ia-05
description: Pareto Jurídico — camada de entrega 80/20 aplicada sobre qualquer análise ou estudo já produzido. Quando ativada, refomata o relatório final destacando o que é crítico memorizar para prova vs. o que é contexto enriquecedor. NÃO substitui a análise filosófica ou jurídica — adiciona um filtro de prioridade sobre ela. O usuário escolhe este modo na hora da entrega.
---

# Fenice IA 05 — Pareto Jurídico (Camada de Entrega)

## Propósito

Esta skill é um **filtro de saída**, não uma análise independente.

Ela é aplicada **sobre** qualquer estudo, relatório ou análise já produzida, reorganizando a entrega em dois blocos:

1. **🔴 CRÍTICO PARA PROVA** — o que o usuário DEVE memorizar (os 20% que geram 80% dos acertos)
2. **📚 CONTEXTO ENRIQUECEDOR** — o restante da análise (compreensão profunda, filosofia, hermenêutica)

A análise filosófica, jurisprudencial e hermenêutica **continua completa** — o Pareto apenas organiza a entrega de forma estratégica para quem tem uma prova pela frente.

---

## Quando Ativar

Esta camada é ativada **na hora da entrega**, quando o usuário escolher:

> *"Quero o modo Fenice Pareto"* / *"entrega para prova"* / *"filtra o que cai mais"*

Ou quando o contexto indicar claramente que o usuário está estudando para:
- Concurso público (qualquer cargo)
- OAB 1ª ou 2ª fase
- Prova acadêmica (graduação, pós-graduação)
- Exame de proficiência jurídica

---

## Como Oferecer ao Usuário (Protocolo de Entrega)

Ao final de qualquer análise ou estudo produzido, **sempre oferecer a escolha**:

```
─────────────────────────────────────
📋 MODO DE ENTREGA — escolha um:

[A] Análise completa (padrão Fenice)
    Profundidade filosófica + jurisprudencial + hermenêutica

[B] Fenice Pareto ⚡ (otimizado para prova)
    Mesma análise reorganizada: crítico primeiro, contexto depois
    Ideal para: concurso | OAB | exame acadêmico

─────────────────────────────────────
```

Se o usuário escolher **[B]**, aplicar o filtro Pareto sobre o conteúdo já produzido.

---

## Estrutura do Relatório em Modo Pareto

Quando ativado, reformatar o estudo produzido no seguinte formato:

```markdown
## ⚡ Fenice Pareto — [Tema]

### 🔴 CRÍTICO PARA PROVA (memorizar)
> Os 20% que geram 80% dos acertos

- **[Conceito 1]** — [definição em 1 linha]
- **[Conceito 2]** — [definição em 1 linha]
- **[Artigo X]** — [o que diz + ponto de prova]
- **Pegadinha clássica:** [o erro mais cobrado sobre este tema]
- **Palavra-chave banca [CESPE/FGV/etc]:** [como a banca enuncia]

---

### 📚 CONTEXTO ENRIQUECEDOR (compreensão profunda)
> Os 80% restantes — enriquecem, mas não são cobrados diretamente

[Análise filosófica completa, hermenêutica, jurisprudência de contexto,
debates doutrinários, visão histórica — tudo que foi produzido na análise padrão]

---

### 🎯 REVISÃO RÁPIDA (Ebbinghaus)
> Para revisar em 5 minutos antes da prova

1. [Ponto 1 em 1 linha]
2. [Ponto 2 em 1 linha]
3. [Ponto 3 em 1 linha]
```

---

## Scoring Pareto — Como Decidir o que é 🔴 CRÍTICO

Para classificar cada elemento da análise:

```
CRÍTICO quando:
  ✓ Aparece em provas há mais de 3 anos consecutivos
  ✓ Está em súmula vinculante ou enunciado de jurisprudência consolidada
  ✓ É a "pegadinha" clássica da banca
  ✓ Bancas CESPE/FGV costumam usar como distrator
  ✓ Está expressamente no edital como ponto cobrado

CONTEXTO quando:
  ✓ É debate doutrinário sem posição consolidada
  ✓ É exceção de exceção raramente cobrada
  ✓ É história da norma sem impacto na questão atual
  ✓ É lente filosófica para interpretação (Kelsen, Gadamer etc.) —
    enriquece a compreensão, mas não é cobrada literalmente
```

---

## Integração com as Outras Skills Fenice IA

Esta skill se encaixa **após** as demais, na camada de entrega:

```
fenice-ia-01 (Túnel do Tempo)    ─┐
fenice-ia-02 (Filtro Epistemológico) ─┤→ Análise produzida → fenice-ia-05 (Pareto)
fenice-ia-03 (Antinomias)        ─┤                          ↓
fenice-ia-04 (Fichamento ABNT)   ─┘                    Entrega organizada
                                                        para prova ou pesquisa
```

---

## Integração com Vault Fenice bRain

Quando gerar relatório Pareto de um tema do vault:

1. Criar nota em `08_ENSINO/PARETO_{tema}_{data}.md`
2. Usar frontmatter:
```yaml
---
titulo: Pareto — Dosimetria da Pena CP
tema: CP_Art59
modo: fenice-pareto
banca: CESPE
data_prova: 2026-10-15
criticos: 5
tags: [pareto, fenice-ia-05, concurso]
---
```
3. Wikilink para a nota de estudo original: `Veja análise completa: [[CP/Art_59_dosimetria]]`

---

## Exemplo de Aplicação

**Contexto:** Usuário pediu análise do Art. 59 CP (dosimetria da pena).  
A análise Fenice padrão foi entregue com profundidade filosófica (Kelsen + teleologia penal).  
O usuário opta por **[B] Fenice Pareto** para a prova de Delegado.

**Saída:**

```markdown
## ⚡ Fenice Pareto — Art. 59 CP (Dosimetria)

### 🔴 CRÍTICO PARA PROVA

- **8 circunstâncias judiciais** — culpabilidade, antecedentes, conduta social,
  personalidade, motivos, circunstâncias, consequências, comportamento da vítima
- **Pena-base SEMPRE no mínimo legal** se todas favoráveis ao réu (STJ sumulado)
- **Erro clássico CESPE:** confundir circunstâncias do Art. 59 com agravantes (Arts. 61-65)
  → Art. 59 = 1ª fase | Arts. 61-65 = 2ª fase
- **Palavra-chave banca:** "fundamentação idônea" — juiz DEVE motivar cada circunstância

### 📚 CONTEXTO ENRIQUECEDOR

[análise kelseniana da discricionariedade judicial vinculada, debate sobre
determinismo vs. livre-arbítrio na culpabilidade, evolução histórica do sistema
trifásico Nelson Hungria, jurisprudência do STF sobre penas excessivas...]

### 🎯 REVISÃO RÁPIDA
1. 8 circunstâncias judiciais (Art. 59) = 1ª fase da dosimetria
2. Pena-base no mínimo se tudo favorável (STJ consolidado)
3. Fundamentação idônea obrigatória — vício = nulidade
```

---

*Fenice IA 05 — Pareto Jurídico · camada de entrega*  
*بِسْمِ اللهِ الرَّحْمَنِ الرَّحِيمِ — Em nome de Allah, o Misericordioso*

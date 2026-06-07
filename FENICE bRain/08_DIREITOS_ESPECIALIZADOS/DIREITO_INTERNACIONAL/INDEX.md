---
nivel: ramo
tipo: index
ramo: direito-internacional
tags: [direito-internacional, index]
created: 2026-06-07
---

# 🌐 Direito Internacional — INDEX

**Cobertura:** Leis nacionais com projeção internacional + tratados/convenções
ratificados pelo Brasil (decretos promulgadores).

---

## 📜 Leis Nacionais (atomizadas — pipeline automático)

Extraídas via `pipeline_direito_internacional.py` (regex `Art. N`, padrão
validado nos demais códigos):

| Lei | Norma | Artigos | Pasta |
|---|---|---|---|
| Lei de Arbitragem | Lei 9.307/1996 | 44 | [[Artigos/L9307/INDEX\|L9307/]] |
| Lei de Migração | Lei 13.445/2017 | 125 | [[Artigos/L13445/INDEX\|L13445/]] |

## 🌍 Tratados e Convenções Internacionais (atomização via skill)

Esses documentos têm **numeração inconsistente** (`ARTIGO`/`Artigo`, arábico/romano
— ver nota técnica abaixo) e estrutura aninhada decreto+anexo. São processados
sob demanda com a skill `atomizar-juridico` (motor de notas atômicas + Zendelski
Graph + vetor de negócio), não por regex fixo.

| Decreto | Trata de | Status |
|---|---|---|
| Decreto 678/1992 | Convenção Americana de Direitos Humanos (Pacto de San José) | ✅ [[Tratados/Convencao-Americana-Direitos-Humanos/INDEX\|4/82 atomizados]] — prova de conceito |
| Decreto 4.311/2002 | Convenção de Nova York — Sentenças Arbitrais Estrangeiras | ✅ [[Tratados/Convencao-Nova-York-Sentencas-Arbitrais/INDEX\|5/16 atomizados]] — **espelha L9307 e liga ao projeto STJ HSE** |
| Decreto 4.388/2002 | Estatuto de Roma (Tribunal Penal Internacional) | ✅ [[Tratados/Estatuto-de-Roma-TPI/INDEX\|4/128 atomizados]] — bloco fundacional |
| Decreto 7.030/2009 | Convenção de Viena sobre Direito dos Tratados | ✅ [[Tratados/Convencao-Viena-Direito-dos-Tratados/INDEX\|4/85 atomizados]] — **hub meta-normativo dos demais tratados** |
| Decreto 8.327/2014 | (a confirmar conteúdo) | 🔲 pendente |
| D0350 | (a confirmar conteúdo) | 🔲 pendente |

> Resultado da atomização vai para `Tratados/<Nome-do-Tratado>/` — uma nota
> atômica por artigo, linkando de volta à lei nacional correlata acima e,
> quando aplicável, ao hub de doutrina em `09_REFERENCIAS/MAESTROS`.

### 📌 Nota técnica (porque não usamos regex aqui)
Testamos os 6 decretos: formatos de numeração variam entre `ARTIGO 1`
(maiúsculo), `Artigo 1` (misto) e até `Artigo I` (numeral romano — Convenção
de Nova York), às vezes misturados no mesmo documento. Um regex único seria
frágil e falharia silenciosamente em casos de borda — exatamente o cenário em
que a análise da skill supera o parsing fixo.

---

## 🔗 Navegação

- **Voltar:** [[../INDEX|Direitos Especializados]]
- **Skill de atomização:** `.claude/skills/atomizar-juridico`
- **Hub de doutrina:** [[../../09_REFERENCIAS/MAESTROS/INDEX|MAESTROS]]

---

**Status:** 🔄 169 artigos de leis nacionais prontos · tratados aguardando atomização

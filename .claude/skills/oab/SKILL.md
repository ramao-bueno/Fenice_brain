---
name: oab
description: Use when the user asks any question about OAB exam prep, Estatuto da OAB (Lei 8.906), Código de Ética e Disciplina (CED), resolving OAB exam questions, or needs study guidance for the Brazilian bar exam.
---

# OAB — Skill de Preparação para o Exame da Ordem

## Vault disponível

```
07_FILOSOFIA/OAB/
├─ Lei 8906 - Estatuto/   ← 58 artigos OCR estruturados
├─ Codigo de Etica/       ← ~40 artigos do CED estruturados
└─ Jurisprudencia/        ← (a preencher)

_sistema/OAB/             ← espelho do Estatuto + artigos avulsos
```

**Buscar artigo específico:** `mcp__mcpvault__search_notes` com "Art. X" ou tema

---

## Estrutura do Exame OAB

| Fase | Formato | O que cai |
|---|---|---|
| **1ª fase** | 80 questões objetivas | Todas as matérias jurídicas + Estatuto/CED |
| **2ª fase** | Peça prática + 4 questões dissertativas | Área escolhida pelo candidato |
| **Prático-profissional** | Após aprovação nas 2 fases | Simulação de atuação profissional |

---

## Matérias da 1ª Fase — Peso por Frequência

| Matéria | Artigos do vault | Frequência em prova |
|---|---|---|
| **Estatuto da OAB** (Lei 8.906) | `_sistema/OAB/` | ⭐⭐⭐⭐⭐ |
| **Código de Ética** (CED) | `07_FILOSOFIA/OAB/Codigo de Etica/` | ⭐⭐⭐⭐⭐ |
| **Direito Constitucional** | `03_PUBLICO/` | ⭐⭐⭐⭐ |
| **Direito Civil** | `01_PRIVADO/Codigos/CC/` | ⭐⭐⭐⭐ |
| **Direito Processual Civil** | `03_PROCESSO_CIVIL/` | ⭐⭐⭐⭐ |
| **Direito Penal** | `02_PENAL/` | ⭐⭐⭐ |
| **Direito do Trabalho** | `04_TRABALHO/` | ⭐⭐⭐ |
| **Direito Administrativo** | `03_PUBLICO/` | ⭐⭐⭐ |
| **Direito Tributário** | `05_ESPECIAL/` | ⭐⭐ |
| **Direito Empresarial** | `05_ESPECIAL/` | ⭐⭐ |

---

## Protocolo de Resolução de Questão OAB

Ao receber uma questão, responder sempre neste formato:

```markdown
**Gabarito:** [letra correta]

**Fundamento:** [dispositivo exato — Art. X, §Y da Lei 8.906 | Art. Z do CED]

**Raciocínio:** [por que as erradas estão erradas — 1 linha cada]

> [!WARNING] Pegadinha
> [ponto que induz ao erro mais comum nesta questão]
```

---

## Temas Quentes do Estatuto (Lei 8.906) — Decorar

| Artigo | Tema | Número crítico |
|---|---|---|
| Art. 7º | Direitos do advogado + imunidades | — |
| Art. 7º-B | Imunidade por manifestação técnica | — |
| Art. 8º | Requisitos de inscrição na OAB | — |
| Art. 22-24 | Honorários advocatícios | Regras de sucumbência |
| Art. 25 | Sigilo profissional | Dever absoluto |
| Art. 27-28 | Impedimentos e incompatibilidades | Lista fechada |
| Art. 34 | Infrações disciplinares | Lista com incisos |
| Art. 37 | Suspensão | Casos de aplicação |
| Art. 43 | Prescrição disciplinar | **5 anos** |
| Art. 44 | OAB — natureza jurídica | Serviço público |
| Art. 45 | Órgãos da OAB | CF, Conselho Federal, Seccionais, Subseções, CAAOAB |
| Art. 49-50 | Tribunal de Ética e Disciplina | Competências |
| Art. 65 | Mandato dos órgãos | **3 anos** |

---

## Temas Quentes do CED — Decorar

| Artigo CED | Tema |
|---|---|
| Art. 2º | Deveres fundamentais do advogado |
| Art. 7º | Sigilo profissional no CED |
| Art. 10-13 | Mandato — outorga, substabelecimento, renúncia |
| Art. 18 | Conflito de interesses |
| Art. 24-25 | Honorários no CED — moderação |
| Art. 28-34 | Publicidade do advogado — limites |
| Art. 49-50 | Tribunal de Ética — competência e processo |

---

## Pegadinhas Clássicas por Tema

### Estatuto da OAB
- **Imunidade do advogado (art. 7º, §2º):** não é absoluta — não cobre injúria, calúnia, difamação fora da defesa técnica
- **Prisão do advogado:** sala de Estado Maior; na falta → **prisão domiciliar** (não cadeia comum)
- **OAB não é sindicato:** contribuição da OAB ≠ contribuição sindical (art. 47)
- **Mandato de 3 anos** nos órgãos da OAB — não confundir com prazos processuais
- **Prescrição disciplinar: 5 anos** — contados da data do fato ou, se ocultação, do conhecimento

### CED
- **Substabelecimento com reserva de poderes** é ato pessoal — sem necessidade de concordância do cliente
- **Sigilo profissional** persiste mesmo após encerramento da causa e até depois da morte do cliente
- **Honorários:** pacto de quota litis permitido, mas vedado percentual sobre o total da causa em ação de alimentos

---

## Como Criar Notas de Estudo a Partir de Questões

Ao processar um bloco de questões OAB para o vault, invocar **[[SuperpowerFenice-03]]** (`/atomizar-juridico`) com o seguinte contexto:

```
Texto: [questão + gabarito comentado]
Destino: _sistema/OAB/ ou 07_FILOSOFIA/OAB/
Tags: oab, [matéria], [artigo-X]
```

---

## Navegação Rápida no Vault

| O que buscar | Onde |
|---|---|
| Artigo específico do Estatuto | `_sistema/OAB/Art. X — *.md` |
| Artigo do CED | `07_FILOSOFIA/OAB/Codigo de Etica/Art. X — *.md` |
| Jurisprudência OAB | `07_FILOSOFIA/OAB/Jurisprudencia/` |
| Direitos fundamentais (prova constitucional) | `03_PUBLICO/` |
| CC — boa-fé, contratos, responsabilidade | `01_PRIVADO/Codigos/CC/` |

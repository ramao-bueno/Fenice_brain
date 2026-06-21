---
name: fenice-ia-03
description: Detector de Antinomias — agente que detecta conflitos entre normas usando busca vetorial no grafo_arestas e alerta sobre incompatibilidade com tratados internacionais, súmulas e direito constitucional
---

# Fenice IA 03 — Detector de Antinomias (Grafo Cross-Reference)

## Propósito

Ao abrir um artigo de lei recém-sancionado, rodar em segundo plano uma busca semântica e estrutural
para detectar **antinomias**: conflitos normativos (explícitos ou ideológicos) com tratados
internacionais, CF/88, súmulas vinculantes e normas do mesmo grau hierárquico.

## Quando usar

- Pesquisa de constitucionalidade de norma
- Análise de conflito entre lei ordinária e tratado internacional (art. 5º §2º CF/88)
- Arguição de inconstitucionalidade (ADI, ADPF)
- Tese sobre antinomia, revogação tácita ou conflito de especialidade

## Tipos de antinomia detectáveis

| Tipo | Exemplo | Resolução clássica |
|---|---|---|
| Hierárquica | Lei vs CF/88 | Lex superior |
| Temporal | Lei nova vs lei antiga | Lex posterior |
| Especialidade | Lei geral vs lei especial | Lex specialis |
| Ideológica | Lei penal vs CADH | Controle de convencionalidade |

## Algoritmo Python

```python
from fenice_graph_schema import consultar_grafo  # scripts/fenice_graph_schema.sql
from planalto_db import PlanaltoDB
from typing import List, Dict
import re

PESO_ANTINOMIA_MINIMO = 0.65  # Score semântico para disparar alerta

def detectar_antinomias(texto_norma: str, numero_ano: str) -> List[Dict]:
    """
    Retorna lista de conflitos detectados, ordenados por score.
    Cada item: {norma_conflitante, tipo_antinomia, score, trecho_conflitante, resolucao_sugerida}
    """
    conflitos = []

    # 1. Busca por arestas tipo 'contraria' no grafo
    arestas = consultar_grafo(numero_ano, tipo_relacao="contraria")
    for aresta in arestas:
        conflitos.append({
            "norma_conflitante": aresta["destino"],
            "tipo_antinomia":    "registrada_no_grafo",
            "score":             aresta.get("peso", 1.0),
            "trecho_conflitante": aresta.get("contexto", ""),
            "resolucao_sugerida": _sugerir_resolucao(aresta),
        })

    # 2. Busca FTS por termos-gatilho de conflito
    TERMOS_RISCO = [
        "prisão perpétua", "pena de morte", "tortura",
        "trabalho forçado", "expulsão coletiva", "retroatividade da pena",
        "confisco", "sigilo absoluto", "censura prévia",
    ]
    texto_lower = texto_norma.lower()
    for termo in TERMOS_RISCO:
        if termo in texto_lower:
            conflitos.append({
                "norma_conflitante": "Convenção Americana de Direitos Humanos (CADH)",
                "tipo_antinomia":    "ideologica_direitos_humanos",
                "score":             0.95,
                "trecho_conflitante": _extrair_trecho(texto_norma, termo),
                "resolucao_sugerida": "Controle de convencionalidade — RE 466.343/STF",
            })

    return sorted(conflitos, key=lambda x: -x["score"])


def _extrair_trecho(texto: str, termo: str, janela: int = 150) -> str:
    idx = texto.lower().find(termo)
    if idx == -1:
        return ""
    start = max(0, idx - janela)
    end = min(len(texto), idx + len(termo) + janela)
    return f"...{texto[start:end]}..."


def _sugerir_resolucao(aresta: dict) -> str:
    tipo = aresta.get("tipo_relacao", "")
    if tipo == "contraria":
        return "Verificar hierarquia normativa — aplicar critério lex superior / lex posterior / lex specialis"
    return "Analisar contexto — possível conflito aparente"
```

## Output — Alerta de Antinomia no vault

```markdown
> [!DANGER] Alerta de Antinomia Detectada
> **Norma em análise:** Lei 14.xxx/2026 — Art. 7º
> **Conflito com:** Convenção Americana de Direitos Humanos, Art. 9º
> **Tipo:** Antinomia ideológica (direitos humanos)
> **Score de conflito:** 95%
> **Resolução sugerida:** Controle de convencionalidade — RE 466.343/STF
>
> **Trecho conflitante:**
> "...determina prisão de caráter perpétuo para..."
```

## Integração com grafo

- Usar tabela `grafo_arestas` de `fenice_graph_schema.sql` com `tipo_relacao = 'contraria'`
- Popular via `fenice_graph_seed.py` com arestas manuais curatoriais
- Futuro: embeddings pgvector para busca semântica de antinomias não catalogadas

## Valor de mercado

O Detector de Antinomias é a funcionalidade **que advogados e procuradores pagariam sozinhos**.
Nenhuma LegalTech brasileira tem alerta automático de conflito normativo em tempo real.

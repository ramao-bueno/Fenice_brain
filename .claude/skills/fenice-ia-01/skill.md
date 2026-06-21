---
name: fenice-ia-01
description: Túnel do Tempo Jurídico — reconstrói o estado de qualquer lei em uma data passada, usando as tags <s> mineradas do Planalto para análise de direito intertemporal
---

# Fenice IA 01 — Túnel do Tempo Jurídico (Temporal Delta-Parser)

## Propósito

Dado um texto HTML de lei baixado do Planalto e uma **data-alvo** informada pelo usuário, reconstruir
o estado exato da norma naquela data: ocultar o que foi incluído _depois_ da data-alvo e restaurar
os fragmentos revogados (`<s>`) cuja revogação ocorreu _após_ a data-alvo.

## Quando usar

- Pesquisa de direito intertemporal (retroatividade, ultratividade)
- Comparativo histórico de redações de artigos
- Teses sobre conflito de leis no tempo (`[[Direito_Civil/LINDB]]`)
- Análise de contratos celebrados sob vigência de lei anterior

## Input esperado

```
data_alvo: "DD/MM/AAAA"
html_lei:  conteúdo HTML bruto da lei (Planalto)
```

## Algoritmo Python — Temporal Delta-Parser

```python
from datetime import datetime
from bs4 import BeautifulSoup
import re

def parse_data(texto: str):
    """Tenta extrair data de metadado inline tipo '(Redação dada pela Lei X, de 12.04.2024)'"""
    m = re.search(r"de\s+(\d{1,2})[./](\d{1,2})[./](\d{4})", texto or "")
    if m:
        return datetime(int(m.group(3)), int(m.group(2)), int(m.group(1)))
    return None

def reconstruir_lei_em_data(html: str, data_alvo: datetime) -> dict:
    """
    Retorna dict com:
      - texto_na_data: texto vigente em data_alvo
      - fragmentos_ja_revogados: textos <s> ainda válidos na data
      - fragmentos_ainda_nao_existiam: textos incluídos após data_alvo
    """
    soup = BeautifulSoup(html, "html.parser")
    resultado = {
        "texto_na_data": [],
        "ja_revogados": [],
        "ainda_nao_existiam": [],
    }

    for tag in soup.find_all(True):
        # Texto riscado: foi revogado — verificar QUANDO
        if tag.name in ("s", "strike", "del"):
            data_revogacao = parse_data(tag.get("title") or tag.get("data-revogado-em") or "")
            if data_revogacao and data_revogacao > data_alvo:
                # Revogação posterior ao alvo: texto ainda VIGENTE na data-alvo
                resultado["texto_na_data"].append(tag.get_text(" ", strip=True))
            else:
                resultado["ja_revogados"].append(tag.get_text(" ", strip=True))
            tag.decompose()
            continue

        # Texto adicionado depois da data-alvo (buscar marcador de inclusão)
        data_inclusao = parse_data(tag.get("title") or "")
        if data_inclusao and data_inclusao > data_alvo:
            resultado["ainda_nao_existiam"].append(tag.get_text(" ", strip=True))
            tag.decompose()

    resultado["texto_na_data"].insert(0, soup.get_text(" ", strip=True))
    return resultado
```

## Output — Callouts Obsidian

Ao apresentar o resultado ao usuário, use o formato:

```markdown
> [!INFO] Estado da Lei em {data_alvo}
> {texto_vigente_na_data}

> [!WARNING] Textos já revogados nesta data
> {lista de fragmentos já revogados}

> [!NOTE] Textos que ainda não existiam
> {lista de acréscimos posteriores}
```

## Integração com vault

- Buscar HTML em cache: `C:\Fenice_bRain\scripts\_cache_planalto\`
- Usar `parsear_lei()` de `scripts/planalto_pipeline.py` para popular o cache
- Tags de destino para notas temporais: `historico-legislativo`, `direito-intertemporal`

## Valor de mercado

Permite ao pesquisador ou advogado **um clique** para responder: "Qual era o texto deste artigo
quando meu cliente assinou o contrato em 2019?" — funcionalidade inexistente em qualquer LegalTech
brasileira de massa.

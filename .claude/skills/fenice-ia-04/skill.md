---
name: fenice-ia-04
description: Exportador de Fichamento ABNT/APA — gera citação formatada, referência bibliográfica automática e insight filosófico para qualquer trecho de lei, súmula ou doutrina do vault
---

# Fenice IA 04 — Exportador de Fichamento ABNT/APA

## Propósito

Para qualquer trecho de texto jurídico selecionado (lei, súmula, artigo de doutrina), gerar
instantaneamente um bloco markdown pronto com: citação formatada, referência bibliográfica
automática e insight filosófico da IA como "Nota do Pesquisador".

## Quando usar

- Escrita de TCC, artigo científico, monografia
- Fichamento de doutrina para estudo de concurso
- Geração de referências bibliográficas de leis e acórdãos
- Exportação para Zotero/Mendeley via markdown

## Formatos suportados

| Fonte | Norma ABNT | Padrão gerado |
|---|---|---|
| Lei Federal | NBR 6023:2018 — legislação | `BRASIL. Lei nº X.XXX...` |
| Código | NBR 6023:2018 | `BRASIL. [Nome do Código]...` |
| Súmula STF/STJ | NBR 6023:2018 | `BRASIL. Supremo Tribunal Federal...` |
| Acórdão | NBR 6023:2018 | `BRASIL. [Tribunal]. [processo]. [data]...` |
| Doutrina | NBR 6023:2018 livro | `SOBRENOME, Nome. Título...` |

## Gerador Python

```python
from datetime import datetime
from pathlib import Path
import re

def gerar_fichamento(
    trecho: str,
    fonte: dict,
    lente: str = "POSITIVISMO_KELSEN",
    insight_ia: str = "",
) -> str:
    """
    trecho: texto selecionado pelo usuário
    fonte:  dict com tipo, numero, ano, url_origem, tribunal, ementa
    lente:  lente filosófica para o insight
    insight_ia: análise gerada pelo FeniceRAG
    """
    ref = _gerar_referencia(fonte)
    citacao = _formatar_citacao(trecho, fonte)
    nota = insight_ia or "[Insight filosófico pendente — ativar Fenice IA 02]"

    return f"""## Fichamento — {fonte.get('numero_ano', 'Fonte Jurídica')}

### Citação ({_detectar_norma(fonte)})

{citacao}

### Referência Bibliográfica (ABNT NBR 6023:2018)

> {ref}

### Nota do Pesquisador _(Lente: {lente})_

{nota}

---
_Fichamento gerado pelo Fenice bRain em {datetime.now().strftime('%d/%m/%Y às %H:%M')}_
_Fonte: {fonte.get('url_origem', 'Vault local')}_
"""


def _gerar_referencia(fonte: dict) -> str:
    tipo = fonte.get("tipo", "lei").lower()
    numero_ano = fonte.get("numero_ano", "")
    ementa = fonte.get("ementa", "")[:120]
    url = fonte.get("url_origem", "")
    acesso = datetime.now().strftime("%d %b. %Y")

    if tipo in ("lei ordinaria", "lei federal", "lei"):
        # Ex: Lei 14.133/2021
        m = re.match(r"Lei\s+(\d+)[./](\d{4})", numero_ano)
        if m:
            n, ano = m.group(1), m.group(2)
            return (
                f"BRASIL. Lei nº {_formatar_numero(n)}, de {ano}. {ementa}. "
                f"Disponível em: <{url}>. Acesso em: {acesso}."
            )

    if tipo in ("sumula-stf",):
        n = fonte.get("numero", "")
        data = fonte.get("data_aprovacao", "")
        return (
            f"BRASIL. Supremo Tribunal Federal. Súmula nº {n}. "
            f"Aprovada em {data}. Brasília: STF, {data[-4:]}. "
            f"Disponível em: <{url}>. Acesso em: {acesso}."
        )

    if tipo in ("sumula-stj",):
        n = fonte.get("numero", "")
        data = fonte.get("julgado_em", "")
        return (
            f"BRASIL. Superior Tribunal de Justiça. Súmula nº {n}. "
            f"{ementa}. Julgada em {data}. "
            f"Disponível em: <{url}>. Acesso em: {acesso}."
        )

    # Fallback genérico
    return f"BRASIL. {numero_ano}. {ementa}. Disponível em: <{url}>. Acesso em: {acesso}."


def _formatar_citacao(trecho: str, fonte: dict) -> str:
    numero_ano = fonte.get("numero_ano", "")
    artigo = fonte.get("artigo", "")
    ref_curta = f"{numero_ano}" + (f", {artigo}" if artigo else "")
    # Citação direta conforme ABNT
    return f'"{trecho.strip()}" (BRASIL, {ref_curta})'


def _detectar_norma(fonte: dict) -> str:
    tipo = fonte.get("tipo", "").lower()
    if "stf" in tipo:
        return "ABNT — Súmula STF"
    if "stj" in tipo:
        return "ABNT — Súmula STJ"
    return "ABNT NBR 6023:2018"


def _formatar_numero(n: str) -> str:
    n = n.zfill(5)
    if len(n) == 5:
        return f"{n[:2]}.{n[2:]}"
    return n
```

## Output exemplo

```markdown
## Fichamento — Lei 14133/2021

### Citação (ABNT NBR 6023:2018)

"É vedada a exigência de capital mínimo superior a 10% do valor estimado da
contratação." (BRASIL, Lei 14.133/2021, Art. 67)

### Referência Bibliográfica (ABNT NBR 6023:2018)

> BRASIL. Lei nº 14.133, de 2021. Lei de Licitações e Contratos Administrativos.
> Disponível em: <https://www.planalto.gov.br/...>. Acesso em: 21 jun. 2026.

### Nota do Pesquisador _(Lente: POSITIVISMO_KELSEN)_

Sob a ótica kelseniana, este dispositivo representa uma norma secundária que limita
a discricionariedade administrativa na fase de habilitação, derivada diretamente
do princípio constitucional da isonomia (Grundnorm → CF/88 → Lei 14.133).

---
_Fichamento gerado pelo Fenice bRain em 21/06/2026 às 14:30_
```

## Integração com vault

1. Usuário seleciona trecho numa nota do vault
2. `Ctrl+P` → comando `Fenice: Fichar com Insight`
3. Sistema lê o frontmatter da nota (número, tribunal, url_origem)
4. Chama `gerar_fichamento()` + `FeniceRAG.responder_com_contexto()`
5. Insere bloco markdown na nota ou cria nova em `03_PROCESSO_CIVIL/FICHAMENTOS/`

## Valor de mercado

Estudantes de pós-graduação e advogados gastam **2-4h por semana** formatando referências.
Esta skill elimina isso com 1 clique — **retenção imediata e diferencial de produto**.

import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict
from config_cf import (TAGS_PADRAO, LEI_NOME, TITULO_MAPEAMENTO,
                       PLANALTO_BASE_URL, TEMA_POR_TITULO)


class MarkdownGeneratorCF:
    """Gera notas Markdown estruturadas para artigos da Constituição Federal."""

    def __init__(self, output_base: Path):
        self.output_base = Path(output_base)

    def gerar_nota_artigo(self, artigo: Dict, titulo: str) -> str:
        num = artigo["numero"]
        titulo_config = TITULO_MAPEAMENTO.get(titulo, {})
        titulo_nome = titulo_config.get("nome", titulo)
        tema = TEMA_POR_TITULO.get(titulo, "constituicao")
        planalto_url = f"{PLANALTO_BASE_URL}#art{num}"

        tags = TAGS_PADRAO.copy()
        tags_extras = [titulo.lower(), f"art-{num}", tema]
        for t in tags_extras:
            if t not in tags:
                tags.append(t)

        frontmatter = {
            "artigo": str(num),
            "lei": LEI_NOME,
            "titulo_cf": titulo,
            "parte": titulo_nome,
            "status": "vigente",
            "cf88": True,
            "emendas": [],
            "planalto_url": planalto_url,
            "tags": tags,
            "created": datetime.now().strftime("%Y-%m-%d"),
        }

        fm_str = yaml.dump(frontmatter, allow_unicode=True,
                           default_flow_style=False, sort_keys=False)

        redacao = artigo.get("redacao", "[Conferir redação no Planalto]")
        titulo_artigo = artigo.get("titulo", f"Art. {num} CF")
        art_anterior = max(1, num - 1)
        art_seguinte = num + 1

        corpo = f"""# CF/88 Art. {num} — {titulo_artigo}

**Lei:** {LEI_NOME}
**Título:** {titulo} — {titulo_nome}
**Status:** VIGENTE
**Planalto:** [Texto oficial]({planalto_url})

---

## REDACAO LEGAL

> {redacao}

---

## ANALISE TECNICA

### Conceito Central

[Sintese do conteudo normativo do artigo]

### Elementos-Chave

| Elemento | Descricao |
|----------|-----------|
| **Sujeito** | A quem se dirige a norma |
| **Objeto** | O que a norma regula |
| **Eficacia** | Aplicabilidade (plena / contida / limitada) |

---

## ARTIGOS CORRELATOS

### Mesma CF
- [[Art. {art_anterior} — CF]] — artigo anterior
- [[Art. {art_seguinte} — CF]] — artigo seguinte

### Legislacao Derivada
[Leis ordinarias que regulamentam este artigo]

---

## JURISPRUDENCIA STF

### Teses e Precedentes
[Precedentes do STF sobre este artigo]

---

## EMENDAS CONSTITUCIONAIS

[ECs que modificaram este artigo — verificar no Planalto]

---

## RELACIONAMENTOS (Dataview)

```dataview
LIST FROM "FENICE bRain/02_DIREITO_CIVIL"
  OR "FENICE bRain/03_CODIGO_PENAL"
  OR "FENICE bRain/01_CODIGO_PROCESSO_CIVIL"
WHERE contains(base_constitucional, "CF Art. {num}")
```

---

**Ultima atualizacao:** {datetime.now().strftime("%Y-%m-%d")}
**Fonte oficial:** [planalto.gov.br]({planalto_url})
"""
        return f"---\n{fm_str}---\n\n{corpo}"

    def salvar_artigo(self, artigo: Dict, conteudo: str, titulo: str) -> Path:
        pasta = self.output_base / titulo
        pasta.mkdir(parents=True, exist_ok=True)

        filename = f"Art. {artigo['numero']} — CF.md"
        filepath = pasta / filename

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(conteudo)
            return filepath
        except Exception as e:
            print(f"Erro ao salvar {filename}: {e}")
            return None


if __name__ == "__main__":
    gen = MarkdownGeneratorCF(Path("test_output_cf"))
    print("Gerador CF pronto")

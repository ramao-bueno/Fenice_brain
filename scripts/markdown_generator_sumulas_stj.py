#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera notas Markdown atômicas para Súmulas STJ."""
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict
from config_sumulas_stj import TAGS_PADRAO


class MarkdownGeneratorSumulaSTJ:
    """Gera notas Markdown estruturadas para Súmulas STJ."""

    def __init__(self, output_base: Path):
        self.output_base = Path(output_base)

    def gerar_nota_sumula(self, sumula: Dict) -> str:
        num = sumula["numero"]
        texto = sumula["texto"]

        # Extrai jurisprudência/tema do texto se possível
        tema = sumula.get("tema", "jurisprudencia-pacifica")

        tags = TAGS_PADRAO.copy()
        tags.extend([f"sumula-{num}", tema, "stj"])

        frontmatter = {
            "sumula": str(num),
            "tribunal": "STJ",
            "tipo": "sumula-stj",
            "status": "vigente",
            "relacionados": [],
            "tags": tags,
            "created": datetime.now().strftime("%Y-%m-%d"),
        }

        fm_str = yaml.dump(frontmatter, allow_unicode=True,
                           default_flow_style=False, sort_keys=False)

        corpo = f"""# Súmula STJ {num}

**Tribunal:** Superior Tribunal de Justiça
**Status:** VIGENTE
**Jurisprudência Consolidada**

---

## TEXTO DA SÚMULA

> {texto}

---

## ANALISE

### Jurisprudência Consolidada

[Qual é a jurisprudência pacífica que esta súmula consolida?
Qual é o precedente ou linha de decisões que originou esta súmula?]

### Aplicação Prática

[Como os tribunais aplicam esta súmula nas decisões?
Qual é o impacto desta súmula na prática forense?]

### Exceções e Ressalvas

[Há exceções à regra consolidada nesta súmula?
Há precedentes que relativizam ou afastam a aplicação desta súmula?]

---

## ARTIGOS CORRELATOS

[Dispositivos do CPC, CC, CP ou leis especiais relacionados a esta súmula]

---

## JURISPRUDENCIA MAIS RECENTE

[Decisões posteriores do STJ que confirmam, afastam ou evoluem sobre
a orientação desta súmula]

---

## OBSERVACOES

[Críticas doutrinárias, discussões sobre a súmula, mudanças jurisprudenciais]

---

**Última atualização:** {datetime.now().strftime("%Y-%m-%d")}
"""
        return f"---\n{fm_str}---\n\n{corpo}"

    def salvar_sumula(self, sumula: Dict, conteudo: str) -> Path:
        pasta = self.output_base
        pasta.mkdir(parents=True, exist_ok=True)

        filename = f"Sumula-STJ-{sumula['numero']:04d}.md"
        filepath = pasta / filename

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(conteudo)
            return filepath
        except Exception as e:
            print(f"Erro ao salvar Súmula {sumula['numero']}: {e}")
            return None


if __name__ == "__main__":
    gen = MarkdownGeneratorSumulaSTJ(Path("test_output_sumulas_stj"))
    print("Gerador Súmulas STJ pronto")

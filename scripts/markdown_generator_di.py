#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera notas Markdown atômicas para artigos de leis de Direito Internacional."""
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from config_direito_internacional import TAGS_PADRAO


# Jurisprudência curada: teses STF/STJ por artigo
JURIS_DI = {
    "1": [  # LINDB — Lei de Introdução às Normas do Direito Brasileiro
        "STJ — A LINDB (DL 4.657/42) é lei de sobredireito: regula a aplicação, interpretação, vigência e eficácia das normas em geral; aplica-se a todos os ramos do direito.",
        "STF — A irretroatividade da lei (art. 6° LINDB): a lei nova não pode prejudicar o ato jurídico perfeito, o direito adquirido e a coisa julgada (art. 5°, XXXVI CF).",
    ],
    "7": [  # LINDB — art. 7° (estatuto pessoal)
        "STJ — A lei do domicílio da pessoa (art. 7° LINDB) rege sua qualificação e relações de família; em caso de domicílios diferentes dos cônjuges, aplica-se a lei do primeiro domicílio conjugal.",
        "STJ — Tese: contratos internacionais entre partes domiciliadas no exterior são regidos pela lei do local de constituição da obrigação (art. 9° LINDB); as partes podem eleger foro estrangeiro.",
    ],
    "9": [  # LINDB — obrigações no exterior
        "STJ — A lei do lugar da constituição da obrigação (art. 9° LINDB) rege os requisitos intrínsecos e extrínsecos; cláusula de eleição de lei estrangeira em contratos internacionais é válida.",
        "STF — Tratados e convenções internacionais ratificados têm status de lei ordinária, salvo tratados de direitos humanos aprovados por quórum qualificado (EC 45/2004) — status supralegal (STF — RE 466.343).",
    ],
    "4": [  # Convenção de Viena sobre Contratos de Compra e Venda Internacional (CISG)
        "STJ — O Brasil ratificou a CISG (promulgada pelo Decreto 8.327/2014); aplica-se a contratos entre partes domiciliadas em diferentes países signatários, salvo exclusão expressa.",
        "STJ — A CISG exclui questões de validade contratual e de propriedade das mercadorias de seu âmbito; essas questões são regidas pela LINDB.",
    ],
    "3": [  # Convenção sobre Direitos da Criança — ECA interface
        "STF — A Convenção sobre os Direitos da Criança (1989), ratificada pelo Brasil, tem status supralegal (RE 466.343); prevalece sobre lei ordinária conflitante.",
        "STJ — O princípio do melhor interesse da criança (art. 3° da Convenção + ECA art. 4°) é standard de ordem pública internacional; afasta aplicação de lei estrangeira que o contrarie.",
    ],
}

# Observações práticas por artigo
OBS_PRATICAS_DI = {
    "9": {
        "autor": "Em contratos internacionais, incluir cláusula de eleição de lei (choice of law) e de foro; no Brasil, a eleição de lei estrangeira é válida mas pode ser afastada pela ordem pública brasileira (art. 17 LINDB).",
        "defesa": "A ordem pública internacional (art. 17 LINDB) é barreira à aplicação de lei estrangeira; demonstrar que a norma estrangeira viola princípios fundamentais do direito brasileiro.",
        "pratica": "Homologação de sentença estrangeira: competência do STJ (art. 105, I, i CF + Res. 9/2005 STJ); requisitos: autenticidade da decisão, contraditório observado, não violação à soberania e ordem pública, e trânsito em julgado no exterior.",
    },
}


def _jurisprudencia_di(num_str: str) -> List[str]:
    return JURIS_DI.get(num_str, [])


def _obs_praticas_di(num_str: str) -> dict:
    return OBS_PRATICAS_DI.get(num_str, {})


def _correlatos_outros_di(num_base) -> List[str]:
    correlatos = [
        "[[CF88 Art. 5]] — tratados de direitos humanos (§3°)",
        "[[CF88 Art. 4]] — princípios das relações internacionais",
        "[[L10406 Art. 7]] — pessoa natural — domicílio (CC)",
    ]
    return correlatos


class MarkdownGeneratorDI:
    """Gera notas Markdown estruturadas para artigos de leis de Direito Internacional."""

    def __init__(self, output_base: Path):
        self.output_base = Path(output_base)

    def gerar_nota_artigo(self, artigo: Dict, lei_cfg: Dict, sigla: str) -> str:
        num_raw = artigo["numero"]
        try:
            num = int(num_raw)
        except (ValueError, TypeError):
            num = num_raw
        num_str = str(num_raw)
        nome_lei = lei_cfg["nome"]
        lei_numero = lei_cfg["lei_numero"]
        categoria = artigo["categoria"]
        tema = lei_cfg.get("tema", "direito-internacional")

        tags = TAGS_PADRAO.copy()
        for t in [categoria.lower(), f"art-{num}", tema, sigla.lower()]:
            if t not in tags:
                tags.append(t)

        frontmatter = {
            "artigo": num_str,
            "lei": f"Lei {lei_numero} ({nome_lei})",
            "sigla": sigla,
            "categoria": categoria,
            "status": "vigente",
            "direito_internacional": True,
            "relacionados": [],
            "tags": tags,
            "created": datetime.now().strftime("%Y-%m-%d"),
        }

        fm_str = yaml.dump(frontmatter, allow_unicode=True,
                           default_flow_style=False, sort_keys=False)

        redacao = artigo.get("redacao", "[Conferir redação no Planalto]")
        redacao_display = (redacao[:600] + "...") if len(redacao) > 600 else redacao
        titulo_artigo = artigo.get("titulo", f"Art. {num}")
        if isinstance(num, int):
            art_anterior = max(1, num - 1)
            art_seguinte = num + 1
        else:
            art_anterior = num_str
            art_seguinte = num_str

        juris = _jurisprudencia_di(num_str)
        if juris:
            juris_str = "\n".join(f"- {j}" for j in juris)
            juris_str += "\n\n[Conferir atualização: STJ «Jurisprudência em Teses»; STF — Repercussão Geral; ACNUR; CIJ]"
        else:
            juris_str = "[Conferir atualização: STJ «Jurisprudência em Teses»; STF — Repercussão Geral; ACNUR; CIJ]"

        obs = _obs_praticas_di(num_str)
        if obs:
            obs_str = (
                f"- **Autor/Contratante:** {obs.get('autor', '')}\n"
                f"- **Defesa/Réu:** {obs.get('defesa', '')}\n"
                f"- **Prática:** {obs.get('pratica', '')}"
            )
        else:
            obs_str = "[Aplicação na prática forense internacional — preencher com experiência do caso concreto]"

        correlatos = _correlatos_outros_di(num)
        correlatos_str = "\n".join(f"- {c}" for c in correlatos)

        corpo = f"""# {sigla} Art. {num} — {titulo_artigo}

**Lei:** {lei_numero} — {nome_lei}
**Categoria:** {categoria}
**Status:** VIGENTE

---

## REDACAO LEGAL

> {redacao_display}

---

## ANALISE TECNICA

### Conceito Central

[Síntese do conteúdo normativo do artigo]

### Co-dependência normativa

[Esta regra depende de qual outro instrumento — CF, tratado internacional, LINDB, IN?]

---

## ARTIGOS CORRELATOS

### Mesma Lei
- [[{sigla} Art. {art_anterior}]] — artigo anterior
- [[{sigla} Art. {art_seguinte}]] — artigo seguinte

### Tratados e outros ramos
{correlatos_str}

---

## JURISPRUDENCIA

{juris_str}

---

## OBSERVACOES PRATICAS

{obs_str}

---

**Última atualização:** {datetime.now().strftime("%Y-%m-%d")}
"""
        return f"---\n{fm_str}---\n\n{corpo}"

    def salvar_artigo(self, artigo: Dict, conteudo: str, sigla: str) -> Path:
        pasta = self.output_base / sigla
        pasta.mkdir(parents=True, exist_ok=True)

        filename = f"{sigla} Art. {artigo['numero']}.md"
        filepath = pasta / filename

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(conteudo)
            return filepath
        except Exception as e:
            print(f"Erro ao salvar {filename}: {e}")
            return None


if __name__ == "__main__":
    gen = MarkdownGeneratorDI(Path("test_output_di"))
    print("Gerador Direito Internacional pronto")

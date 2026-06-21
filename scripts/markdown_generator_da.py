#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera notas Markdown atômicas para artigos de leis de Direito Administrativo."""
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from config_direito_administrativo import TAGS_PADRAO


# Jurisprudência curada: teses STJ/STF/TCU por artigo
JURIS_DA = {
    "37": [  # CF/88 art. 37 — princípios da Administração Pública
        "STF — Súmula Vinculante 3: nos processos perante o TCU, asseguram-se o contraditório e a ampla defesa quando da decisão puder resultar anulação ou revogação de ato que beneficie o interessado.",
        "STF — Súmula Vinculante 13: a nomeação de cônjuge, companheiro ou parente em linha reta, colateral ou por afinidade, até o 3° grau, configura nepotismo, vedado pelo art. 37 caput.",
        "STJ — Tese: atos discricionários são controlados pelo Poder Judiciário quando violam proporcionalidade, razoabilidade ou desvio de finalidade.",
    ],
    "5": [  # Lei 8.666 — Art. 5° (Lei de Licitações)
        "STJ — A Lei 14.133/2021 (Nova Lei de Licitações) substituiu a Lei 8.666/93; contratos firmados sob a lei anterior são regidos pela legislação vigente à época da contratação.",
        "TCU — A dispensa de licitação é taxativa (art. 75 da Lei 14.133/2021); hipóteses não previstas configuram irregularidade sujeita à responsabilidade do agente.",
    ],
    "9": [  # Lei 8.429 — Improbidade
        "STJ — Tese (após Lei 14.230/2021): a improbidade administrativa exige dolo específico do agente; a modalidade culposa foi suprimida pela reforma.",
        "STF — ADI 6.428: a retroatividade das normas mais benéficas da Lei 14.230/2021 alcança ações em curso e prescrições em andamento.",
        "STJ — A prescrição das ações de improbidade é de 8 anos do fato (art. 23 da Lei 8.429/92, com alterações); após a Lei 14.230/2021 passou a ser de 8 anos do conhecimento do fato.",
    ],
    "41": [  # Estabilidade do servidor — CF art. 41
        "STF — A estabilidade do servidor público (art. 41 CF) só se adquire após 3 anos de efetivo exercício e aprovação em estágio probatório; cargo em comissão não gera estabilidade.",
        "STJ — A demissão do servidor estável exige processo administrativo com garantia de contraditório e ampla defesa; decisão sumária é nula.",
    ],
    "37_licitacao": [
        "STF — A dispensa de licitação por emergência (art. 75 da Lei 14.133) não admite contratação de empresa que causou a situação emergencial; configura desvio de finalidade.",
        "TCU — A contratação direta sem o devido procedimento configura dano ao erário; o gestor responde solidariamente com a empresa contratada.",
    ],
}

# Observações práticas
OBS_PRATICAS_DA = {
    "9": {
        "mp": "Após a Lei 14.230/2021, a denúncia/petição inicial de improbidade deve indicar explicitamente o dolo específico do agente; a alegação de culpa grave foi suprimida como fundamento autônomo.",
        "defesa": "Arguir ausência de dolo específico (principal inovação da Lei 14.230/2021); a negligência ou imprudência, por si sós, não configuram mais improbidade. Prescrição retroativa favorável deve ser invocada.",
        "pratica": "Lei 14.230/2021 trouxe grandes mudanças: (1) extinção da modalidade culposa; (2) retroatividade das normas benéficas; (3) prazo de prescrição de 8 anos; (4) acordo de não-persecução cível (ANPC) previsto no art. 17-B.",
    },
}


def _jurisprudencia_da(num_str: str, sigla: str) -> List[str]:
    chave = f"{num_str}_{sigla.lower()}" if f"{num_str}_{sigla.lower()}" in JURIS_DA else num_str
    return JURIS_DA.get(chave, JURIS_DA.get(num_str, []))


def _obs_praticas_da(num_str: str) -> dict:
    return OBS_PRATICAS_DA.get(num_str, {})


def _correlatos_outros_da(num_base, sigla: str) -> List[str]:
    correlatos = [
        "[[CF88 Art. 37]] — princípios da Administração Pública",
        "[[L13105 Art. 1]] — processo administrativo judicial (CPC subsidiário)",
    ]
    if "8429" in sigla or "improbidade" in sigla.lower():
        correlatos += ["[[DEL2848 Art. 312]] — improbidade e corrupção ativa (CP)"]
    return list(dict.fromkeys(correlatos))


class MarkdownGeneratorDA:
    """Gera notas Markdown estruturadas para artigos de leis administrativas."""

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
        tema = lei_cfg.get("tema", "direito-administrativo")

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
            "direito_administrativo": True,
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

        juris = _jurisprudencia_da(num_str, sigla)
        if juris:
            juris_str = "\n".join(f"- {j}" for j in juris)
            juris_str += "\n\n[Conferir atualização: STJ «Jurisprudência em Teses»; TCU — Jurisprudência]"
        else:
            juris_str = "[Conferir atualização: STJ «Jurisprudência em Teses»; TCU — Jurisprudência]"

        obs = _obs_praticas_da(num_str)
        if obs:
            obs_str = (
                f"- **MP/Acusação:** {obs.get('mp', '')}\n"
                f"- **Defesa:** {obs.get('defesa', '')}\n"
                f"- **Prática:** {obs.get('pratica', '')}"
            )
        else:
            obs_str = "[Aplicação na prática administrativa — preencher com experiência do caso concreto]"

        correlatos = _correlatos_outros_da(num, sigla)
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

[Esta regra depende de qual outro instrumento — CF Art. 37, decreto regulamentador, legislação especial?]

---

## ARTIGOS CORRELATOS

### Mesma Lei
- [[{sigla} Art. {art_anterior}]] — artigo anterior
- [[{sigla} Art. {art_seguinte}]] — artigo seguinte

### Outros ramos
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
    gen = MarkdownGeneratorDA(Path("test_output_da"))
    print("Gerador Direito Administrativo pronto")

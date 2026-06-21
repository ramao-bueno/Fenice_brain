#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera notas Markdown atômicas para artigos de leis de Direito Previdenciário."""
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from config_direito_previdenciario import TAGS_PADRAO


# Jurisprudência curada: teses STJ/STF/TNU por artigo
JURIS_DP = {
    "1": [  # Lei 8.213 — art. 1° (princípios RPPS)
        "STF — A Previdência Social (art. 201 CF) é direito social de seguridade; o princípio da solidariedade exige custeio coletivo e não se confunde com seguro privado.",
        "STJ — Tese: a aposentadoria é ato complexo (requerimento + concessão); o direito adquirido nasce no momento em que o segurado preenche os requisitos, não na data do requerimento.",
    ],
    "15": [  # Qualidade de segurado — Lei 8.213 art. 15
        "STJ — Tese: a qualidade de segurado é mantida pelo período de graça (art. 15); o segurado desempregado tem até 36 meses de manutenção após o último vínculo.",
        "TNU — Súmula 27: é possível o reconhecimento de tempo de serviço rural por meio de documentos indiretos (certidão de casamento com qualificação de lavrador, por exemplo).",
    ],
    "29": [  # Salário de benefício — Lei 8.213 art. 29
        "STJ — Tese: o salário de benefício é calculado com base nas contribuições dos 80% maiores salários de contribuição (após EC 20/98); períodos anteriores à EC 20/98 podem ser calculados pela regra anterior se mais favorável.",
        "STF — O período básico de cálculo (PBC) deve incluir competências de todo o CNIS, inclusive períodos rurais com salário de contribuição presumido.",
    ],
    "42": [  # Aposentadoria por invalidez
        "STJ — Tese: a aposentadoria por invalidez não exige incapacidade total e definitiva; basta a incapacidade para a função habitual com impossibilidade de reabilitação a curto prazo.",
        "TNU — Súmula 47: uma vez deferida medida liminar para implantar benefício previdenciário, não cabe o INSS suspendê-lo unilateralmente.",
    ],
    "57": [  # Aposentadoria especial
        "STJ — Tese: a aposentadoria especial exige efetiva exposição a agente nocivo; o EPI eficaz que neutraliza totalmente o agente nocivo afasta o direito ao especial (STF — ARE 664.335).",
        "STF — ARE 664.335 (repercussão geral): o deferimento do EPI eficaz afasta o direito à aposentadoria especial; mas o risco residual é aferido caso a caso.",
        "TNU — Súmula 68: o laudo pericial não é meio exclusivo de prova da especialidade; o PPP (Perfil Profissiográfico Previdenciário) tem presunção de veracidade.",
    ],
    "74": [  # Pensão por morte
        "STJ — Tese: a pensão por morte exige qualidade de segurado do de cujus na data do óbito; a qualidade é mantida durante o período de graça (art. 15).",
        "STF — RE 1.270.983 (tese vinculante): a pensão por morte calculada pelas regras anteriores à EC 103/2019 se aplica quando o óbito ocorreu antes da emenda.",
        "STJ — Súmula 336: a mulher que renunciou aos alimentos na separação judicial tem direito à pensão previdenciária por morte do ex-marido, comprovada a necessidade econômica superveniente.",
    ],
    "86": [  # Auxílio-acidente
        "STJ — Tese: o auxílio-acidente é devido quando a sequela reduz a capacidade laborativa para a atividade habitual, ainda que não impeça o trabalho; é compatível com benefício de aposentadoria por tempo de contribuição se esta foi requerida antes do acidente.",
    ],
}

# Observações práticas por artigo
OBS_PRATICAS_DP = {
    "42": {
        "autor": "Na ação de aposentadoria por invalidez, juntar laudos médicos e relatórios de tratamento; requerer perícia judicial imparcial quando o laudo do INSS for desfavorável; explorar a impossibilidade de reabilitação profissional.",
        "defesa_inss": "O INSS pode requerer perícia de alta (art. 101 da Lei 8.213) periódica; alta sem recuperação da capacidade é passível de mandado de segurança.",
        "pratica": "DIB (Data de Início do Benefício): regra geral — data do requerimento; se o requerimento for feito em até 30 dias do afastamento, retroage à data do afastamento (art. 60). DER (Data de Entrada do Requerimento) é fundamental para cálculo da DIB.",
    },
    "57": {
        "autor": "Para aposentadoria especial, o PPP (Perfil Profissiográfico Previdenciário) é o documento principal; o LTCAT (Laudo Técnico das Condições Ambientais de Trabalho) comprova a exposição; são documentos distintos e complementares.",
        "defesa_inss": "O INSS pode questionar a veracidade do PPP solicitando fiscalização ao empregador; laudos genéricos que não individualizam a exposição ao trabalhador específico podem ser contestados.",
        "pratica": "Lista de agentes nocivos: NR-15 (ruído, calor, agentes químicos) + Decreto 3.048/99 (Anexos IV e V). Contagem de tempo especial: período integral, ainda que intercalado com períodos comuns.",
    },
    "74": {
        "autor": "Dependentes de 1ª classe (cônjuge, companheiro, filho menor de 21 anos ou inválido) têm habilitação presumida; dependentes de 2ª e 3ª classes devem provar dependência econômica.",
        "defesa_inss": "Impugnar a qualidade de segurado do de cujus se o óbito ocorreu após perda dessa qualidade e fora do período de graça; verificar carência exigida.",
        "pratica": "União estável: companheiro tem direito à pensão por morte; prova por qualquer meio lícito (contrato de convivência, declaração de IR, conta conjunta). União homoafetiva: reconhecida pelo STF — IN 45/2010 INSS.",
    },
}


def _jurisprudencia_dp(num_str: str) -> List[str]:
    return JURIS_DP.get(num_str, [])


def _obs_praticas_dp(num_str: str) -> dict:
    return OBS_PRATICAS_DP.get(num_str, {})


def _correlatos_outros_dp(num_base, sigla: str) -> List[str]:
    correlatos = [
        "[[CF88 Art. 201]] — Regime Geral de Previdência Social",
        "[[CF88 Art. 194]] — seguridade social",
    ]
    if "8212" in sigla:
        correlatos += ["[[L8213 Art. 1]] — plano de benefícios (lei gêmea)"]
    elif "8213" in sigla:
        correlatos += ["[[L8212 Art. 1]] — custeio da previdência (lei gêmea)"]
    correlatos += ["[[DEC3048 Art. 1]] — Regulamento da Previdência Social"]
    return list(dict.fromkeys(correlatos))


class MarkdownGeneratorDP:
    """Gera notas Markdown estruturadas para artigos de leis previdenciárias."""

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
        tema = lei_cfg.get("tema", "direito-previdenciario")

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
            "direito_previdenciario": True,
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

        juris = _jurisprudencia_dp(num_str)
        if juris:
            juris_str = "\n".join(f"- {j}" for j in juris)
            juris_str += "\n\n[Conferir atualização: STJ «Jurisprudência em Teses»; Temas STF; TNU — Súmulas]"
        else:
            juris_str = "[Conferir atualização: STJ «Jurisprudência em Teses»; Temas STF; TNU — Súmulas]"

        obs = _obs_praticas_dp(num_str)
        if obs:
            obs_str = (
                f"- **Segurado/Autor:** {obs.get('autor', '')}\n"
                f"- **INSS/Réu:** {obs.get('defesa_inss', '')}\n"
                f"- **Prática:** {obs.get('pratica', '')}"
            )
        else:
            obs_str = "[Aplicação na prática forense previdenciária — preencher com experiência do caso concreto]"

        correlatos = _correlatos_outros_dp(num, sigla)
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

[Esta regra depende de qual outro instrumento — CF Art. 201/202, Decreto 3.048/99, lei complementar?]

---

## ARTIGOS CORRELATOS

### Mesma Lei
- [[{sigla} Art. {art_anterior}]] — artigo anterior
- [[{sigla} Art. {art_seguinte}]] — artigo seguinte

### Lei gêmea e regulamento
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
    gen = MarkdownGeneratorDP(Path("test_output_dp"))
    print("Gerador Direito Previdenciário pronto")

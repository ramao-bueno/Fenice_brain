#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera notas Markdown atômicas para artigos de Processo Penal."""
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from config_codigo_processo_penal import TAGS_PADRAO


# Jurisprudência curada: súmulas e teses STJ/STF por artigo DEL3689
JURIS_CPP = {
    "1": [
        "STJ — O CPP se aplica a todos os processos penais salvo disposição especial de lei; leis especiais (Lei de Drogas, Maria da Penha, Lei de Improbidade) prevalecem no que conflitam.",
        "STF — O contraditório e a ampla defesa (CF/88, art. 5°, LV) são autoaplicáveis no processo penal e prevalecem sobre normas processuais restritivas.",
    ],
    "41": [
        "STJ — Súmula 234: a Constituição não proíbe a atuação dos mesmos magistrados em fases distintas do processo penal.",
        "STJ — Tese: a denúncia deve descrever a conduta, a autoria e o nexo causal com clareza mínima; inépcia formal não se confunde com insuficiência de provas.",
        "STF — A denúncia genérica em crimes de autoria coletiva (lavagem, organização criminosa) é admitida quando impossível individualizar condutas no momento do oferecimento.",
    ],
    "155": [
        "STF — Proibição de condenação fundada exclusivamente em prova produzida no inquérito policial; prova inquisitorial deve ser repetida em juízo.",
        "STJ — Tese: o juiz forma sua convicção pela livre apreciação das provas, mas deve fundamentar a decisão (art. 93, IX CF); motivação per relationem é admitida com parcimônia.",
    ],
    "157": [
        "STF — Provas ilícitas são inadmissíveis (art. 5°, LVI CF); prova derivada da ilícita também é contaminada pela teoria dos frutos da árvore envenenada (fruit of the poisonous tree).",
        "STF — Exceções à teoria: descoberta inevitável, fonte independente e limitação da contaminação. As exceções devem ser demonstradas concretamente pelo acusador.",
    ],
    "212": [
        "STJ — Tese: o magistrado é fiscal da inquirição e pode fazer perguntas complementares após as partes, mas não pode assumir a posição de acusador (sistema acusatório — art. 3-A CPP).",
        "STF — O sistema acusatório (EC 45/2004 + Lei 13.964/2019 — Pacote Anticrime) proíbe que o juiz de garantias tome providências investigatórias de ofício.",
    ],
    "312": [
        "STJ — Tese: a prisão preventiva exige concretude dos fundamentos; alegações genéricas de periculosidade ou gravidade abstrata do crime não são suficientes.",
        "STF — HC 84.078: a prisão antes do trânsito em julgado só se admite de forma cautelar; execução antecipada da pena é inconstitucional.",
        "STJ — Súmula 697 (STF): a proibição de liberdade provisória nos processos por crimes hediondos não veda o relaxamento da prisão processual por excesso de prazo.",
    ],
    "316": [
        "STJ — Tese: a prisão preventiva deve ser revisada periodicamente (art. 316 §único — a cada 90 dias); juiz deve proferir decisão fundamentada de ofício.",
        "STJ — A inobservância do prazo de revisão (art. 316, §único) gera relaxamento da prisão por excesso de prazo (art. 648, II CPP).",
    ],
    "383": [
        "STJ — Emendatio libelli (art. 383): o juiz pode dar ao fato classificação diversa sem alterar a descrição fática; não exige nova manifestação das partes.",
        "STJ — Distinção: emendatio (mesmo fato, nova classificação) vs. mutatio libelli (fato diverso — art. 384, exige aditamento da denúncia e nova instrução).",
    ],
    "387": [
        "STJ — Tese: a sentença deve fixar o valor mínimo de indenização (art. 387, IV) quando houver prova nos autos de dano material à vítima, dispensando liquidação posterior.",
        "STJ — Tese: a reincidência (art. 61, I CP) não é bis in idem quando usada para agravar a pena (art. 68 CP): é considerada na 2ª fase da dosimetria, não na 3ª.",
    ],
    "397": [
        "STJ — Tese: a absolvição sumária (art. 397) é medida excepcional; deve ser usada apenas quando a improcedência for manifesta (atipicidade, extinção da punibilidade, excludentes evidentes).",
        "STF — A extinção da punibilidade (art. 107 CP) pode ser reconhecida a qualquer tempo, inclusive na absolvição sumária.",
    ],
    "563": [
        "STJ — Pas de nullité sans grief: a nulidade processual exige demonstração de prejuízo concreto (art. 563 CPP); meras formalidades não são causa de nulidade.",
        "STJ — Nulidades relativas: devem ser arguidas no momento oportuno; a preclusão impede arguição posterior. Nulidades absolutas podem ser arguidas a qualquer tempo.",
    ],
    "621": [
        "STJ — A revisão criminal (art. 621) é ação autônoma de impugnação; não há prazo para propositura; pode ser proposta pelo réu, cônjuge, ascendentes, descendentes e irmãos.",
        "STJ — Tese: a revisão criminal não cabe para prejudicar o réu (reformatio in pejus); visa exclusivamente desconstituir condenações injustas.",
    ],
}

# Observações práticas por artigo
OBS_PRATICAS_CPP = {
    "41": {
        "mp": "A denúncia deve ser clara na descrição do fato e da autoria; admite-se denúncia genérica em crimes plurissubjetivos (organização criminosa, quadrilha) quando impossível individualizar condutas no início.",
        "defesa": "Arguir inépcia formal da denúncia por falta de descrição fática ou de autoria específica; inépcia material (falta de provas) deve ser combatida na absolvição sumária (art. 397) ou no mérito.",
        "pratica": "Rejeição da denúncia (art. 395): manifesta ilegitimidade da parte, falta de justa causa ou inépcia formal. Decisão irrecorrível pelo MP via RESE (art. 581, I).",
    },
    "157": {
        "mp": "Demonstrar que a prova, mesmo que obtida irregularmente, deriva de fonte independente ou seria descoberta inevitavelmente; afastar a contaminação com argumento de compartimentação investigativa.",
        "defesa": "Requerer o desentranhamento da prova ilícita e de todas as provas dela derivadas; documentar a cadeia de causalidade entre a prova maculada e as derivadas.",
        "pratica": "Prova emprestada de processo civil é admissível no processo penal se produzida com contraditório; prova de interceptação telefônica ilegal (sem autorização judicial) é inadmissível e contamina o processo.",
    },
    "312": {
        "mp": "Demonstrar concretamente os requisitos da preventiva: prova da existência do crime + indício de autoria + um dos fundamentos do art. 312 (garantia da ordem pública, instrução criminal, etc.).",
        "defesa": "Impugnar a preventiva por falta de concretude: fundamentação abstrata baseada na gravidade do crime não basta. Requerer revogação (art. 316) ou HC se prazo de revisão (90 dias) não for observado.",
        "pratica": "Audiência de custódia (art. 310): obrigatória em 24h após flagrante. O juiz decide: relaxamento, liberdade provisória ou conversão em preventiva. Ausência de audiência de custódia gera nulidade.",
    },
    "387": {
        "mp": "Na fase de sentença, requerer expressamente fixação do valor mínimo de indenização (art. 387, IV) com base nos danos materiais comprovados nos autos; facilita execução civil posterior.",
        "defesa": "Impugnar o valor mínimo fixado se não há prova nos autos de dano material específico; o valor mínimo não afasta liquidação civil posterior para apuração do dano real.",
        "pratica": "Dosimetria — três fases obrigatórias: (1) pena-base (art. 59 CP); (2) agravantes/atenuantes (arts. 61-65 CP); (3) causas de aumento/diminuição. Cada fase deve ser fundamentada individualmente.",
    },
    "563": {
        "mp": "Arguir preclusão de nulidades relativas não arguidas na fase oportuna pela defesa; demonstrar ausência de prejuízo para afastar nulidade.",
        "defesa": "Distinguir nulidade relativa (preclusão) de nulidade absoluta (arguível a qualquer tempo, ex: falta de defesa técnica, incompetência absoluta, ausência de intimação pessoal do réu).",
        "pratica": "Interrogatório do réu: é o último ato da instrução (Lei 11.719/2008); a inobservância da ordem é nulidade relativa. O réu tem direito ao silêncio (art. 5°, LXIII CF); não pode ser valorado negativamente.",
    },
}


def _jurisprudencia_cpp(num_str: str) -> List[str]:
    return JURIS_CPP.get(num_str, [])


def _obs_praticas_cpp(num_str: str) -> dict:
    return OBS_PRATICAS_CPP.get(num_str, {})


def _correlatos_outros_cpp(num_base) -> List[str]:
    try:
        num_base = int(num_base)
    except (ValueError, TypeError):
        num_base = -1
    correlatos = []
    if num_base == 157:
        correlatos += [
            "[[CF88 Art. 5]] — inadmissibilidade de provas ilícitas (LVI)",
        ]
    elif 312 <= num_base <= 316:
        correlatos += [
            "[[DEL2848 Art. 312]] — prisão preventiva",
            "[[CF88 Art. 5]] — liberdade (LXI, LXVIII)",
        ]
    elif num_base == 387:
        correlatos += [
            "[[DEL2848 Art. 59]] — dosimetria da pena (CP)",
            "[[DEL2848 Art. 68]] — método trifásico",
        ]
    correlatos += [
        "[[CF88 Art. 5]] — garantias processuais penais (CF/88)",
        "[[DEL2848 Art. 1]] — aplicação do CP",
    ]
    return list(dict.fromkeys(correlatos))


class MarkdownGeneratorCPP:
    """Gera notas Markdown estruturadas para artigos de processo penal."""

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
        categoria = artigo.get("categoria", lei_cfg.get("categoria", "PROCESSO_PENAL"))
        tema = lei_cfg.get("tema", "processo-penal")

        tags = TAGS_PADRAO.copy()
        for t in [categoria.lower(), f"art-{num}", tema, sigla.lower()]:
            if t not in tags:
                tags.append(t)

        frontmatter = {
            "artigo": num_str,
            "lei": f"{lei_numero} — {nome_lei}",
            "sigla": sigla,
            "categoria": categoria,
            "status": "vigente",
            "processo_penal": True,
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

        juris = _jurisprudencia_cpp(num_str)
        if juris:
            juris_str = "\n".join(f"- {j}" for j in juris)
            juris_str += "\n\n[Conferir atualização: STJ «Jurisprudência em Teses»; Informativos STF/STJ]"
        else:
            juris_str = "[Conferir atualização: STJ «Jurisprudência em Teses»; Informativos STF/STJ]"

        obs = _obs_praticas_cpp(num_str)
        if obs:
            obs_str = (
                f"- **MP/Acusação:** {obs.get('mp', '')}\n"
                f"- **Defesa:** {obs.get('defesa', '')}\n"
                f"- **Prática:** {obs.get('pratica', '')}"
            )
        else:
            obs_str = "[Aplicação concreta na prática forense: como promotores, defensores e juízes utilizam este artigo?]"

        correlatos = _correlatos_outros_cpp(num)
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

### Conceito Processual Penal

[Síntese do conceito processual penal: qual é a regra ou princípio que este artigo estabelece?]

### Fase Processual

[Em qual fase do processo penal este artigo atua? (Inquérito, instrução, sentença, recursos?)]

### Conexão com Direito Material

[Como este artigo de processo se articula com o direito penal material (CP)?]

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
    gen = MarkdownGeneratorCPP(Path("test_output_cpp"))
    print("Gerador Código de Processo Penal pronto")

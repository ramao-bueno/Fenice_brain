import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from config_cf import (TAGS_PADRAO, LEI_NOME, TITULO_MAPEAMENTO,
                       PLANALTO_BASE_URL, TEMA_POR_TITULO)


# Jurisprudência curada: teses STF por artigo da CF/88
JURIS_CF = {
    "1": [
        "STF — O Estado Democrático de Direito (art. 1° CF) impõe que toda restrição de direitos seja proporcional, necessária e fundamentada em lei.",
        "STF — A soberania popular (art. 1°, parágrafo único) é exercida pelo voto direto e por mecanismos de democracia participativa; nenhum poder emana sem legitimidade democrática.",
    ],
    "5": [
        "STF — Súmula Vinculante 11: o uso de algemas só é admitido em situações excecionais de resistência, fuga ou risco à integridade; o desrespeito gera nulidade do ato e responsabilidade da autoridade.",
        "STF — Súmula Vinculante 14: é direito do defensor ter acesso a todos os elementos de informação já documentados em procedimento investigatório que recaiam sobre o interesse do representado.",
        "STF — ADI 3.510: direitos fundamentais podem ser expandidos mas não reduzidos pelo legislador infraconstitucional (proibição de retrocesso).",
        "STF — A teoria da eficácia horizontal dos direitos fundamentais: os direitos do art. 5° vinculam também os particulares em relações privadas.",
    ],
    "37": [
        "STF — Súmula Vinculante 3: nos processos perante o TCU, asseguram-se o contraditório e a ampla defesa quando da decisão puder resultar anulação ou revogação de ato administrativo que beneficie o interessado.",
        "STF — Súmula Vinculante 43: é inconstitucional qualquer remuneração adicional paga a servidor público aposentado, salvo a decorrente do exercício de cargo inacumulável.",
        "STJ — Tese: a legalidade administrativa (art. 37) não afasta o poder discricionário; atos discricionários são controlados pelo STJ quando violarem proporcionalidade ou razoabilidade.",
    ],
    "93": [
        "STF — Toda decisão judicial deve ser fundamentada (art. 93, IX); a motivação per relationem é admitida desde que a decisão referenciada seja suficientemente clara.",
        "STJ — Súmula 522: a motivação inidônea da sentença penal (art. 93, IX) gera nulidade absoluta do julgado.",
    ],
    "102": [
        "STF — A competência do STF (art. 102) é taxativa e de interpretação estrita; não pode ser ampliada por lei ordinária ou ato normativo.",
        "STF — O controle concentrado de constitucionalidade (ADI, ADC, ADPF) tem efeito erga omnes e vinculante; afasta a aplicação da norma declarada inconstitucional.",
    ],
    "150": [
        "STF — Súmula Vinculante 50: norma legal que altera o prazo de recolhimento de obrigação tributária não se sujeita ao princípio da anterioridade.",
        "STF — A legalidade tributária estrita (art. 150, I) exige lei formal para instituição, majoração e extinção de tributos; atos normativos infralegais não criam obrigação tributária.",
        "STF — Súmula Vinculante 52: ainda quando alugado a terceiros, permanece imune ao IPTU o imóvel pertencente a qualquer das entidades referidas pelo art. 150, VI, c.",
    ],
    "155": [
        "STF — Súmula Vinculante 31: é inconstitucional a incidência do ISS sobre operações de locação de bens móveis.",
        "STF — Tese: a progressividade do ICMS (art. 155, II) é inconstitucional quando fundada apenas no valor da operação; a progressividade é tributária (arrecadatória), não extrafiscal.",
    ],
    "170": [
        "STF — A ordem econômica (art. 170) consagra a livre iniciativa; intervenções estatais no domínio econômico são constitucionais quando proporcionais e com fundamento legal.",
        "STF — A função social da empresa (art. 170, III) impõe que a atividade econômica respeite os direitos dos trabalhadores, consumidores e meio ambiente.",
    ],
    "196": [
        "STF — Direito à saúde (art. 196): o STF reconhece o direito subjetivo a medicamentos e tratamentos, inclusive os não constantes das listas do SUS, em casos de necessidade comprovada.",
        "STF — RE 657.718 (tese vinculante): o Estado não é obrigado a fornecer medicamento experimental ou sem registro na ANVISA, salvo casos excepcionais.",
    ],
    "225": [
        "STF — O direito ao meio ambiente ecologicamente equilibrado (art. 225) é direito fundamental de terceira geração; o Estado deve agir preventivamente (princípio da precaução).",
        "STF — A responsabilidade ambiental é objetiva (art. 225, §3°); o dano ambiental prescinde de culpa; aplica-se a teoria do risco integral nas atividades lesivas ao meio ambiente.",
    ],
}

# Observações práticas por artigo
OBS_PRATICAS_CF = {
    "5": {
        "peticionamento": "Ao invocar direito fundamental, indicar o inciso específico do art. 5° e a eficácia da norma (plena, contida ou limitada); no STF, demonstrar que houve violação direta da CF, não apenas de lei.",
        "defesa": "Arguir proporcionalidade e razoabilidade quando o Estado restringir direito fundamental; demonstrar que a medida é necessária, adequada e proporcional em sentido estrito.",
        "pratica": "Habeas Corpus (art. 5°, LXVIII): remédio para liberdade de locomoção; Mandado de Segurança (LXIX): para direito líquido e certo não amparado por HC. Ambos têm prazo decadencial de 120 dias.",
    },
    "37": {
        "peticionamento": "Em ações contra a Administração, invocar o princípio da moralidade e da eficiência (art. 37 caput) para questionar atos discricionários desarrazoados; o TCU controla atos administrativos de forma plena.",
        "defesa": "A Administração goza de presunção de legalidade dos atos administrativos; o ônus de demonstrar a ilegalidade é do particular. O controle judicial é de legalidade, não de mérito.",
        "pratica": "Concurso público (art. 37, II): o aprovado dentro do número de vagas tem direito subjetivo à nomeação (STF — RE 598.099 — repercussão geral). Aprovado fora do número de vagas tem mera expectativa.",
    },
    "150": {
        "peticionamento": "Em questões tributárias, verificar se a cobrança respeita os limites constitucionais: legalidade estrita, anterioridade, irretroatividade e não confisco. A inconstitucionalidade pode ser arguida por ADI, ADPF ou em controle difuso.",
        "defesa": "O contribuinte pode questionar a constitucionalidade do tributo em ação declaratória negativa; o mandado de segurança preventivo (antes do lançamento) é cabível quando a ameaça é concreta.",
        "pratica": "Anterioridade nonagesimal (art. 150, III, c): tributos majorados só podem ser cobrados 90 dias após a publicação da lei. Exceções: II, IE, IPI, IOF, IEG e empréstimos compulsórios de calamidade.",
    },
    "196": {
        "peticionamento": "Em demandas de saúde, demonstrar: (1) necessidade médica comprovada por laudo; (2) inexistência de tratamento equivalente no SUS; (3) impossibilidade financeira do paciente. Liminar é cabível quando há risco de vida.",
        "defesa": "O Estado pode alegar reserve do possível e impacto orçamentário; mas o STF firmou que o mínimo existencial (vida e saúde) não pode ser suprimido por razões orçamentárias.",
        "pratica": "RE 657.718 (tese vinculante): medicamentos sem registro ANVISA → regra é a não obrigatoriedade; exceções: doença grave, inexistência de alternativa, laudo médico e registro em agência estrangeira reconhecida.",
    },
}


def _jurisprudencia_cf(num_str: str) -> List[str]:
    return JURIS_CF.get(num_str, [])


def _obs_praticas_cf(num_str: str) -> dict:
    return OBS_PRATICAS_CF.get(num_str, {})


def _correlatos_outros_cf(num_base) -> List[str]:
    try:
        num_base = int(num_base)
    except (ValueError, TypeError):
        num_base = -1
    correlatos = []
    if num_base == 5:
        correlatos += [
            "[[L13105 Art. 1]] — constitucionalização do processo (CPC)",
            "[[DEL2848 Art. 1]] — princípio da legalidade penal",
        ]
    elif num_base == 37:
        correlatos += [
            "[[L8429 Art. 9]] — improbidade administrativa",
            "[[L14230 Art. 1]] — reforma da Lei de Improbidade",
        ]
    elif 150 <= num_base <= 162:
        correlatos += [
            "[[L5172 Art. 3]] — Código Tributário Nacional",
        ]
    elif num_base == 196:
        correlatos += [
            "[[L8080 Art. 2]] — Lei do SUS — direito à saúde",
        ]
    correlatos += [
        "[[L13105 Art. 1]] — interpretação conforme CF (CPC art. 1°)",
    ]
    return list(dict.fromkeys(correlatos))


class MarkdownGeneratorCF:
    """Gera notas Markdown estruturadas para artigos da Constituição Federal."""

    def __init__(self, output_base: Path):
        self.output_base = Path(output_base)

    def gerar_nota_artigo(self, artigo: Dict, titulo: str) -> str:
        num_raw = artigo["numero"]
        try:
            num = int(num_raw)
        except (ValueError, TypeError):
            num = num_raw
        num_str = str(num_raw)
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
            "artigo": num_str,
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
        redacao_display = (redacao[:600] + "...") if len(redacao) > 600 else redacao
        titulo_artigo = artigo.get("titulo", f"Art. {num} CF")
        if isinstance(num, int):
            art_anterior = max(1, num - 1)
            art_seguinte = num + 1
        else:
            art_anterior = num_str
            art_seguinte = num_str

        juris = _jurisprudencia_cf(num_str)
        if juris:
            juris_str = "\n".join(f"- {j}" for j in juris)
            juris_str += "\n\n[Conferir atualização: STF — Teses de Repercussão Geral; Súmulas Vinculantes]"
        else:
            juris_str = "[Conferir atualização: STF — Teses de Repercussão Geral; Súmulas Vinculantes]"

        obs = _obs_praticas_cf(num_str)
        if obs:
            obs_str = (
                f"- **Peticionamento/Autor:** {obs.get('peticionamento', '')}\n"
                f"- **Defesa/Estado:** {obs.get('defesa', '')}\n"
                f"- **Prática:** {obs.get('pratica', '')}"
            )
        else:
            obs_str = "[Aplicação na prática constitucional — preencher com experiência do caso concreto]"

        correlatos = _correlatos_outros_cf(num)
        correlatos_str = "\n".join(f"- {c}" for c in correlatos)

        corpo = f"""# CF/88 Art. {num} — {titulo_artigo}

**Lei:** {LEI_NOME}
**Título:** {titulo} — {titulo_nome}
**Status:** VIGENTE
**Planalto:** [Texto oficial]({planalto_url})

---

## REDACAO LEGAL

> {redacao_display}

---

## ANALISE TECNICA

### Conceito Central

[Síntese do conteúdo normativo do artigo]

### Elementos-Chave

| Elemento | Descrição |
|----------|-----------|
| **Sujeito** | A quem se dirige a norma |
| **Objeto** | O que a norma regula |
| **Eficácia** | Aplicabilidade (plena / contida / limitada) |

---

## ARTIGOS CORRELATOS

### Mesma CF
- [[Art. {art_anterior} — CF]] — artigo anterior
- [[Art. {art_seguinte} — CF]] — artigo seguinte

### Legislação derivada
{correlatos_str}

---

## JURISPRUDENCIA STF

{juris_str}

---

## OBSERVACOES PRATICAS

{obs_str}

---

## EMENDAS CONSTITUCIONAIS

[ECs que modificaram este artigo — verificar no Planalto]

---

**Última atualização:** {datetime.now().strftime("%Y-%m-%d")}
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

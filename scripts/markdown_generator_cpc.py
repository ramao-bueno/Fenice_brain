#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera notas Markdown atômicas para artigos do Código de Processo Civil."""
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from config_codigo_processo_civil import TAGS_PADRAO


# Jurisprudência curada: súmulas e teses STJ/STF por artigo L13105
JURIS_CPC = {
    "1": [
        "STF — O processo civil deve ser interpretado conforme a Constituição; garantias do art. 5° CF (contraditório, ampla defesa, devido processo legal) são autoaplicáveis no processo.",
        "STJ — Tese: a constitucionalização do processo (art. 1° CPC) exige que normas processuais sejam lidas à luz dos direitos fundamentais.",
    ],
    "4": [
        "STJ — Tese: o juiz deve promover a solução consensual a qualquer tempo (art. 4° e 139, V); a homologação de acordo judicial tem eficácia de título executivo judicial.",
        "STJ — A mediação e conciliação realizadas antes do ajuizamento (art. 174) não interrompem a prescrição, mas a suspensão pode ser arguida.",
    ],
    "17": [
        "STJ — Súmula 258: a nota promissória vinculada a contrato de abertura de crédito não goza de autonomia; é necessária a juntada do contrato para execução.",
        "STJ — Tese: o interesse de agir (art. 17) é aferido em abstrato; não se exige prova prévia do dano para propositura de ação preventiva.",
    ],
    "139": [
        "STJ — Os poderes do juiz (art. 139) não autorizam decisão surpresa; o contraditório deve ser observado antes de qualquer medida de ofício.",
        "STJ — Tese: a cláusula geral de poderes do juiz (art. 139, IV) permite medidas atípicas de execução (bloqueio de CNH, passaporte, cartão de crédito) quando as típicas forem ineficazes.",
    ],
    "319": [
        "STJ — A petição inicial deve indicar com clareza os pedidos e a causa de pedir; o pedido genérico é cabível apenas nas hipóteses do art. 324.",
        "STJ — Tese: a emenda da inicial (art. 321) deve ser admitida quando for possível sanar os vícios apontados; a extinção prematura viola o princípio da primazia do julgamento de mérito.",
    ],
    "330": [
        "STJ — O julgamento antecipado do mérito (art. 330) só é cabível quando a questão for exclusivamente de direito ou quando a prova documental já bastante nos autos.",
        "STJ — Tese: o julgamento antecipado sem ouvir as partes sobre os documentos juntados viola o contraditório (art. 9° CPC).",
    ],
    "373": [
        "STJ — Súmula 479: nas operações bancárias, inverte-se o ônus da prova em favor do consumidor (CDC + art. 373, II CPC).",
        "STJ — Tese: a inversão do ônus da prova (art. 373, §1°) deve ser feita antes da fase probatória para não causar surpresa.",
        "STJ — Tese: o ônus da prova é regra de julgamento (art. 373) e não de produção de prova; deve ser aplicado apenas quando o juiz não conseguir se convencer pelos elementos dos autos.",
    ],
    "485": [
        "STJ — Tese: a extinção sem resolução de mérito (art. 485) não faz coisa julgada material; nova ação pode ser proposta (art. 486).",
        "STJ — Súmula 240: a extinção do processo, sem julgamento do mérito, em razão do abandono da causa pelo autor, depende de requerimento do réu.",
    ],
    "487": [
        "STJ — Tese: a sentença que julga o mérito (art. 487) faz coisa julgada material e impede rediscussão, salvo ação rescisória (art. 966) no prazo de 2 anos.",
        "STJ — A prescrição e decadência reconhecidas de ofício (art. 487, II) extinguem o processo com resolução do mérito.",
    ],
    "528": [
        "STJ — Súmula 309: o débito alimentar que autoriza a prisão civil (art. 528 §3°) é o que compreende as 3 prestações anteriores ao ajuizamento e as que se vencerem no curso do processo.",
        "STJ — Tese: a prisão civil do devedor de alimentos (art. 5°, LXVII CF) é cabível em regime fechado, pelo prazo de 1 a 3 meses por período.",
    ],
    "784": [
        "STJ — Súmula 233: o contrato de abertura de crédito, ainda que acompanhado de extrato da conta-corrente, não é título executivo.",
        "STJ — Súmula 300: o instrumento de confissão de dívida, ainda que originário de contrato de abertura de crédito, constitui título executivo extrajudicial.",
        "STJ — Tese: a certidão de dívida ativa (art. 784, IX) é título executivo; o executado pode se defender por embargos à execução (art. 917) ou exceção de pré-executividade.",
    ],
    "966": [
        "STJ — Tese: o prazo de 2 anos para ação rescisória (art. 975) começa da última decisão no processo, incluindo embargos de declaração.",
        "STJ — Súmula 401: o prazo decadencial da ação rescisória só começa a contar do trânsito em julgado da última decisão proferida na causa.",
        "STJ — Tese: a violação manifesta de norma jurídica (art. 966, V) abrange súmulas vinculantes e precedentes do STF com efeito erga omnes.",
    ],
    "1022": [
        "STJ — Súmula 98: embargos de declaração manifestados com notório propósito de prequestionamento não têm caráter protelatório.",
        "STJ — Tese: os embargos de declaração (art. 1.022) não servem para rediscutir o mérito da decisão; prestam-se apenas a aclarar obscuridade, eliminar contradição ou omissão.",
    ],
}

# Observações práticas por artigo
OBS_PRATICAS_CPC = {
    "139": {
        "autor": "Invocar art. 139, IV para medidas atípicas em execução (bloqueio de CNH, passaporte, cartão de crédito) quando devedores ocultam patrimônio; peticionar com fundamentação de insuficiência das medidas típicas.",
        "reu": "Impugnar medida atípica por desproporcionalidade; exigir que o credor comprove esgotamento das medidas típicas (penhora, bloqueio Sisbajud) antes da atípica.",
        "pratica": "STJ (EREsp 1.679.909) admitiu medidas atípicas; exige-se fundamentação concreta da insuficiência das típicas. Medidas como suspensão de CNH são controversas — evitar em caso de extrema necessidade do devedor.",
    },
    "373": {
        "autor": "Na inversão do ônus (relação de consumo, hipossuficiência), requerer expressamente antes da fase probatória; mostrar verossimilhança da alegação ou hipossuficiência técnica.",
        "reu": "Impugnar a inversão do ônus se não há relação de consumo ou se o autor tem plena capacidade probatória; demonstrar que a inversão viola isonomia processual.",
        "pratica": "Regra de distribuição dinâmica do ônus (§1°): juiz pode distribuir conforme maior facilidade de produção. Deve ser decidida antes da instrução, com ciência das partes, para não causar surpresa.",
    },
    "485": {
        "autor": "Verificar se a causa de extinção é sanável antes do trânsito em julgado; extinção sem mérito permite repropositura, mas com risco de nova extinção e preclusão temporal.",
        "reu": "Arguir extinção por ilegitimidade, falta de interesse de agir ou ausência de pressupostos processuais — elimina a ação sem análise do mérito, evitando coisa julgada favorável ao autor.",
        "pratica": "Abandono da causa (art. 485, III): requer intimação pessoal do autor para dar andamento em 5 dias + requerimento do réu. A extinção de ofício só é cabível para litígio (§1°).",
    },
    "528": {
        "autor": "Na execução de alimentos, requerer desconto em folha (art. 529) como primeira opção; subsidiariamente, penhora de bens e prisão civil (art. 528, §3°) para débito das 3 últimas parcelas.",
        "reu": "Purgar a mora (pagar o débito das 3 últimas parcelas) para evitar a prisão civil; apresentar justificativa plausível de impossibilidade de pagamento.",
        "pratica": "Prisão civil de alimentos: 1 a 3 meses em regime fechado, mas pode ser cumprida em prisão domiciliar se o devedor for idoso, doente ou responsável por crianças. Débito antigo (> 3 meses): execução por expropriação, não prisão.",
    },
    "784": {
        "autor": "Verificar a liquidez, certeza e exigibilidade do título antes de ajuizar execução; título ilíquido exige ação de conhecimento ou liquidação. Juntar contrato + planilha de débito atualizada.",
        "reu": "Embargos à execução (art. 914): prazo de 15 dias do depósito/penhora. Exceção de pré-executividade: cabível apenas para matérias de ordem pública cognoscíveis de ofício (prescrição, nulidade do título).",
        "pratica": "Sisbajud (antigo Bacenjud): bloqueio eletrônico de contas bancárias é a primeira medida em execução de quantia; autorizado de ofício após frustração de penhora (art. 854). Prazo: 24h para liberação após mandado judicial.",
    },
    "966": {
        "autor": "Ação rescisória: prazo de 2 anos do trânsito em julgado da última decisão (art. 975); propor no tribunal competente (art. 968). Depósito de 5% do valor da causa como pressuposto (art. 968, II).",
        "reu": "Impugnar a violação manifesta da norma jurídica (art. 966, V): mostrar que a questão era controvertida na jurisprudência à época da decisão; mera divergência não configura violação manifesta.",
        "pratica": "Rescisória é exceção ao princípio da imutabilidade da coisa julgada; STJ admite em casos de súmula vinculante do STF editada após o trânsito em julgado (art. 525, §15).",
    },
}


def _jurisprudencia_cpc(num_str: str) -> List[str]:
    return JURIS_CPC.get(num_str, [])


def _obs_praticas_cpc(num_str: str) -> dict:
    return OBS_PRATICAS_CPC.get(num_str, {})


def _correlatos_outros_cpc(num_base) -> List[str]:
    try:
        num_base = int(num_base)
    except (ValueError, TypeError):
        num_base = -1
    correlatos = []
    if 319 <= num_base <= 331:
        correlatos += [
            "[[L10406 Art. 186]] — ato ilícito (CC) — base da causa de pedir",
            "[[L8078 Art. 6]] — direitos do consumidor (CDC)",
        ]
    elif num_base == 373:
        correlatos += [
            "[[L8078 Art. 6]] — inversão do ônus de prova no CDC",
            "[[CF88 Art. 5]] — igualdade processual",
        ]
    elif 528 <= num_base <= 533:
        correlatos += [
            "[[L10406 Art. 1696]] — obrigação alimentar (CC)",
            "[[CF88 Art. 5]] — prisão civil por dívida alimentar",
        ]
    elif 784 <= num_base <= 788:
        correlatos += [
            "[[L6830 Art. 3]] — CDA como título executivo (Lei de Execução Fiscal)",
        ]
    elif 966 <= num_base <= 975:
        correlatos += [
            "[[CF88 Art. 5]] — coisa julgada (XXXVI)",
        ]
    correlatos += [
        "[[CF88 Art. 5]] — garantias processuais (CF/88)",
        "[[L10406 Art. 421]] — função social do contrato (CC)",
    ]
    return list(dict.fromkeys(correlatos))


class MarkdownGeneratorCPC:
    """Gera notas Markdown estruturadas para artigos do CPC."""

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
        categoria = artigo.get("categoria", lei_cfg.get("categoria", "CODIGO_PROCESSO_CIVIL"))
        tema = lei_cfg.get("tema", "processo-civil")

        tags = TAGS_PADRAO.copy()
        for t in [categoria.lower(), f"art-{num}", tema, sigla.lower()]:
            if t not in tags:
                tags.append(t)

        livro_info = self._detectar_livro_cpc(num) if (sigla == "L13105" and isinstance(num, int)) else None

        frontmatter = {
            "artigo": num_str,
            "lei": f"{lei_numero} — {nome_lei}",
            "sigla": sigla,
            "categoria": categoria,
            "status": "vigente" if "13105" in sigla else "revogado",
            "processo_civil": True,
            "relacionados": [],
            "tags": tags,
            "created": datetime.now().strftime("%Y-%m-%d"),
        }

        if livro_info:
            frontmatter.update(livro_info)

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

        juris = _jurisprudencia_cpc(num_str)
        if juris:
            juris_str = "\n".join(f"- {j}" for j in juris)
            juris_str += "\n\n[Conferir atualização: STJ «Jurisprudência em Teses»; Informativos STF/STJ]"
        else:
            juris_str = "[Conferir atualização: STJ «Jurisprudência em Teses»; Informativos STF/STJ]"

        obs = _obs_praticas_cpc(num_str)
        if obs:
            obs_str = (
                f"- **Autor/MP:** {obs.get('autor', '')}\n"
                f"- **Réu/Defesa:** {obs.get('reu', '')}\n"
                f"- **Prática:** {obs.get('pratica', '')}"
            )
        else:
            obs_str = "[Aplicação concreta no tribunal: como este artigo é utilizado na prática forense?]"

        correlatos = _correlatos_outros_cpc(num)
        correlatos_str = "\n".join(f"- {c}" for c in correlatos)

        corpo = f"""# {sigla} Art. {num} — {titulo_artigo}

**Lei:** {lei_numero} — {nome_lei}
**Categoria:** {categoria}
**Status:** {'VIGENTE' if '13105' in sigla else 'REVOGADO'}

---

## REDACAO LEGAL

> {redacao_display}

---

## ANALISE TECNICA

### Conceito Processual

[Síntese do conceito processual: qual é a regra ou princípio que este artigo estabelece?]

### Função no Processo

[Como este artigo estrutura o procedimento? Qual etapa do processo ele disciplina?]

### Co-dependência normativa

[Qual outro dispositivo do CPC, CC, CF ou lei especial depende desta regra?]

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

    @staticmethod
    def _detectar_livro_cpc(num: int) -> Dict:
        """Detecta qual livro/parte do CPC o artigo pertence."""
        if 1 <= num <= 77:
            return {"livro": "Preliminar", "titulo": "Disposições Preliminares"}
        elif 78 <= num <= 139:
            return {"livro": "I", "titulo": "Da Tutela Jurisdicional"}
        elif 140 <= num <= 295:
            return {"livro": "II", "titulo": "Da Composição e Competência"}
        elif 296 <= num <= 516:
            return {"livro": "III", "titulo": "Das Partes e dos Procuradores"}
        elif 517 <= num <= 771:
            return {"livro": "IV", "titulo": "Dos Atos Processuais"}
        elif 772 <= num <= 1072:
            return {"livro": "V", "titulo": "Do Processo de Conhecimento"}
        return {}


if __name__ == "__main__":
    gen = MarkdownGeneratorCPC(Path("test_output_cpc"))
    print("Gerador Código de Processo Civil pronto")

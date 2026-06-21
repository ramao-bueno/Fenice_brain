#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera notas Markdown atômicas para artigos do Código Civil."""
import re
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from config_codigo_civil import TAGS_PADRAO


# Jurisprudência curada: súmulas e teses STJ/STF por artigo
JURIS_CC = {
    "5": [
        "STJ — A incapacidade superveniente do agente não invalida o ato praticado quando ainda capaz.",
        "STJ — Menor emancipado responde civilmente pelos seus atos; a emancipação não afasta a responsabilidade civil.",
    ],
    "11": [
        "STJ — Súmula 403: independe de prova de dano a indenização pela publicação não autorizada de imagem de pessoa com fins econômicos ou comerciais.",
        "STJ — Os direitos da personalidade são intransmissíveis e irrenunciáveis; ação por dano moral é personalíssima, mas cabe aos herdeiros prosseguir em ação já proposta.",
    ],
    "186": [
        "STJ — Tese: o dano moral in re ipsa dispensa prova do prejuízo; presume-se da própria ofensa à dignidade.",
        "STJ — Súmula 227: a pessoa jurídica pode sofrer dano moral.",
        "STF — Súmula 37: são cumuláveis as indenizações por dano material e dano moral oriundos do mesmo fato.",
    ],
    "187": [
        "STJ — Tese: configura abuso de direito a cobrança vexatória de dívida, ainda que o crédito seja legítimo.",
        "STJ — O exercício irregular de direito potestativo que cause dano desproporcional ao outro contratante configura abuso (art. 187 CC).",
    ],
    "205": [
        "STJ — Súmula 85: nas relações jurídicas de trato sucessivo, a prescrição de que trata o art. 205 corre da data em que surgiu cada parcela.",
        "STJ — Tese: o prazo prescricional de 10 anos (art. 205) aplica-se às pretensões sem prazo específico no CC ou em lei especial.",
    ],
    "206": [
        "STJ — Súmula 278: o prazo prescricional para o segurado reclamar indenização do seguro é de 1 ano (§1°, II, b).",
        "STJ — Tese: o prazo de 3 anos (§3°, V) aplica-se à reparação civil de ato ilícito extracontratual.",
        "STJ — Tese: o prazo de 5 anos (§5°, I) aplica-se à cobrança de dívidas líquidas constantes de instrumento público ou particular.",
    ],
    "421": [
        "STJ — Tese: a função social do contrato impede cláusulas abusivas que gerem desequilíbrio excessivo, mesmo entre partes iguais.",
        "STJ — A revisão judicial do contrato por onerosidade excessiva exige imprevisibilidade do fato que alterou a base negocial (art. 478 CC).",
    ],
    "422": [
        "STJ — Tese: a boa-fé objetiva impõe deveres anexos de lealdade, informação e proteção, mesmo fora da fase de execução contratual.",
        "STJ — Enunciado CJF 25: o art. 422 abrange a fase pré-contratual e pós-contratual (culpa post factum finitum).",
        "STJ — Teoria do venire contra factum proprium: é vedado comportamento contraditório que viola a confiança legítima da outra parte.",
    ],
    "927": [
        "STJ — Tese: a responsabilidade objetiva (parágrafo único, art. 927) aplica-se a atividades de risco intrínseco; o risco deve ser anormal em comparação com atividade comum.",
        "STF — RE 636.331: responsabilidade objetiva de transportadoras aéreas por danos ao consumidor é regida pelo CDC, não pela Convenção de Varsóvia.",
    ],
    "932": [
        "STJ — Tese: a responsabilidade dos pais por atos dos filhos menores (art. 932, I) é objetiva e independe de culpa in vigilando.",
        "STJ — Tese: empregador responde objetivamente por danos causados por empregado no exercício do trabalho ou em razão dele (art. 932, III).",
    ],
    "944": [
        "STJ — O juiz pode reduzir equitativamente a indenização quando houver desproporção entre a gravidade da culpa e o dano (parágrafo único).",
        "STJ — Tese: a compensatio lucri cum damno (desconto de benefícios previdenciários na indenização) é aplicável em responsabilidade civil.",
    ],
    "1228": [
        "STF — Súmula 619: a ocupação de imóvel por particular não configura posse com animus domini; é mera detenção se ausente o elemento intencional.",
        "STJ — Tese: a função social da propriedade (§1°) não elimina o direito de reivindicação do proprietário, mas pode mitigar efeitos da reintegração em situações consolidadas.",
    ],
    "1696": [
        "STJ — Tese: o dever de alimentos é recíproco entre pais e filhos; filhos maiores e emancipados perdem o direito a alimentos ao completar 24 anos e concluir curso superior, salvo necessidade comprovada.",
        "STJ — Súmula 358: o cancelamento de pensão alimentícia de filho que atingiu a maioridade está sujeito à decisão judicial, mediante contraditório.",
    ],
    "1829": [
        "STJ — Tese: cônjuge concorre com descendentes na herança; a fração depende do regime de bens — no regime de separação legal, o cônjuge não herda.",
        "STJ — Tese: o companheiro tem direito à herança nas mesmas condições do cônjuge (STF RE 646.721 e RE 878.694 — tese vinculante).",
    ],
    "1845": [
        "STJ — Tese: herdeiros necessários (descendentes, ascendentes e cônjuge) têm direito à legítima (50% da herança), que não pode ser afastada por testamento.",
        "STJ — O companheiro em união estável é equiparado ao cônjuge para fins de herança (STF — tese vinculante RE 878.694).",
    ],
}

# Observações práticas por artigo
OBS_PRATICAS_CC = {
    "186": {
        "acusacao": "Em ação de indenização, qualificar o ato ilícito com precisão (comissivo ou omissivo), descrever o nexo causal e o dano concreto; juntar laudo pericial ou prova documental do prejuízo.",
        "defesa": "Impugnar o nexo causal e o quantum debeatur; explorar culpa concorrente da vítima (art. 945 CC) para redução proporcional; arguir excludentes (caso fortuito, força maior, culpa exclusiva da vítima).",
        "pratica": "Dano moral in re ipsa: em casos de violação de dignidade, honra ou imagem, a prova do dano é presumida — basta demonstrar o ato e o nexo. Dano material exige comprovação efetiva do prejuízo patrimonial.",
    },
    "187": {
        "acusacao": "Demonstrar que o exercício do direito ultrapassou os limites impostos pela boa-fé, pelos bons costumes ou pela função social; mostrar conduta contraditória (venire) ou desequilíbrio desproporcional.",
        "defesa": "O exercício de direito potestativo (rescisão contratual, cobrança legítima) não é abuso per se; demonstrar que a conduta não gerou dano desproporcional nem violou expectativa legítima.",
        "pratica": "Art. 187 é base legal para teoria do venire contra factum proprium, supressio/surrectio e tu quoque — argumentos de abuso de direito amplamente usados no STJ.",
    },
    "421": {
        "acusacao": "Invocar função social para afastar cláusula contratual abusiva que gere desequilíbrio excessivo; juntar perícia econômica para demonstrar o impacto da cláusula.",
        "defesa": "A função social não transforma contratos privados em públicos; autonomia privada (§ único, acrescentado pela Lei 13.874/2019) deve ser respeitada entre partes paritárias e informadas.",
        "pratica": "Lei 13.874/2019 (Liberdade Econômica) incluiu §único no art. 421: nas relações paritárias, a intervenção judicial deve ser mínima. Distinguir contratos de adesão (CDC) de contratos civis paritários.",
    },
    "422": {
        "acusacao": "Demonstrar violação de dever anexo de informação (omissão relevante pré-contratual) ou de lealdade (descumprimento de ato próprio); boa-fé objetiva é parâmetro objetivo, não subjetivo.",
        "defesa": "O dever de informação tem limites: não abrange dados estratégicos ou sigilosos; a outra parte tem o dever de se informar (autorresponsabilidade). Distinguir boa-fé objetiva (conduta) de boa-fé subjetiva (crença).",
        "pratica": "Enunciado CJF 170: a boa-fé objetiva deve ser observada pelas partes na fase de conclusão do contrato. Enunciado 25: alcança fases pré e pós-contratuais.",
    },
    "927": {
        "acusacao": "Na responsabilidade objetiva, provar apenas o dano e o nexo causal — não é necessário demonstrar culpa. Juntar documentos que comprovem o exercício da atividade de risco.",
        "defesa": "O parágrafo único do art. 927 exige atividade de risco intrínseco; atividade comum com risco eventual não basta. Explorar excludentes: culpa exclusiva da vítima, caso fortuito externo, fato de terceiro.",
        "pratica": "Distinção prática: atividade de risco normal (regime subjetivo, art. 927 caput) vs. atividade de risco intrínseco (regime objetivo, §único). Exemplos objetivos: transporte, produtos defeituosos, mineração.",
    },
    "1228": {
        "acusacao": "Em ação reivindicatória, provar domínio (matrícula/registro) e esbulho; na usucapião, demonstrar posse com animus domini, mansa, pacífica e pelo prazo legal.",
        "defesa": "Impugnar o animus domini do possuidor; demonstrar que a posse é por mera tolerância do proprietário (detenção precária); arguir descumprimento da função social como fundamento de resistência.",
        "pratica": "Usucapião extrajudicial (art. 1.071 CPC) permite via cartorária quando não há litígio. Registro de imóveis: matrícula é o título de domínio mais robusto — verificar ônus e gravames antes de qualquer negócio.",
    },
    "1696": {
        "acusacao": "Demonstrar o binômio necessidade do alimentando e possibilidade do alimentante; juntar documentos de despesas (escola, saúde, moradia) e renda do devedor.",
        "defesa": "Alimentos são revisíveis; mudança de capacidade econômica (desemprego, doença) justifica revisão (art. 1.699 CC). Filhos maiores que não estudam perdem o direito.",
        "pratica": "Alimentos provisórios são concedidos em tutela de urgência; execução por desconto em folha é a mais eficiente. Prisão civil (art. 528 CPC) é cabível na execução de alimentos — prazo máximo 3 meses por período.",
    },
    "1829": {
        "acusacao": "Em inventário, verificar regime de bens do casamento/união para calcular meação do cônjuge/companheiro e quota hereditária; distinguir meação (direito real) de herança (direito sucessório).",
        "defesa": "No regime de separação legal de bens (art. 1.641 CC), não há comunicação de bens; cônjuge pode não ter direito à herança dependendo da interpretação do art. 1.829, I.",
        "pratica": "Inventário extrajudicial (art. 610 CPC) é cabível quando todos os herdeiros são maiores e capazes, sem testamento e sem litígio. Arrolamento sumário: herança abaixo de 1.000 salários mínimos.",
    },
    "1845": {
        "acusacao": "Herdeiro necessário preterido pode propor ação de petição de herança; a legítima é calculada sobre o total do patrimônio do falecido na data da abertura da sucessão.",
        "defesa": "Testamento não pode reduzir a legítima (50% da herança líquida), mas o testador pode escolher qual bem cada herdeiro necessário recebe (art. 1.848 CC). Impugnar cálculo da legítima se houver dívidas a descontar.",
        "pratica": "Doação feita em vida que exceda a legítima é colacionável (art. 2.002 CC); herdeiro necessário pode exigir redução das disposições testamentárias que ultrapassem a parte disponível.",
    },
}


def _jurisprudencia_cc(num_str: str) -> List[str]:
    return JURIS_CC.get(num_str, [])


def _obs_praticas_cc(num_str: str) -> dict:
    return OBS_PRATICAS_CC.get(num_str, {})


def _correlatos_outros_cc(num_base, num_str: str) -> List[str]:
    try:
        num_base = int(num_base)
    except (ValueError, TypeError):
        num_base = -1
    correlatos = []
    try:
        num_base = int(num_base)
    except (ValueError, TypeError):
        return [
            "[[L13105 Art. 1]] — normas processuais civis (CPC)",
            "[[CF88 Art. 5]] — direitos fundamentais (CF/88)",
        ]
    if 186 <= num_base <= 188:
        correlatos += [
            "[[L10406 Art. 927]] — responsabilidade civil geral",
            "[[L13105 Art. 373]] — ônus da prova (CPC)",
        ]
    elif num_base == 421 or num_base == 422:
        correlatos += [
            "[[L10406 Art. 478]] — resolução por onerosidade excessiva",
            "[[L10406 Art. 113]] — interpretação dos negócios jurídicos",
        ]
    elif num_base == 927:
        correlatos += [
            "[[L10406 Art. 186]] — ato ilícito",
            "[[L10406 Art. 944]] — extensão da indenização",
        ]
    elif 1829 <= num_base <= 1850:
        correlatos += [
            "[[L10406 Art. 1784]] — abertura da sucessão",
            "[[L13105 Art. 610]] — inventário extrajudicial (CPC)",
        ]
    elif 1696 <= num_base <= 1710:
        correlatos += [
            "[[L13105 Art. 528]] — execução de alimentos (CPC)",
        ]
    # Correlatos estruturais gerais
    correlatos += [
        "[[L13105 Art. 1]] — normas processuais civis (CPC)",
        "[[CF88 Art. 5]] — direitos fundamentais (CF/88)",
    ]
    return list(dict.fromkeys(correlatos))  # deduplicar mantendo ordem


class MarkdownGeneratorCC:
    """Gera notas Markdown estruturadas para artigos do Código Civil."""

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
        categoria = artigo.get("categoria", lei_cfg.get("categoria", "CODIGO_CIVIL"))
        tema = lei_cfg.get("tema", "direito-civil")

        tags = TAGS_PADRAO.copy()
        for t in [categoria.lower(), f"art-{num}", tema, sigla.lower()]:
            if t not in tags:
                tags.append(t)

        livro_info = self._detectar_livro_cc(num) if (sigla == "L10406" and isinstance(num, int)) else None

        frontmatter = {
            "artigo": num_str,
            "lei": f"{lei_numero} — {nome_lei}",
            "sigla": sigla,
            "categoria": categoria,
            "status": "vigente",
            "direito_civil": True,
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

        # Jurisprudência
        juris = _jurisprudencia_cc(num_str)
        if juris:
            juris_str = "\n".join(f"- {j}" for j in juris)
            juris_str += "\n\n[Conferir atualização: STJ «Jurisprudência em Teses»; Informativos STF/STJ]"
        else:
            juris_str = "[Conferir atualização: STJ «Jurisprudência em Teses»; Informativos STF/STJ]"

        # Observações práticas
        obs = _obs_praticas_cc(num_str)
        if obs:
            obs_str = (
                f"- **Acusação/Autor:** {obs.get('acusacao', '')}\n"
                f"- **Defesa/Réu:** {obs.get('defesa', '')}\n"
                f"- **Prática:** {obs.get('pratica', '')}"
            )
        else:
            obs_str = "[Aplicação na prática forense — preencher com experiência do caso concreto]"

        # Correlatos
        correlatos = _correlatos_outros_cc(num, num_str)
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

### Função no Sistema

[Como este artigo se relaciona com o sistema de Direito Civil — que direito ele
tutela? Qual obrigação, responsabilidade ou direito real ele estrutura?]

### Co-dependência normativa

[Qual outro dispositivo este artigo depende? CF/88? CPC? Leis especiais?]

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
    def _detectar_livro_cc(num: int) -> Dict:
        """Detecta qual livro do CC o artigo pertence."""
        if 1 <= num <= 232:
            return {"livro": "I", "titulo": "Das Pessoas"}
        elif 233 <= num <= 709:
            return {"livro": "II", "titulo": "Do Direito das Obrigações"}
        elif 710 <= num <= 1227:
            return {"livro": "III", "titulo": "Do Direito das Coisas"}
        elif 1228 <= num <= 1626:
            return {"livro": "IV", "titulo": "Do Direito de Família"}
        elif 1627 <= num <= 2046:
            return {"livro": "V", "titulo": "Do Direito das Sucessões"}
        return {}


if __name__ == "__main__":
    gen = MarkdownGeneratorCC(Path("test_output_cc"))
    print("Gerador Código Civil pronto")

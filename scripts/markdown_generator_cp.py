#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera notas Markdown atômicas para artigos do Código Penal."""
import re
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict
from config_codigo_penal import TAGS_PADRAO


# Jurisprudência curada: súmulas e teses consolidadas STJ/STF por artigo DEL2848
JURIS_CP = {
    "33": [
        "STJ — Súmula 440: fixada a pena-base no mínimo legal, é vedado o regime mais gravoso com fundamento apenas na gravidade abstrata do delito.",
        "STF — Súmula 718: a opinião do julgador sobre a gravidade em abstrato do crime não constitui motivação idônea para regime mais severo do que o cabível.",
    ],
    "59": [
        "STJ — Súmula 444: é vedada a utilização de inquéritos policiais e ações penais em curso para agravar a pena-base.",
        "STJ — Tese firmada: cada circunstância judicial (art. 59) deve ser fundamentada concretamente; motivação genérica é nula.",
    ],
    "121": [
        "STJ — Tese: feminicídio (§2°-VI) e motivo torpe (§2°-I) são qualificadoras compatíveis e podem coexistir no mesmo fato.",
        "STJ — Tese: o reconhecimento do dolo eventual no homicídio de trânsito não afasta a competência do Tribunal do Júri.",
    ],
    "121-A": [
        "STJ — Tese: feminicídio é qualificadora de natureza objetiva (razão da condição do sexo feminino); compatível com qualificadoras subjetivas como motivo torpe.",
        "STJ — Súmula 600: para configurar violência doméstica e familiar, não se exige coabitação entre vítima e agressor.",
    ],
    "121-B": [
        "Art. 121-B inserido pela Lei 14.994/2024 — jurisprudência ainda em formação; consultar STJ Informativos mais recentes.",
        "STJ — Por extensão: teses do feminicídio (art. 121-A) sobre natureza objetiva da qualificadora e dispensa de coabitação aplicam-se por analogia.",
    ],
    "129": [
        "STJ — Súmula 536: suspensão condicional do processo e transação penal não se aplicam a delitos sujeitos ao rito da Lei Maria da Penha.",
        "STJ — Súmula 600: para violência doméstica, não se exige coabitação entre vítima e agressor no mesmo domicílio.",
    ],
    "138": [
        "STF — Súmula 714: é concorrente a legitimidade do ofendido (queixa) e do MP (representação) para crime contra a honra de servidor público em razão do cargo.",
        "STJ — Tese: crítica de interesse público não configura calúnia; exige-se dolo específico de ofender a honra.",
    ],
    "155": [
        "STJ — Súmula 511: é possível reconhecer o privilégio (§2°) no furto qualificado, se presentes primariedade, pequeno valor e qualificadora de ordem objetiva.",
        "STJ — Súmula 442: é inadmissível aplicar no furto qualificado a causa de aumento do §1° (noturno) pelo simples fato de o crime ser qualificado.",
    ],
    "157": [
        "STJ — Súmula 582: consuma-se o roubo com a inversão da posse mediante violência ou ameaça, ainda que breve e mesmo que a coisa seja recuperada em seguida.",
        "STJ — Súmula 443: o aumento na terceira fase para roubo circunstanciado exige fundamentação explícita; não basta indicar o número de majorantes.",
    ],
    "171": [
        "STJ — Súmula 554: o pagamento do cheque sem fundos após o recebimento da denúncia não obsta ao prosseguimento da ação penal.",
        "STJ — Tese: estelionato previdenciário é crime permanente enquanto perdurar o recebimento do benefício indevido; prescrição não flui antes da cessação.",
    ],
    "213": [
        "STJ — Súmula 608: no estupro praticado mediante violência real, a ação penal é pública incondicionada.",
        "STJ — Tese: mais de um ato libidinoso contra a mesma vítima no mesmo contexto fático configura crime único de estupro, não concurso formal.",
    ],
    "217-A": [
        "STJ — Súmula 593: o estupro de vulnerável configura-se com ato libidinoso com menor de 14 anos, sendo irrelevante o consentimento da vítima.",
        "STJ — Tese: a presunção de vulnerabilidade do art. 217-A é absoluta; não admite relativização por experiência sexual anterior da vítima.",
    ],
    "288": [
        "STJ — Tese: o crime de associação criminosa é autônomo e punível ainda que os membros não sejam condenados pelos crimes praticados pela associação.",
        "STJ — Tese: exige-se estabilidade e permanência do vínculo; encontro eventual de três ou mais pessoas não configura o tipo.",
    ],
    "312": [
        "STJ — Súmula 599: o princípio da insignificância é inaplicável aos crimes contra a administração pública.",
        "STJ — Tese: peculato-desvio (§1°) consuma-se quando o funcionário dá ao bem destinação diversa da legal; não exige locupletamento pessoal.",
    ],
    "317": [
        "STJ — Súmula 599: é inaplicável o princípio da insignificância à corrupção passiva (crime contra a administração pública).",
        "STF — AP 470 (Mensalão): a teoria do domínio do fato permite responsabilizar por corrupção passiva quem controla a conduta delitiva sem executá-la diretamente.",
    ],
    "333": [
        "STJ — Tese: na corrupção ativa, o crime consuma-se no momento da oferta ou promessa, independentemente da aceitação pelo funcionário.",
        "STJ — Súmula 599: inaplicabilidade do princípio da insignificância aos crimes contra a administração pública.",
    ],
}


# Observações práticas curadas: perspectiva MP, Defesa e Tribunais por artigo DEL2848
OBS_PRATICAS_CP = {
    "121": (
        "- **MP/Acusação:** descrever conduta com especificação do dolo (direto ou eventual) e das qualificadoras incidentes; "
        "nos crimes qualificados, cada qualificadora do §2° é quesitada separadamente no Júri.\n"
        "- **Defesa:** teses frequentes — desclassificação para homicídio culposo (§3°), privilégio do §1° "
        "(relevante valor moral, violenta emoção logo após injusta provocação), legítima defesa (art. 25 CP).\n"
        "- **Tribunais:** competência constitucional do Tribunal do Júri (art. 5°, XXXVIII, CF); "
        "in dubio pro reo na pronúncia; qualificadoras de natureza subjetiva são decididas pelos jurados."
    ),
    "121-A": (
        "- **MP/Acusação:** demonstrar as razões da condição do sexo feminino — violência doméstica/familiar (inciso I) "
        "ou menosprezo/discriminação à mulher (inciso II); Súmula 600 STJ dispensa coabitação.\n"
        "- **Defesa:** verificar se as razões do §1° estão efetivamente presentes e se não há mera violência interpessoal "
        "sem motivação de gênero; possível desclassificação para homicídio simples (art. 121, caput).\n"
        "- **Prática:** crime hediondo (Lei 8.072/90); competência do Tribunal do Júri; "
        "Lei Maria da Penha (11.340/06) pode ser aplicada cumulativamente para medidas protetivas."
    ),
    "121-B": (
        "- **MP/Acusação:** demonstrar feminicídio (art. 121-A) + uma das causas qualificadoras do art. 121-B "
        "(vítima menor de 14 ou maior de 60 anos, gestante, deficiente, presença de filhos etc.).\n"
        "- **Defesa:** impugnar a presença das qualificadoras com prova documental (certidão de nascimento, laudo médico); "
        "distinguir do feminicídio simples (art. 121-A) caso ausente a causa qualificadora.\n"
        "- **Prática:** art. 121-B inserido pela Lei 14.994/2024 — verificar data do fato para aplicação da lei mais grave; "
        "pena mínima de 20 anos impede progressão de regime no menor prazo."
    ),
    "129": (
        "- **MP/Acusação:** nos casos de violência doméstica, ação penal é pública incondicionada — Lei 11.340/06 "
        "dispensa representação da vítima; classificar corretamente entre leve, grave (§1°) e gravíssima (§2°).\n"
        "- **Defesa:** legítima defesa é tese frequente; verificar laudo de lesões corporais — ausência de lesões "
        "pode impor desclassificação para vias de fato (LCP art. 21).\n"
        "- **Prática:** lesão leve em contexto de violência doméstica é de competência do Juizado de Violência Doméstica "
        "(não do JECRIM); Súmula 536 STJ veda suspensão condicional do processo nesses casos."
    ),
    "155": (
        "- **MP/Acusação:** quantificar o prejuízo e descrever o modus operandi; nas qualificadoras materiais "
        "(rompimento de obstáculo, escalada), apresentar laudo pericial — ausência pode nulificar a qualificadora.\n"
        "- **Defesa:** princípio da insignificância (STJ analisa valor do bem + condições da vítima + primariedade); "
        "privilégio do §2° (bem de pequeno valor + primariedade); arrependimento posterior (art. 16 CP) reduz a pena.\n"
        "- **Prática:** furto de energia elétrica é equiparado a coisa móvel (§3°); "
        "furto mediante fraude distingue-se do estelionato pelo meio de execução (subtração vs. entrega voluntária)."
    ),
    "157": (
        "- **MP/Acusação:** descrever a violência ou grave ameaça concretamente; no roubo majorado, "
        "indicar qual inciso do §2° aplica-se e fundamentar cada majorante na terceira fase da pena (Súmula 443 STJ).\n"
        "- **Defesa:** verificar se houve efetiva violência/ameaça grave; simulacro de arma de fogo não majora a pena "
        "(§2°-I exige arma real ou funcional — laudo pericial); tentativa possível (Súmula 582 STJ para consumação).\n"
        "- **Prática:** latrocínio (§3°) ocorre quando a morte resulta da violência, ainda que sem dolo de matar; "
        "competência do Tribunal do Júri apenas no latrocínio — roubo simples é da Vara Criminal comum."
    ),
    "171": (
        "- **MP/Acusação:** demonstrar os três elementos cumulativos — artifício/ardil/meio fraudulento, "
        "indução em erro da vítima e obtenção de vantagem ilícita em prejuízo alheio; dolo deve preexistir.\n"
        "- **Defesa:** ausência do artifício fraudulento (mero inadimplemento civil não é estelionato); "
        "pagamento do cheque antes da denúncia extingue a punibilidade (Súmula 554 STJ) nos crimes de cheque sem fundos.\n"
        "- **Prática:** estelionato contra idoso tem pena aumentada de 1/3 (§4°); "
        "estelionato por meio eletrônico (§2°-A, incluído pela Lei 14.155/21) tem pena aumentada de 1/3 a 2/3."
    ),
    "213": (
        "- **MP/Acusação:** com violência real, a ação é pública incondicionada (Súmula 608 STJ); "
        "descrever os atos executórios e a ausência de consentimento; crime hediondo (regime inicial fechado).\n"
        "- **Defesa:** verificar autoria e prova testemunhal; retratação da representação só cabe antes da denúncia; "
        "consentimento da vítima maior de 14 anos e capaz pode afastar o tipo.\n"
        "- **Prática:** concurso material quando há mais de uma vítima; "
        "estupro de vulnerável (art. 217-A) aplica-se quando a vítima é menor de 14 anos — tipos penais distintos."
    ),
    "217-A": (
        "- **MP/Acusação:** presunção absoluta de vulnerabilidade (Súmula 593 STJ) — dispensada prova de violência; "
        "basta demonstrar a prática de ato libidinoso e que a vítima era menor de 14 anos.\n"
        "- **Defesa:** impugnar autoria; distinção entre conjunção carnal e ato libidinoso diverso "
        "(penas diferenciadas antes da Lei 12.015/09); verificar data do fato.\n"
        "- **Prática:** crime hediondo; ação penal pública incondicionada; "
        "vulnerabilidade inclui também enfermidade ou doença mental que impeça discernimento (§1°)."
    ),
    "312": (
        "- **MP/Acusação:** demonstrar o vínculo funcional (funcionário público para fins penais — art. 327 CP) "
        "e a relação de posse/administração com o bem; peculato-desvio dispensa prova de locupletamento pessoal.\n"
        "- **Defesa:** peculato culposo (§2°) admite extinção da punibilidade por reparação integral do dano "
        "antes da sentença irrecorrível; verificar se o agente tem a qualidade de funcionário público.\n"
        "- **Prática:** Súmula 599 STJ veda insignificância; colaboração premiada e acordo de não-persecução "
        "penal (ANPP) são instrumentos frequentes em investigações de improbidade-penal."
    ),
    "317": (
        "- **MP/Acusação:** demonstrar nexo entre a vantagem indevida e o ato de ofício; "
        "crime formal — consuma-se com a solicitação ou recebimento, dispensando a prática do ato de ofício.\n"
        "- **Defesa:** ausência de nexo entre a vantagem e ato de ofício específico; "
        "distinção com advocacia administrativa (art. 321 CP) e tráfico de influência (art. 332 CP).\n"
        "- **Prática:** AP 470 STF consolidou teoria do domínio do fato para chefes hierárquicos; "
        "delação premiada e ANPP são instrumentos frequentes; Súmula 599 STJ veda insignificância."
    ),
    "333": (
        "- **MP/Acusação:** crime formal — oferta ou promessa consuma o tipo, independente da aceitação; "
        "descrever o ato de ofício visado e o vínculo com a vantagem oferecida.\n"
        "- **Defesa:** ausência do elemento normativo 'ato de ofício' específico; "
        "distinguir de tráfico de influência (art. 332) quando não há servidor determinado.\n"
        "- **Prática:** corrupção ativa e passiva são crimes autônomos — processamento simultâneo de "
        "corruptor e corrompido não é bis in idem; Súmula 599 STJ veda insignificância."
    ),
    "288": (
        "- **MP/Acusação:** demonstrar estabilidade e permanência do vínculo associativo — não basta reunião "
        "eventual; indicar os membros identificados (mínimo 3) e a finalidade de praticar crimes.\n"
        "- **Defesa:** distinguir de concurso eventual de pessoas (art. 29 CP); "
        "ausência de estabilidade e permanência afasta o tipo; organização criminosa (Lei 12.850/13) é figura distinta.\n"
        "- **Prática:** autonomia do crime — punível ainda que os crimes-fim não sejam consumados; "
        "pena aumentada de metade se a associação é armada (§1°)."
    ),
}


class MarkdownGeneratorCP:
    """Gera notas Markdown estruturadas para artigos do Código Penal."""

    def __init__(self, output_base: Path):
        self.output_base = Path(output_base)

    def gerar_nota_artigo(self, artigo: Dict, lei_cfg: Dict, sigla: str) -> str:
        num = artigo["numero"]
        nome_lei = lei_cfg["nome"]
        lei_numero = lei_cfg["lei_numero"]
        categoria = artigo.get("categoria", lei_cfg.get("categoria", "DIREITO_PENAL"))
        tema = lei_cfg.get("tema", "direito-penal")

        tags = TAGS_PADRAO.copy()
        for t in [categoria.lower(), f"art-{num}", tema, sigla.lower()]:
            if t not in tags:
                tags.append(t)

        # Detectar parte do CP (arts. 1-84: Parte Geral, 85-302: Parte Especial)
        num_base = int(str(num).split("-")[0]) if str(num).split("-")[0].isdigit() else 0
        parte_info = self._detectar_parte_cp(num_base) if sigla == "DEL2848" else None

        frontmatter = {
            "artigo": str(num),
            "lei": f"{lei_numero} — {nome_lei}",
            "sigla": sigla,
            "categoria": categoria,
            "status": "vigente",
            "direito_penal": True,
            "relacionados": [],
            "tags": tags,
            "created": datetime.now().strftime("%Y-%m-%d"),
        }

        if parte_info:
            frontmatter.update(parte_info)

        fm_str = yaml.dump(frontmatter, allow_unicode=True,
                           default_flow_style=False, sort_keys=False)

        redacao = artigo.get("redacao", "[Conferir redação no Planalto]")
        titulo_artigo = artigo.get("titulo", f"Art. {num}")

        # Exibe até 600 chars na nota; usa texto completo (3000) para extrações
        redacao_display = (redacao[:600] + "...") if len(redacao) > 600 else redacao

        penas = self._extrair_pena(redacao)
        tem_aumento = bool(re.search(
            r'aumenta(?:-se)?|pena.{0,25}aumentada|dobra(?:-se)?', redacao, re.IGNORECASE))
        tem_reducao = bool(re.search(
            r'reduz(?:-se)?|pena.{0,25}reduzida|redução de pena|pode ser reduzida', redacao, re.IGNORECASE))

        if not penas:
            pena_bloco = "[Pena não localizada — artigo não comina pena diretamente.]"
        elif len(penas) == 1:
            mods = []
            if tem_aumento:
                mods.append("causas de aumento")
            if tem_reducao:
                mods.append("causas de diminuição")
            pena_bloco = f"**Pena:** {penas[0]}"
            if mods:
                pena_bloco += f"\n\n*Há {' e '.join(mods)} — conferir §§ na redação acima.*"
            else:
                pena_bloco += "\n\n[Verificar §§ para qualificadoras ou causas de modificação.]"
        else:
            linhas = [f"- **Caput:** {penas[0]}"]
            for p in penas[1:]:
                linhas.append(f"- **Qualificadora/modalidade:** {p}")
            pena_bloco = "\n".join(linhas)
            mods = []
            if tem_aumento:
                mods.append("causas de aumento")
            if tem_reducao:
                mods.append("causas de diminuição")
            if mods:
                pena_bloco += f"\n\n*Há {' e '.join(mods)} — conferir §§ na redação acima.*"

        # Artigos correlatos — outros crimes
        correlatos_linhas = self._correlatos_outros(num_base, str(num), redacao, sigla)
        correlatos_str = "\n".join(correlatos_linhas) if correlatos_linhas else \
            "[Dispositivos do CP que se relacionam — crimes conexos, concurso de crimes,\ncausas de exclusão de ilicitude ou culpabilidade]"

        # Jurisprudência curada (DEL2848) ou placeholder
        juris = self._jurisprudencia(str(num), sigla)
        if juris:
            juris_str = "\n".join(f"- {j}" for j in juris) + \
                "\n\n[Conferir atualização: STJ «Jurisprudência em Teses»; Informativos STF/STJ]"
        else:
            juris_str = "[Pesquisar: STJ «Jurisprudência em Teses» + tema do artigo; Informativos STF/STJ]"

        # Observações práticas curadas ou placeholder
        obs = self._obs_praticas(str(num), sigla)
        obs_str = obs if obs else \
            "[Aplicação na prática forense: como MP, defesa e tribunais utilizam este artigo\nem denúncias, defesas, sentenças?]"

        # prev/next pela ordem real da lei (calculado no pipeline com lista completa)
        if artigo.get("prev_num") is not None:
            art_anterior = artigo["prev_num"]
        else:
            art_anterior = max(1, num_base - 1)

        if artigo.get("next_num") is not None:
            art_seguinte = artigo["next_num"]
        else:
            art_seguinte = num_base + 1

        corpo = f"""# {sigla} Art. {num} — {titulo_artigo}

**Lei:** {lei_numero} — {nome_lei}
**Categoria:** {categoria}
**Status:** VIGENTE

---

## REDACAO LEGAL

> {redacao_display}

---

## ANALISE TECNICA

### Bem Jurídico Tutelado

[Qual bem jurídico penal este artigo protege?
Exemplo: vida, liberdade, honra, patrimônio, segurança pública, etc.]

### Tipo Penal

[Síntese do tipo penal: sujeitos do crime (ativo/passivo), conduta, resultado, nexo causal]

### Dolo/Culpa

[Qual é a forma de imputação? Dolo direto? Dolo eventual? Culpa?
Há tipificação culposa em outro artigo?]

### Tentativa e Consumação

[Qual é o momento de consumação?
A tentativa é punível conforme art. 14 do CP?]

### Penas Cominadas

{pena_bloco}

---

## ARTIGOS CORRELATOS

### Mesma Lei
- [[{sigla} Art. {art_anterior}]] — artigo anterior
- [[{sigla} Art. {art_seguinte}]] — artigo seguinte

### Outros crimes
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
    def _extrair_pena(redacao: str) -> list:
        """Extrai todas as cláusulas de pena únicas da redação legal."""
        pat = re.compile(r'Pena\s*[-–—:]\s*(.+?\.)', re.IGNORECASE | re.DOTALL)
        vistas: set = set()
        penas = []
        for m in pat.finditer(redacao):
            p = m.group(1).strip()
            if p not in vistas:
                vistas.add(p)
                penas.append(p)
        return penas

    @staticmethod
    def _correlatos_outros(num_base: int, num_str: str, redacao: str, sigla: str) -> list:
        """Extrai cross-refs do texto + adiciona correlatos estruturais (tentativa, excludentes, concurso)."""
        linhas = []
        incluidos: set = set()

        # Cross-references explícitas na redação (lowercase "art. N" = refs internas à lei)
        if sigla == "DEL2848":
            pat_ref = re.compile(r'\bart\.\s*(\d+(?:-[A-Z])?)\b')
            for m in pat_ref.finditer(redacao):
                ref = m.group(1)
                num_ref = int(ref.split("-")[0]) if ref.split("-")[0].isdigit() else 0
                if 1 <= num_ref <= 361 and ref != num_str and ref not in incluidos:
                    incluidos.add(ref)
                    linhas.append(f"- [[DEL2848 Art. {ref}]] — mencionado na redação")
            linhas = linhas[:6]  # limita ruído

        # Correlatos estruturais para crimes (Parte Especial ou leis penais extravagantes)
        if num_base >= 85 or sigla != "DEL2848":
            estruturais = [
                ("14", "tentativa (art. 14 CP)"),
                ("23", "excludentes de ilicitude (arts. 23-25 CP)"),
                ("29", "concurso de pessoas (art. 29 CP)"),
            ]
            for art, desc in estruturais:
                if art not in incluidos:
                    linhas.append(f"- [[DEL2848 Art. {art}]] — {desc}")

        return linhas

    @staticmethod
    def _jurisprudencia(num_str: str, sigla: str) -> list:
        """Retorna até 2 precedentes curados (súmulas/teses STJ·STF) para o artigo."""
        if sigla != "DEL2848":
            return []
        return JURIS_CP.get(num_str, [])

    @staticmethod
    def _obs_praticas(num_str: str, sigla: str) -> str:
        """Retorna observações práticas curadas (MP, Defesa, Tribunais) para o artigo."""
        if sigla != "DEL2848":
            return ""
        return OBS_PRATICAS_CP.get(num_str, "")

    @staticmethod
    def _detectar_parte_cp(num: int) -> Dict:
        """Detecta qual parte do CP o artigo pertence."""
        if 1 <= num <= 84:
            return {"parte": "Geral", "titulo": "Disposições Gerais"}
        elif 85 <= num <= 302:
            return {"parte": "Especial", "titulo": "Dos Crimes"}
        return {}


if __name__ == "__main__":
    gen = MarkdownGeneratorCP(Path("test_output_cp"))
    print("Gerador Código Penal pronto")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera notas Markdown atômicas para artigos de leis de Direito Digital."""
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from config_direito_digital import TAGS_PADRAO


# Jurisprudência curada: teses STJ/STF por artigo
JURIS_DD = {
    "7": [  # Marco Civil da Internet — L12965 art. 7° (direitos do usuário)
        "STJ — Tese: dados pessoais do usuário de internet são tutelados pelo Marco Civil (art. 7°) e pela LGPD; o tratamento sem consentimento livre e específico configura violação.",
        "STJ — Tese: provedores de aplicação não respondem objetivamente pelo conteúdo gerado por terceiros; a responsabilidade surge após notificação judicial e descumprimento da ordem de remoção (art. 19 MCI).",
    ],
    "19": [  # Marco Civil — responsabilidade do provedor
        "STJ — Tese: a responsabilidade do provedor de aplicação (art. 19 MCI) exige ordem judicial; notificação extrajudicial não gera responsabilidade por omissão.",
        "STF — ADPF 403 e RE 1.037.396 (pendentes): questionamento da constitucionalidade do art. 19 por dificultar remoção de conteúdo ilícito — aguardar desfecho.",
        "STJ — Exceção ao art. 19: conteúdo de nudez não consensual (art. 21 MCI) gera responsabilidade após notificação extrajudicial — não exige ordem judicial.",
    ],
    "21": [  # Nudez não consensual — MCI art. 21
        "STJ — Tese: a vítima de revenge porn (art. 21 MCI) tem direito à remoção do conteúdo mediante notificação ao provedor; a responsabilidade nasce após o descumprimento da notificação.",
        "STJ — Art. 218-C CP (Lei 13.718/2018): tipifica a divulgação não consentida de cenas de sexo, nudez ou pornografia — integrar com o art. 21 MCI na estratégia de proteção da vítima.",
    ],
    "6": [  # LGPD — L13709 art. 6° (princípios do tratamento de dados)
        "ANPD — Os princípios do art. 6° da LGPD (finalidade, adequação, necessidade, transparência) devem ser observados em todo o ciclo de vida do dado pessoal.",
        "STJ — Tese: vazamento de dados pessoais por falha de segurança do controlador gera dano moral in re ipsa — o controlador responde objetivamente (art. 44 LGPD).",
    ],
    "7_lgpd": [  # LGPD — art. 7° (bases legais)
        "ANPD — As 10 bases legais do art. 7° da LGPD são taxativas; o tratamento sem base legal é ilícito. Consentimento (inciso I) deve ser livre, específico, informado e inequívoco.",
        "STJ — Tese: o legítimo interesse (art. 7°, IX) não pode ser invocado para dados sensíveis (art. 11); para esses, as bases são mais restritas.",
    ],
    "44": [  # LGPD — responsabilidade do controlador
        "STJ — Tese: a responsabilidade por tratamento inadequado de dados pessoais (art. 44 LGPD) é subjetiva para controlador e operador; o ônus da prova de ausência de culpa é do fornecedor (inversão pelo CDC).",
        "ANPD — A sanção máxima da LGPD é de 2% do faturamento no Brasil, limitada a R$ 50 milhões por infração (art. 52); as sanções são gradativas conforme a gravidade.",
    ],
}

# Observações práticas por artigo
OBS_PRATICAS_DD = {
    "19": {
        "autor": "Para remoção de conteúdo ilícito: notificar o provedor extrajudicialmente (art. 21 para nudez); para demais conteúdos, requerer ordem judicial (art. 19) com prazo de cumprimento; provedores têm 48h para remoção de conteúdo de nudez (art. 21).",
        "defesa": "Provedor de aplicação: ao receber notificação judicial, cumprir no prazo determinado; documentar a remoção; manter logs pelo prazo legal (6 meses para registros de acesso, 1 ano para dados de conexão — art. 15 MCI).",
        "pratica": "Jurisdição: o MCI permite que usuários brasileiros processem plataformas estrangeiras no Brasil quando o serviço é oferecido ao público brasileiro (art. 11). O direito ao esquecimento foi afastado pelo STJ (REsp 1.660.168) — distinguir de remoção de conteúdo ilícito.",
    },
    "6_lgpd": {
        "autor": "Em ações por violação à LGPD, demonstrar: (1) qual base legal foi violada; (2) qual dado foi tratado; (3) qual dano decorreu. Dano moral por vazamento: in re ipsa quando há exposição de dados sensíveis (saúde, biometria, etc.).",
        "defesa": "O controlador pode exonerar-se demonstrando que (art. 43): (1) não realizou o tratamento; (2) inexiste violação à LGPD; (3) dano decorre de culpa exclusiva do titular ou de terceiro.",
        "pratica": "Notificação de incidente de segurança (art. 48 LGPD): obrigatória à ANPD e ao titular quando o incidente pode acarretar risco ou dano relevante; prazo de 72h da ciência pelo controlador.",
    },
}


def _jurisprudencia_dd(num_str: str, sigla: str) -> List[str]:
    chave_sigla = f"{num_str}_{sigla.lower()}"
    if chave_sigla in JURIS_DD:
        return JURIS_DD[chave_sigla]
    return JURIS_DD.get(num_str, [])


def _obs_praticas_dd(num_str: str, sigla: str) -> dict:
    chave_sigla = f"{num_str}_{sigla.lower()}"
    if chave_sigla in OBS_PRATICAS_DD:
        return OBS_PRATICAS_DD[chave_sigla]
    return OBS_PRATICAS_DD.get(num_str, {})


def _correlatos_outros_dd(num_base, sigla: str) -> List[str]:
    correlatos = [
        "[[CF88 Art. 5]] — privacidade e liberdade de expressão (X, XIV, XXXIV)",
        "[[L10406 Art. 186]] — responsabilidade civil por dano digital (CC)",
    ]
    if "12965" in sigla:  # Marco Civil
        correlatos += ["[[L13709 Art. 6]] — princípios da LGPD (complementar ao MCI)"]
    elif "13709" in sigla:  # LGPD
        correlatos += ["[[L12965 Art. 7]] — direitos do usuário (Marco Civil)"]
    correlatos += ["[[DEL2848 Art. 218-C]] — divulgação não consentida (CP)"]
    return list(dict.fromkeys(correlatos))


class MarkdownGeneratorDD:
    """Gera notas Markdown estruturadas para artigos de leis de Direito Digital."""

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
        tema = lei_cfg.get("tema", "direito-digital")

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
            "direito_digital": True,
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

        juris = _jurisprudencia_dd(num_str, sigla)
        if juris:
            juris_str = "\n".join(f"- {j}" for j in juris)
            juris_str += "\n\n[Conferir atualização: STJ «Jurisprudência em Teses»; ANPD — Guias e Resoluções]"
        else:
            juris_str = "[Conferir atualização: STJ «Jurisprudência em Teses»; ANPD — Guias e Resoluções]"

        obs = _obs_praticas_dd(num_str, sigla)
        if obs:
            obs_str = (
                f"- **Autor/Vítima:** {obs.get('autor', '')}\n"
                f"- **Réu/Provedor:** {obs.get('defesa', '')}\n"
                f"- **Prática:** {obs.get('pratica', '')}"
            )
        else:
            obs_str = "[Aplicação na prática forense digital — preencher com experiência do caso concreto]"

        correlatos = _correlatos_outros_dd(num, sigla)
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

[Esta regra depende de qual outro instrumento — CF Art. 5° (privacidade/liberdade), CC, CP, outra lei de Direito Digital?]

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
    gen = MarkdownGeneratorDD(Path("test_output_dd"))
    print("Gerador Direito Digital pronto")

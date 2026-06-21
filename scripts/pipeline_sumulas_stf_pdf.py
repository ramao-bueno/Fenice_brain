#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pipeline Súmulas STF — PDF → 736 notas Obsidian
Gera: 00_APEX/SUMULAS STF/Sumulas/Sumula-STF-{numero:04d}.md
"""
import sys
import unicodedata
import yaml
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from extrator_pdf_sumulas_stf import extrair_sumulas_pdf

# ── Classificador de temas ────────────────────────────────────────────────────

TEMAS = [
    ("tributario",       ["tribut","imposto","icms","iss","ipi","cofins","pis","csll","fiscal","receita federal"]),
    ("previdenciario",   ["previdenc","inss","segurado","aposentadori","beneficio","salario-maternidade","acidente do trabalho"]),
    ("trabalhista",      ["trabalhist","empregado","empregador","clt","tst","salario","fgts","hora extra","sindicato"]),
    ("penal",            ["crime","delito","pena ","penal","criminal","reu ","dolo","furto","roubo","estelionato","peculato","homicidio","estupro","prescricao criminal","habeas corpus"]),
    ("processual-penal", ["prisao","flagrante","inquerito","acao penal","competencia criminal","juri","liberdade provisoria"]),
    ("administrativo",   ["administrac","licitacao","contrato administrativo","servidor publico","concurso publico","desapropriac","autarquia"]),
    ("consumidor",       ["consumidor","cdc","fornecedor","plano de saude","banco","cartao de credito","negativacao"]),
    ("civil",            ["civil","contrato","obrigac","responsabilidade civil","indenizac","dano moral","posse","propriedade","heranca","locacao","alimentos"]),
    ("processual-civil", ["acao civil","processo civil","cpc","recurso especial","embargos","execucao","penhora","honorarios","coisa julgada"]),
    ("constitucional",   ["constituic","constitucional","mandado de seguranca","direito fundamental","isonomia","devido processo","acao direta","stf","recurso extraordinario","repercussao geral"]),
    ("ambiental",        ["ambient","meio ambiente","flora","fauna","floresta","poluicao","ibama"]),
    ("empresarial",      ["empresa","sociedade ","falencia","recuperacao judicial","cheque","nota promissoria","duplicata","marca","patente"]),
]

RAMOS = {
    "tributario":       "Direito Tributario",
    "previdenciario":   "Direito Previdenciario",
    "trabalhista":      "Direito do Trabalho",
    "penal":            "Direito Penal",
    "processual-penal": "Direito Processual Penal",
    "administrativo":   "Direito Administrativo",
    "consumidor":       "Direito do Consumidor",
    "civil":            "Direito Civil",
    "processual-civil": "Direito Processual Civil",
    "constitucional":   "Direito Constitucional",
    "ambiental":        "Direito Ambiental",
    "empresarial":      "Direito Empresarial",
}


def _normalizar(texto: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFD", texto.lower())
        if unicodedata.category(c) != "Mn"
    )


def classificar(texto: str):
    t = _normalizar(texto)
    for tema, kws in TEMAS:
        if any(kw in t for kw in kws):
            return tema, RAMOS.get(tema, "Geral")
    return "jurisprudencia-pacifica", "Geral"


# ── Gerador de nota ───────────────────────────────────────────────────────────

def gerar_nota(s: dict, hoje: str) -> str:
    tema, ramo = classificar(s["texto"])

    fm = {
        "sumula":               str(s["numero"]),
        "tribunal":             "STF",
        "tipo":                 "sumula-stf",
        "status":               s["status"],
        "data_aprovacao":       s["data_aprovacao"],
        "referencia_legislativa": s.get("referencia_legislativa", "")[:200],
        "tema":                 tema,
        "ramo":                 ramo,
        "relacionados":         [],
        "tags":                 ["sumula-stf", "jurisprudencia", "stf", f"sumula-{s['numero']}", tema],
        "created":              hoje,
    }
    fm_str = yaml.dump(fm, allow_unicode=True, default_flow_style=False, sort_keys=False)

    status_badge = s["status"].upper()
    ref = s.get("referencia_legislativa", "").strip() or "_Não listada no PDF._"

    return f"""---
{fm_str}---

# Sumula STF {s['numero']}

**Tribunal:** Supremo Tribunal Federal
**Status:** {status_badge}
**Aprovada em:** {s['data_aprovacao']}

---

## TEXTO DA SUMULA

> {s['texto']}

---

## ANALISE

### Jurisprudencia Consolidada

[O que esta sumula consolida no entendimento do STF?]

### Aplicacao Pratica

[Como os tribunais inferiores aplicam esta sumula?]

### Excecoes e Ressalvas

[Ha enunciados que limitam a aplicacao?]

---

## REFERENCIA LEGISLATIVA

{ref}

---

## JURISPRUDENCIA RELACIONADA

[Precedentes do STF que deram origem a este verbete]

---

**Ultima atualizacao:** {hoje}
"""


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    OUT = Path(__file__).parent.parent / "00_APEX" / "SUMULAS STF" / "Sumulas"
    OUT.mkdir(parents=True, exist_ok=True)

    print("Extraindo PDF...")
    sumulas = extrair_sumulas_pdf()
    hoje = datetime.now().strftime("%Y-%m-%d")
    contagem = {}
    salvas = 0
    erros = 0

    for s in sumulas:
        tema, ramo = classificar(s["texto"])
        contagem[ramo] = contagem.get(ramo, 0) + 1
        try:
            nota = gerar_nota(s, hoje)
            path = OUT / f"Sumula-STF-{s['numero']:04d}.md"
            path.write_text(nota, encoding="utf-8")
            salvas += 1
        except Exception as e:
            print(f"  ERRO sumula {s['numero']}: {e}")
            erros += 1

    print(f"\nResultado:")
    print(f"  Salvas:   {salvas}/{len(sumulas)}")
    print(f"  Erros:    {erros}")
    print(f"\nDistribuicao por ramo:")
    for r, c in sorted(contagem.items(), key=lambda x: -x[1]):
        print(f"  {r:<38} {c:>3}")
    print(f"\nSaida: {OUT}")


if __name__ == "__main__":
    main()

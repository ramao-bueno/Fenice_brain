#!/usr/bin/env python3
"""
baixar_fontes.py — Baixa HTMLs das fontes oficiais do Planalto/STF/STJ
                   para o repositório centralizado scripts/fontes/

Uso:
  python scripts/baixar_fontes.py              # baixa tudo que está faltando
  python scripts/baixar_fontes.py --forcar     # re-baixa tudo (atualiza)
  python scripts/baixar_fontes.py cp cc cf     # só os módulos indicados
  python scripts/baixar_fontes.py DEL2848      # uma sigla específica
  python scripts/baixar_fontes.py --listar     # mostra status e sai

Requer: pip install requests
"""

import sys
import time
import argparse
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

try:
    import requests
except ImportError:
    print("ERRO: instale requests -> pip install requests")
    sys.exit(1)

FONTES_BASE = Path(__file__).parent / "fontes"

# ─────────────────────────────────────────────────────────────────────────────
# CATÁLOGO DE FONTES
# Planalto serve windows-1252; o script re-salva em UTF-8.
# ─────────────────────────────────────────────────────────────────────────────

FONTES: dict[str, dict] = {

    # ── CONSTITUIÇÃO FEDERAL ──────────────────────────────────────────────────
    "CF88": {
        "pasta": "cf",
        "url": "https://www.planalto.gov.br/ccivil_03/constituicao/constituicaocompilado.htm",
        "desc": "Constituição Federal de 1988 — texto compilado",
    },

    # ── CÓDIGO CIVIL ─────────────────────────────────────────────────────────
    "L10406": {
        "pasta": "cc",
        "url": "https://www.planalto.gov.br/ccivil_03/leis/2002/l10406compilado.htm",
        "desc": "Código Civil (Lei 10.406/2002)",
    },
    "L4657": {
        "pasta": "cc",
        "url": "https://www.planalto.gov.br/ccivil_03/decreto-lei/del4657compilado.htm",
        "desc": "LINDB — Lei de Introdução às Normas do Direito Brasileiro",
    },
    "L13655": {
        "pasta": "cc",
        "url": "https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13655.htm",
        "desc": "Lei 13.655/2018 — LINDB: segurança jurídica e eficiência",
    },

    # ── CÓDIGO DE PROCESSO CIVIL ──────────────────────────────────────────────
    "L13105": {
        "pasta": "cpc",
        "url": "https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm",
        "desc": "Código de Processo Civil (Lei 13.105/2015)",
    },

    # ── CÓDIGO DE DEFESA DO CONSUMIDOR ───────────────────────────────────────
    "L8078": {
        "pasta": "cdc",
        "url": "https://www.planalto.gov.br/ccivil_03/leis/l8078compilado.htm",
        "desc": "Código de Defesa do Consumidor (Lei 8.078/1990)",
    },

    # ── CÓDIGO PENAL ──────────────────────────────────────────────────────────
    "DEL2848": {
        "pasta": "cp",
        "url": "https://www.planalto.gov.br/ccivil_03/decreto-lei/del2848compilado.htm",
        "desc": "Código Penal (Decreto-Lei 2.848/1940 — compilado)",
    },
    "L7492": {
        "pasta": "cp",
        "url": "https://www.planalto.gov.br/ccivil_03/leis/l7492.htm",
        "desc": "Lei 7.492/1986 — Crimes contra o Sistema Financeiro",
    },
    "L8072": {
        "pasta": "cp",
        "url": "https://www.planalto.gov.br/ccivil_03/leis/l8072.htm",
        "desc": "Lei 8.072/1990 — Crimes Hediondos",
    },
    "L8137": {
        "pasta": "cp",
        "url": "https://www.planalto.gov.br/ccivil_03/leis/l8137.htm",
        "desc": "Lei 8.137/1990 — Crimes contra a Ordem Tributária",
    },
    "L9605": {
        "pasta": "cp",
        "url": "https://www.planalto.gov.br/ccivil_03/leis/l9605.htm",
        "desc": "Lei 9.605/1998 — Crimes Ambientais",
    },
    "L9613": {
        "pasta": "cp",
        "url": "https://www.planalto.gov.br/ccivil_03/leis/l9613.htm",
        "desc": "Lei 9.613/1998 — Lavagem de Dinheiro",
    },
    "L11343": {
        "pasta": "cp",
        "url": "https://www.planalto.gov.br/ccivil_03/_ato2004-2006/2006/lei/l11343.htm",
        "desc": "Lei 11.343/2006 — Lei de Drogas (SISNAD)",
    },
    "L12850": {
        "pasta": "cp",
        "url": "https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2013/lei/l12850.htm",
        "desc": "Lei 12.850/2013 — Organizações Criminosas",
    },
    "L14132": {
        "pasta": "cp",
        "url": "https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2021/lei/l14132.htm",
        "desc": "Lei 14.132/2021 — Stalking (perseguição)",
    },
    "L14155": {
        "pasta": "cp",
        "url": "https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2021/lei/l14155.htm",
        "desc": "Lei 14.155/2021 — Crimes eletrônicos (estelionato digital)",
    },
    "L14811": {
        "pasta": "cp",
        "url": "https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2024/Lei/L14811.htm",
        "desc": "Lei 14.811/2024 — Proteção de crianças em parques/eventos",
    },

    # ── CÓDIGO DE PROCESSO PENAL ──────────────────────────────────────────────
    "DEL3689": {
        "pasta": "cpp",
        "url": "https://www.planalto.gov.br/ccivil_03/decreto-lei/del3689compilado.htm",
        "desc": "Código de Processo Penal (Decreto-Lei 3.689/1941 — compilado)",
    },
    "L7210": {
        "pasta": "cpp",
        "url": "https://www.planalto.gov.br/ccivil_03/leis/l7210compilado.htm",
        "desc": "Lei 7.210/1984 — Lei de Execução Penal (LEP)",
    },
    "L9099": {
        "pasta": "cpp",
        "url": "https://www.planalto.gov.br/ccivil_03/leis/l9099.htm",
        "desc": "Lei 9.099/1995 — Juizados Especiais Cíveis e Criminais",
    },
    "L11340": {
        "pasta": "cpp",
        "url": "https://www.planalto.gov.br/ccivil_03/_ato2004-2006/2006/lei/l11340.htm",
        "desc": "Lei 11.340/2006 — Lei Maria da Penha",
    },
    "L13869": {
        "pasta": "cpp",
        "url": "https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2019/lei/l13869.htm",
        "desc": "Lei 13.869/2019 — Abuso de Autoridade",
    },
    "L13964": {
        "pasta": "cpp",
        "url": "https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2019/lei/l13964.htm",
        "desc": "Lei 13.964/2019 — Pacote Anticrime",
    },

    # ── DIREITO ADMINISTRATIVO / PÚBLICO ─────────────────────────────────────
    "L8112": {
        "pasta": "publico",
        "url": "https://www.planalto.gov.br/ccivil_03/leis/l8112cons.htm",
        "desc": "Lei 8.112/1990 — Estatuto dos Servidores Públicos Federais",
    },
    "L8429": {
        "pasta": "publico",
        "url": "https://www.planalto.gov.br/ccivil_03/leis/l8429.htm",
        "desc": "Lei 8.429/1992 — Improbidade Administrativa",
    },
    "L9784": {
        "pasta": "publico",
        "url": "https://www.planalto.gov.br/ccivil_03/leis/l9784.htm",
        "desc": "Lei 9.784/1999 — Processo Administrativo Federal",
    },
    "L12527": {
        "pasta": "publico",
        "url": "https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2011/lei/l12527.htm",
        "desc": "Lei 12.527/2011 — Lei de Acesso à Informação (LAI)",
    },
    "L12846": {
        "pasta": "publico",
        "url": "https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2012/lei/l12846.htm",
        "desc": "Lei 12.846/2013 — Lei Anticorrupção",
    },

    # ── PREVIDENCIÁRIO / ESPECIAL ─────────────────────────────────────────────
    "L8212": {
        "pasta": "especial",
        "url": "https://www.planalto.gov.br/ccivil_03/leis/l8212cons.htm",
        "desc": "Lei 8.212/1991 — Custeio da Seguridade Social",
    },
    "L8213": {
        "pasta": "especial",
        "url": "https://www.planalto.gov.br/ccivil_03/leis/l8213cons.htm",
        "desc": "Lei 8.213/1991 — Planos de Benefícios da Previdência Social",
    },
    "L12965": {
        "pasta": "especial",
        "url": "https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2014/lei/l12965.htm",
        "desc": "Lei 12.965/2014 — Marco Civil da Internet",
    },
    "L13709": {
        "pasta": "especial",
        "url": "https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2018/lei/l13709.htm",
        "desc": "Lei 13.709/2018 — LGPD",
    },

    # ── DIREITO INTERNACIONAL ─────────────────────────────────────────────────
    "D0678": {
        "pasta": "internacional",
        "url": "https://www.planalto.gov.br/ccivil_03/decreto/1990-1994/d0678.htm",
        "desc": "Decreto 678/1992 — CADH (Pacto de San José da Costa Rica)",
    },
    "D7030": {
        "pasta": "internacional",
        "url": "https://www.planalto.gov.br/ccivil_03/_ato2007-2010/2009/decreto/d7030.htm",
        "desc": "Decreto 7.030/2009 — CVDT (Convenção de Viena sobre Tratados)",
    },
    "D592": {
        "pasta": "internacional",
        "url": "https://www.planalto.gov.br/ccivil_03/decreto/1990-1994/d0592.htm",
        "desc": "Decreto 592/1992 — PIDCP (Pacto Internacional de Direitos Civis)",
    },
    "D6949": {
        "pasta": "internacional",
        "url": "https://www.planalto.gov.br/ccivil_03/_ato2007-2010/2009/decreto/d6949.htm",
        "desc": "Decreto 6.949/2009 — CDPD (Convenção sobre Dir. da Pessoa com Deficiência)",
    },

    # ── CONSTITUIÇÃO: REMÉDIOS E CONTROLE DE CONSTITUCIONALIDADE ─────────────
    "L12016": {
        "pasta": "cf",
        "url": "https://www.planalto.gov.br/ccivil_03/_ato2007-2010/2009/lei/l12016.htm",
        "desc": "Lei 12.016/2009 — Mandado de Segurança",
    },
    "L13300": {
        "pasta": "cf",
        "url": "https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2016/lei/l13300.htm",
        "desc": "Lei 13.300/2016 — Mandado de Injunção",
    },
    "L4717": {
        "pasta": "cf",
        "url": "https://www.planalto.gov.br/ccivil_03/leis/l4717.htm",
        "desc": "Lei 4.717/1965 — Ação Popular",
    },
    "L9507": {
        "pasta": "cf",
        "url": "https://www.planalto.gov.br/ccivil_03/leis/l9507.htm",
        "desc": "Lei 9.507/1997 — Habeas Data",
    },
    "L9709": {
        "pasta": "cf",
        "url": "https://www.planalto.gov.br/ccivil_03/leis/l9709.htm",
        "desc": "Lei 9.709/1998 — Plebiscito, Referendo e Iniciativa Popular",
    },
    "L9868": {
        "pasta": "cf",
        "url": "https://www.planalto.gov.br/ccivil_03/leis/l9868.htm",
        "desc": "Lei 9.868/1999 — ADI e ADC (controle concentrado)",
    },
    "L9882": {
        "pasta": "cf",
        "url": "https://www.planalto.gov.br/ccivil_03/leis/l9882.htm",
        "desc": "Lei 9.882/1999 — ADPF",
    },
    "LCP95": {
        "pasta": "cf",
        "url": "https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp95.htm",
        "desc": "LC 95/1998 — Técnica Legislativa",
    },
    "L11417": {
        "pasta": "cf",
        "url": "https://www.planalto.gov.br/ccivil_03/_ato2004-2006/2006/lei/l11417.htm",
        "desc": "Lei 11.417/2006 — Súmula Vinculante",
    },

    # ── CPC: JUIZADOS FEDERAIS ────────────────────────────────────────────────
    "L10259": {
        "pasta": "cpc",
        "url": "https://www.planalto.gov.br/ccivil_03/leis/2001/l10259.htm",
        "desc": "Lei 10.259/2001 — Juizados Especiais Federais",
    },

    # ── CPP COMPLEMENTAR ──────────────────────────────────────────────────────
    "L7960": {
        "pasta": "cpp",
        "url": "https://www.planalto.gov.br/ccivil_03/leis/l7960.htm",
        "desc": "Lei 7.960/1989 — Prisão Temporária",
    },

    # ── ESPECIAL: PROPRIEDADE INTELECTUAL ─────────────────────────────────────
    "L9609": {
        "pasta": "especial",
        "url": "https://www.planalto.gov.br/ccivil_03/leis/l9609.htm",
        "desc": "Lei 9.609/1998 — Lei do Software",
    },
    "L9610": {
        "pasta": "especial",
        "url": "https://www.planalto.gov.br/ccivil_03/leis/l9610.htm",
        "desc": "Lei 9.610/1998 — Lei de Direitos Autorais",
    },

    # ── INTERNACIONAL: LEIS NACIONAIS ─────────────────────────────────────────
    "L9307": {
        "pasta": "internacional",
        "url": "https://www.planalto.gov.br/ccivil_03/leis/l9307.htm",
        "desc": "Lei 9.307/1996 — Arbitragem",
    },
    "L13445": {
        "pasta": "internacional",
        "url": "https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2017/lei/l13445.htm",
        "desc": "Lei 13.445/2017 — Migração",
    },

    # ── SÚMULAS STF / STJ ────────────────────────────────────────────────────
    # Portais JavaScript — precisam de scraper dedicado.
    # Baixar manualmente em: scripts/fontes/sumulas/stf/ e sumulas/stj/
    # Ver: https://portal.stf.jus.br/sumulas/
    #      https://scon.stj.jus.br/SCON/sumanot/toc.jsp

}

# ─────────────────────────────────────────────────────────────────────────────
# MÓDULOS — agrupamentos por área para seleção na linha de comando
# ─────────────────────────────────────────────────────────────────────────────

MODULOS: dict[str, list[str]] = {
    "cf":            ["CF88", "L12016", "L13300", "L4717", "L9507", "L9709",
                      "L9868", "L9882", "LCP95", "L11417"],
    "cc":            ["L10406", "L4657", "L13655"],
    "cpc":           ["L13105", "L10259"],
    "cdc":           ["L8078"],
    "cp":            ["DEL2848", "L7492", "L8072", "L8137", "L9605", "L9613",
                      "L11343", "L12850", "L14132", "L14155", "L14811"],
    "cpp":           ["DEL3689", "L7210", "L7960", "L9099", "L11340", "L13869", "L13964"],
    "publico":       ["L8112", "L8429", "L9784", "L12527", "L12846"],
    "especial":      ["L8212", "L8213", "L12965", "L13709", "L9609", "L9610"],
    "internacional": ["D0678", "D7030", "D592", "D6949", "L9307", "L13445"],
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
}


def destino(sigla: str) -> Path:
    return FONTES_BASE / FONTES[sigla]["pasta"] / f"{sigla}.html"


def baixar(sigla: str, forcar: bool = False) -> bool:
    cfg = FONTES[sigla]
    arq = destino(sigla)

    if arq.exists() and not forcar:
        kb = arq.stat().st_size // 1024
        print(f"  [OK-cache]  {sigla:12} já existe ({kb} KB)")
        return True

    print(f"  [baixando]  {sigla:12} {cfg['desc'][:58]}...")

    for tentativa in range(1, 4):
        try:
            resp = requests.get(cfg["url"], headers=HEADERS, timeout=30)
            resp.raise_for_status()

            # Planalto serve windows-1252 mesmo sem declarar charset explícito.
            # Decodifica para str e re-codifica para UTF-8 antes de salvar.
            enc = (resp.encoding or "iso-8859-1").lower()
            if enc in ("iso-8859-1", "latin-1", "windows-1252"):
                html = resp.content.decode("windows-1252", errors="replace")
            else:
                html = resp.content.decode(enc, errors="replace")

            arq.write_bytes(html.encode("utf-8"))
            kb = arq.stat().st_size // 1024
            print(f"  [salvo]     {sigla:12} {kb} KB → {arq.relative_to(FONTES_BASE.parent)}")
            return True

        except requests.HTTPError as e:
            codigo = e.response.status_code if e.response else "?"
            print(f"  [HTTP {codigo}]   {sigla}: {e}")
            if codigo in (404, 403, 410):
                print(f"             URL: {cfg['url']}")
                return False

        except Exception as e:
            print(f"  [erro {tentativa}/3]  {sigla}: {e}")
            if tentativa < 3:
                time.sleep(2 ** tentativa)

    return False


def listar_status() -> None:
    total = len(FONTES)
    existem = 0
    faltam: list[str] = []

    for sigla, cfg in FONTES.items():
        arq = destino(sigla)
        if arq.exists():
            kb = arq.stat().st_size // 1024
            print(f"  ✓ {sigla:12} [{cfg['pasta']:13}]  {kb:6} KB  {cfg['desc'][:48]}")
            existem += 1
        else:
            print(f"  ✗ {sigla:12} [{cfg['pasta']:13}]  FALTANDO   {cfg['desc'][:48]}")
            faltam.append(sigla)

    print(f"\n  {existem}/{total} presentes", end="")
    if faltam:
        print(f" — {len(faltam)} faltando")
        grupos: dict[str, list[str]] = {}
        for s in faltam:
            grupos.setdefault(FONTES[s]["pasta"], []).append(s)
        print("  Faltando por pasta:")
        for pasta, sigs in sorted(grupos.items()):
            print(f"    {pasta}: {' '.join(sigs)}")
        print(f"\n  Para baixar tudo: python scripts/baixar_fontes.py")
    else:
        print(" — tudo presente!")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Baixa HTMLs do Planalto para scripts/fontes/",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Módulos disponíveis: " + ", ".join(MODULOS) + "\n"
            "Siglas individuais:  DEL2848, L10406, CF88, ..."
        ),
    )
    parser.add_argument(
        "alvos", nargs="*",
        help="Módulos (cp, cc, cf…) ou siglas (DEL2848, L10406…); omitir = todos",
    )
    parser.add_argument(
        "--forcar", "-f", action="store_true",
        help="Re-baixa mesmo se o arquivo já existe",
    )
    parser.add_argument(
        "--listar", "-l", action="store_true",
        help="Mostra status de cada fonte e sai sem baixar",
    )
    args = parser.parse_args()

    if args.listar:
        listar_status()
        return

    # Resolve siglas a partir dos alvos fornecidos
    if args.alvos:
        siglas: list[str] = []
        for alvo in args.alvos:
            if alvo in MODULOS:
                siglas.extend(MODULOS[alvo])
            elif alvo.upper() in FONTES:
                siglas.append(alvo.upper())
            else:
                validos = ", ".join(list(MODULOS) + list(FONTES))
                print(f"AVISO: '{alvo}' desconhecido. Válidos: {validos}")
        if not siglas:
            print("Nenhum alvo válido. Abortando.")
            sys.exit(1)
        siglas = list(dict.fromkeys(siglas))  # deduplica mantendo ordem
    else:
        siglas = list(FONTES)

    print(f"Fenice bRain — download de fontes jurídicas")
    print(f"Destino: {FONTES_BASE}")
    print(f"Alvos: {len(siglas)} fonte(s)", "(--forcar)" if args.forcar else "")
    print()

    ok = 0
    erros: list[str] = []

    for i, sigla in enumerate(siglas, 1):
        prefixo = f"[{i:02}/{len(siglas):02}]"
        print(prefixo, end=" ")
        if baixar(sigla, forcar=args.forcar):
            ok += 1
        else:
            erros.append(sigla)
        if i < len(siglas):
            time.sleep(1.2)  # respeita o servidor do Planalto

    print()
    if erros:
        print(f"Resultado: {ok}/{len(siglas)} OK — {len(erros)} com erro: {', '.join(erros)}")
        print("Dica: verifique as URLs no catálogo FONTES[] e tente --forcar.")
        sys.exit(1)
    else:
        print(f"Resultado: {ok}/{len(siglas)} OK — tudo certo!")


if __name__ == "__main__":
    main()

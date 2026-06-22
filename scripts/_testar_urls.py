#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from planalto_pipeline import baixar_html, parsear_lei

urls_teste = [
    ("L11340a", "https://www.planalto.gov.br/ccivil_03/_ato2003-2006/2006/lei/l11340compilada.htm"),
    ("L11340b", "https://www.planalto.gov.br/ccivil_03/_ato2003-2006/2006/lei/L11340.htm"),
    ("L11343a", "https://www.planalto.gov.br/ccivil_03/_ato2003-2006/2006/lei/l11343compilada.htm"),
    ("L10741a", "https://www.planalto.gov.br/ccivil_03/_ato2003-2006/2003/lei/l10741.htm"),
    ("L10741b", "https://www.planalto.gov.br/ccivil_03/leis/2003/L10741.htm"),
    ("L10741c", "https://www.planalto.gov.br/ccivil_03/_ato2003-2006/2003/lei/L10741.htm"),
]

for nome, url in urls_teste:
    p = baixar_html(url, forcar=True)
    if p:
        d = parsear_lei(p, url_origem=url)
        chars = len(d.get("texto_vigente", ""))
        print(f"{nome}: {chars:,} chars")
    else:
        print(f"{nome}: 404 / ERRO")

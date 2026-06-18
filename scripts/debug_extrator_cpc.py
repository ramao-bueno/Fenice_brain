#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')
from pathlib import Path
from extrator_html_generico import extrair_artigos_html

html_file = Path("../Fenice bRain/03_PROCESSO_CIVIL/CÓDIGO_PROCESSO_CIVIL/L13105.html")
artigos = extrair_artigos_html(html_file)
print(f"Total extraído: {len(artigos)} artigos")
if artigos:
    print(f"Primeiros 10: {[a['numero'] for a in artigos[:10]]}")
    print(f"Últimos 5: {[a['numero'] for a in artigos[-5:]]}")

    # Verifica se há saltos
    nums = sorted([a['numero'] for a in artigos])
    saltos = []
    for i in range(len(nums)-1):
        if nums[i+1] - nums[i] > 1:
            saltos.append((nums[i], nums[i+1]))
    if saltos:
        print(f"\nSaltos na numeração ({len(saltos)} saltos):")
        for a, b in saltos[:20]:
            print(f"  {a} -> {b}")

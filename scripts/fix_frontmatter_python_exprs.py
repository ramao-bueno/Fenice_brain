#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Corrige expressões Python no frontmatter YAML dos arquivos .md do vault.

Padrão problemático gerado pelo pipeline:
  livro: "I — " if c['livro'] else ""
  titulo: "III — ..." if c['titulo'] else ""

Substitui pela string antes do 'if':
  livro: "I — "
  titulo: "III — ..."
"""
import re
import sys
from pathlib import Path

VAULT = Path(__file__).parent.parent
PATTERN = re.compile(r'^(\s*\w+:\s*)(".*?")\s+if c\[\'.*?\'\] else ".*?"(\s*)$')

def fix_file(path: Path) -> bool:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return False

    if "if c['" not in text:
        return False

    lines = text.splitlines(keepends=True)
    new_lines = []
    changed = False
    for line in lines:
        m = PATTERN.match(line.rstrip('\n').rstrip('\r'))
        if m:
            fixed = f"{m.group(1)}{m.group(2)}\n"
            new_lines.append(fixed)
            changed = True
        else:
            new_lines.append(line)

    if changed:
        path.write_text("".join(new_lines), encoding="utf-8")
    return changed

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    files = list(VAULT.rglob("*.md"))
    total = 0
    for f in files:
        if fix_file(f):
            total += 1
    print(f"Corrigidos: {total} arquivos")

if __name__ == "__main__":
    main()

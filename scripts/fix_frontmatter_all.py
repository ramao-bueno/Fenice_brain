#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Valida e corrige todos os frontmatters YAML do vault.

Problemas tratados:
1. Expressões Python: `"valor" if c['x'] else ""` → `"valor"`
2. Aspas duplas não escapadas em valores: `titulo: "texto "com" aspas"`
3. Dois-pontos sem escape em valores sem aspas
4. Frontmatter com YAML completamente inválido → remove o frontmatter
"""
import re
import sys
import yaml
from pathlib import Path

VAULT = Path(__file__).parent.parent

# Padrão 1: expressões Python
RE_PYTHON_EXPR = re.compile(
    r'^(\s*\w[\w\-]*:\s*)(".*?")\s+if\s+c\[\'.*?\'\]\s+else\s+".*?"\s*$'
)

def extract_frontmatter(text: str):
    """Retorna (frontmatter_raw, body) ou (None, text) se não houver."""
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end == -1:
        return None, text
    fm = text[3:end].strip()
    body = text[end+4:]
    return fm, body

def fix_python_exprs(fm_lines: list) -> tuple:
    """Corrige expressões Python. Retorna (linhas_corrigidas, n_fixes)."""
    fixed = []
    n = 0
    for line in fm_lines:
        m = RE_PYTHON_EXPR.match(line.rstrip('\n'))
        if m:
            fixed.append(f"{m.group(1)}{m.group(2)}\n")
            n += 1
        else:
            fixed.append(line)
    return fixed, n

def sanitize_yaml_value(line: str) -> str:
    """Tenta consertar linhas YAML com aspas problemáticas."""
    # Detecta padrão: key: "valor com aspas dentro"
    m = re.match(r'^(\s*[\w\-]+:\s*)(.+)$', line.rstrip('\n'))
    if not m:
        return line
    key_part = m.group(1)
    val_part = m.group(2).strip()

    # Se o valor começa com aspas mas tem aspas internas problemáticas
    if val_part.startswith('"') and val_part.count('"') > 2:
        # Remove todas as aspas duplas internas, mantendo as externas
        inner = val_part[1:].rstrip('"')
        inner = inner.replace('"', "'")
        return f"{key_part}\"{inner}\"\n"

    return line

def process_file(path: Path) -> str:
    """'ok', 'fixed', 'removed_fm', 'skipped'"""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return "skipped"

    fm_raw, body = extract_frontmatter(text)
    if fm_raw is None:
        return "ok"

    fm_lines = (fm_raw + "\n").splitlines(keepends=True)

    # Passo 1: corrigir expressões Python
    fm_lines, n_py = fix_python_exprs(fm_lines)

    # Passo 2: tentar parsear o YAML
    try:
        yaml.safe_load("".join(fm_lines))
        if n_py > 0:
            new_text = f"---\n{''.join(fm_lines)}---{body}"
            path.write_text(new_text, encoding="utf-8")
            return "fixed"
        return "ok"
    except yaml.YAMLError:
        pass

    # Passo 3: tentar sanitizar linha a linha
    sanitized = [sanitize_yaml_value(l) for l in fm_lines]
    try:
        yaml.safe_load("".join(sanitized))
        new_text = f"---\n{''.join(sanitized)}---{body}"
        path.write_text(new_text, encoding="utf-8")
        return "fixed"
    except yaml.YAMLError:
        pass

    # Passo 4: remover frontmatter completamente (melhor do que bloquear o build)
    path.write_text(body.lstrip('\n'), encoding="utf-8")
    return "removed_fm"

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    files = list(VAULT.rglob("*.md"))
    print(f"Verificando {len(files)} arquivos...")

    counts = {"ok": 0, "fixed": 0, "removed_fm": 0, "skipped": 0}
    removed = []

    for f in files:
        result = process_file(f)
        counts[result] += 1
        if result == "removed_fm":
            removed.append(str(f.relative_to(VAULT)))

    print(f"\nResultado:")
    print(f"  OK (sem alteração): {counts['ok']}")
    print(f"  Corrigidos:         {counts['fixed']}")
    print(f"  FM removido:        {counts['removed_fm']}")
    print(f"  Ignorados:          {counts['skipped']}")

    if removed:
        print(f"\nArquivos com frontmatter removido ({len(removed)}):")
        for r in removed[:20]:
            print(f"  - {r}")
        if len(removed) > 20:
            print(f"  ... e mais {len(removed)-20}")

if __name__ == "__main__":
    main()

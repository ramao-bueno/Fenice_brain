#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera artigos LINDB (Arts. 20-30) no padrao Fenice Brain
Fonte: L13655.html (Lei 13.655/2018 — adiciona arts. 20-30 ao Dec-Lei 4.657/1942)
"""
import sys, re, html, yaml
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent
HTML_PATH    = PROJECT_ROOT / "02 - Áreas" / "Base Jurídica" / "02_DIREITO_PRIVADO" / "DIREITO_CIVIL" / "L13655.html"
OUTPUT_BASE  = PROJECT_ROOT / 'Fenice bRain' / '02_DIREITO_PRIVADO' / 'DIREITO_CIVIL' / 'Artigos' / 'LINDB'

LEI_NOME     = 'Decreto-Lei 4.657/1942 (LINDB) — Lei 13.655/2018'
PLANALTO_URL = 'https://www.planalto.gov.br/ccivil_03/Decreto-Lei/Del4657.htm'
PLANALTO_LEI = 'https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13655.htm'


def limpar_html(texto: str) -> str:
    """Remove tags HTML e normaliza espaços."""
    t = re.sub(r'<[^>]+>', ' ', texto)
    t = html.unescape(t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t


def extrair_artigos(html_text: str) -> list:
    """Extrai artigos 20-30 do HTML da Lei 13.655/2018."""
    artigos = []

    # Padrão: ârt. N. texto... até próximo Art.
    # O HTML usa windows-1252 com caracteres especiais como º → ° ou \xba
    texto = html_text.decode('windows-1252', errors='replace')

    # Remove CSS/head — começa a partir do body
    idx_body = texto.find('<blockquote>')
    if idx_body > 0:
        texto = texto[idx_body:]

    # Limpa HTML e obtém texto limpo
    limpo = limpar_html(texto)

    # Divide por marcadores de artigo
    # Padrão: Art. 20. | Art. 20 . | "Art. 20. | ...
    marcadores = list(re.finditer(
        r'(?:[\"«""])?\s*(Art\.\s*(\d+)\s*\.)',
        limpo
    ))

    for i, m in enumerate(marcadores):
        try:
            num_str = m.group(2).strip()
            num = int(num_str)
            if num < 20 or num > 30:
                continue

            inicio = m.start()
            fim = marcadores[i+1].start() if i+1 < len(marcadores) else len(limpo)
            bloco = limpo[inicio:fim].strip()

            # Remove o prefixo "Art. N."
            sem_prefixo = re.sub(
                r'^[\"««“]?Art\.\s*\d+\s*\.\s*', '', bloco
            ).strip()

            # Separa caput dos parágrafos
            caput_fim = sem_prefixo.find('Parágrafo')
            if caput_fim < 0:
                caput_fim = sem_prefixo.find('§')
            if caput_fim < 0:
                caput_fim = sem_prefixo.find(' I -')
            if caput_fim < 0:
                caput_fim = sem_prefixo.find(' I – ')

            if caput_fim > 0:
                caput    = sem_prefixo[:caput_fim].strip()
                restante = sem_prefixo[caput_fim:].strip()
            else:
                caput    = sem_prefixo.strip()
                restante = ''

            # Título do artigo = primeiros 80 chars do caput
            titulo = caput[:80].rstrip('.,;')

            artigos.append({
                'numero':   num,
                'titulo':   titulo,
                'caput':    caput,
                'restante': restante,
                'redacao':  sem_prefixo[:800],
            })

        except Exception as e:
            print(f'  SKIP art {m.group(2)}: {e}')
            continue

    artigos.sort(key=lambda x: x['numero'])
    return artigos


def gerar_md(art: dict) -> str:
    num      = art['numero']
    titulo   = art['titulo']
    redacao  = art['redacao']
    caput    = art['caput']
    restante = art['restante']
    planalto = f'{PLANALTO_URL}#art{num}'

    # Detecta parágrafos para tags
    tags = ['cc', 'lindb', 'vigente', f'art-{num}', 'lindb-13655', 'direito-civil']
    if 'Parágrafo único' in redacao or 'Parágrafo único' in redacao:
        tags.append('paragrafo-unico')
    for n in re.findall(r'§\s*(\d+)', redacao):
        tags.append(f'paragrafo-{n}')
    for r in ['I','II','III','IV','V','VI']:
        if re.search(rf'\b{r}\s*[-–]', redacao):
            tags.append(f'inciso-{r.lower()}')

    fm = {
        'artigo':  str(num),
        'lei':     LEI_NOME,
        'tipo':    'direito-civil',
        'livro':   'LINDB',
        'status':  'vigente',
        'planalto_url': planalto,
        'tags':    tags,
        'created': datetime.now().strftime('%Y-%m-%d'),
    }
    fm_str = yaml.dump(fm, allow_unicode=True, default_flow_style=False, sort_keys=False)

    art_anterior = max(20, num - 1)
    art_seguinte = num + 1

    corpo = f"""# LINDB Art. {num} — {titulo}

**Lei:** {LEI_NOME}
**Livro:** LINDB — Lei de Introdução às Normas do Direito Brasileiro
**Status:** VIGENTE
**Planalto:** [Texto oficial]({planalto})

---

## REDACAO LEGAL

> {redacao}

---

## ANALISE TECNICA

### Conceito Central

[Síntese do conteúdo normativo do artigo]

### Elementos-Chave

| Elemento | Descrição |
|----------|-----------|
| **Âmbito** | Esferas administrativa, controladora e judicial |
| **Destinatário** | Agentes e autoridades públicas |

---

## ARTIGOS CORRELATOS

### Mesma LINDB
- [[Art. {art_anterior} — LINDB]] — artigo anterior
- [[Art. {art_seguinte} — LINDB]] — artigo seguinte

### Legislação Relacionada
- [[CF Art. 5 — CF]] — legalidade e devido processo
- [[CF Art. 37 — CF]] — princípios da administração pública

---

## JURISPRUDENCIA STJ / STF

[Precedentes sobre este artigo]

---

**Última atualização:** {datetime.now().strftime('%Y-%m-%d')}
**Fonte:** [planalto.gov.br]({planalto})
**Lei:** [Lei 13.655/2018]({PLANALTO_LEI})
"""
    return f'---\n{fm_str}---\n\n{corpo}'


def main():
    print('\n' + '='*60)
    print('GERADOR LINDB: L13655.html -> Markdown')
    print('='*60 + '\n')

    html_bytes = HTML_PATH.read_bytes()
    artigos = extrair_artigos(html_bytes)

    if not artigos:
        print('ERRO: Nenhum artigo extraído!')
        return

    print(f'{len(artigos)} artigos encontrados: {[a["numero"] for a in artigos]}\n')

    OUTPUT_BASE.mkdir(parents=True, exist_ok=True)
    salvos = 0

    for art in artigos:
        conteudo = gerar_md(art)
        titulo_limpo = art['titulo'].replace('/', '-')[:60]
        fname = f"Art. {art['numero']} — LINDB.md"
        path = OUTPUT_BASE / fname
        path.write_text(conteudo, encoding='utf-8')
        print(f'  ✔ {fname}')
        salvos += 1

    # INDEX da LINDB
    idx_linhas = [
        '---\n',
        'tags: [lindb, cc, direito-civil, index]\n',
        f'created: {datetime.now().strftime("%Y-%m-%d")}\n',
        '---\n\n',
        '# INDEX — LINDB (Arts. 20-30)\n\n',
        '**Lei:** Decreto-Lei 4.657/1942 com redação da Lei 13.655/2018\n',
        f'**Planalto:** [Texto oficial]({PLANALTO_URL})\n\n',
        '---\n\n',
        '## Artigos\n\n',
    ]
    for art in artigos:
        idx_linhas.append(f"- [[Art. {art['numero']} — LINDB]] — {art['titulo'][:70]}\n")

    idx_linhas += [
        '\n## Links\n\n',
        '- [[INDEX — CF/88 Completo]] — Hierarquia normativa\n',
        '- [[INDEX Código Civil]] — Código Civil\n',
        '- [[00_NAVIGATOR]] — Busca por código\n',
    ]
    (OUTPUT_BASE / 'INDEX-LINDB.md').write_text(''.join(idx_linhas), encoding='utf-8')

    print(f'\n{"="*60}')
    print(f'CONCLUIDO: {salvos} artigos + INDEX-LINDB.md')
    print(f'Saída: {OUTPUT_BASE}')
    print('='*60)


if __name__ == '__main__':
    main()

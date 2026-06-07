#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera artigos Decreto 9.830/2019 no padrão Fenice Brain
Fonte: D9830.html — regulamenta Arts. 20-30 da LINDB
"""
import sys, re, html as hlib, yaml
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime

HTML_PATH    = Path(r'C:\Users\oicon\OneDrive\Allah - Islamismo\Stand Alone Legaltech\Fenice brain\FENICE bRain\02_DIREITO_PRIVADO\DIREITO_CIVIL\D9830.html')
PROJECT_ROOT = Path(__file__).parent.parent
OUTPUT_BASE  = PROJECT_ROOT / 'FENICE bRain' / '02_DIREITO_PRIVADO' / 'DIREITO_CIVIL' / 'Artigos' / 'D9830'

LEI_NOME     = 'Decreto 9.830/2019 (Regulamenta LINDB)'
PLANALTO_URL = 'https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2019/decreto/d9830.htm'

# Mapeamento Art → Capítulo
CAPITULOS = {
    range(1,  2):  ('I',   'Disposições Preliminares'),
    range(2,  10): ('II',  'Da Decisão'),
    range(10, 14): ('III', 'Dos Instrumentos'),
    range(14, 21): ('IV',  'Da Responsabilização do Agente Público'),
    range(21, 26): ('V',   'Da Segurança Jurídica na Aplicação das Normas'),
}


def get_capitulo(num: int) -> tuple:
    for r, cap in CAPITULOS.items():
        if num in r:
            return cap
    return ('', '')


def limpar(texto: str) -> str:
    t = re.sub(r'<[^>]+>', ' ', texto)
    t = hlib.unescape(t)
    t = re.sub(r'[\xa0\s]+', ' ', t).strip()
    return t


def extrair_artigos(html_bytes: bytes) -> list:
    txt = html_bytes.decode('windows-1252', errors='replace')
    limpo = limpar(txt)

    # Padrão unificado: Arts 1-9 usam "Art. Nº" | Arts 10-25 usam "Art. N."
    # Ambos cobertos por: Art. N (ordinal OU ponto) espaço texto
    marcadores_todos = list(re.finditer(
        r'\bArt\.\s*(\d{1,2})\s*(?:[ºo°]|\.)\s+',
        limpo
    ))

    # Filtra apenas marcadores de início de artigo (não refs internas)
    vistos_filter = set()
    marcadores_reais = []
    for m in marcadores_todos:
        num = int(m.group(1))
        if num < 1 or num > 25 or num in vistos_filter:
            continue
        # Verifica contexto anterior: deve ser inicio de secao
        pos = m.start()
        ante = limpo[max(0, pos-15):pos].strip()
        # É referência interna se precedido por "nos", "do", "ao", "o"
        if re.search(r'\b(nos|do|ao|o|a|no|na|dos|às|nos|pelo|da|de)\s*$', ante, re.I):
            continue
        vistos_filter.add(num)
        marcadores_reais.append(m)

    print(f'  Marcadores válidos encontrados: {len(marcadores_reais)}')
    artigos = []
    vistos = set()

    for i, m in enumerate(marcadores_reais):
        try:
            num = int(m.group(1))
            if num in vistos or num > 25:
                continue
            vistos.add(num)

            inicio = m.start()
            fim = marcadores_reais[i+1].start() if i+1 < len(marcadores_reais) else len(limpo)
            bloco = limpo[inicio:fim].strip()

            # Remove prefixo "Art. N°"
            sem_prefix = re.sub(r'^Art\.\s*\d+\s*[ºo°]?\s*', '', bloco).strip()

            # Título = primeiros 80 chars até ponto
            titulo_m = re.match(r'^(.{10,80}?)(?:\.|$)', sem_prefix)
            titulo = titulo_m.group(1).strip() if titulo_m else sem_prefix[:80]

            cap_num, cap_nome = get_capitulo(num)

            artigos.append({
                'numero':    num,
                'titulo':    titulo,
                'redacao':   sem_prefix[:800],
                'capitulo':  cap_num,
                'cap_nome':  cap_nome,
            })
        except Exception as e:
            continue

    artigos.sort(key=lambda x: x['numero'])
    return artigos


def gerar_md(art: dict) -> str:
    num      = art['numero']
    titulo   = art['titulo']
    redacao  = art['redacao']
    cap_num  = art['capitulo']
    cap_nome = art['cap_nome']
    planalto = f'{PLANALTO_URL}#art{num}'

    tags = ['d9830', 'lindb', 'direito-civil', 'vigente',
            f'art-{num}', 'decreto-9830', 'seguranca-juridica']
    if 'Parágrafo único' in redacao:
        tags.append('paragrafo-unico')
    for n in re.findall(r'§\s*(\d+)', redacao):
        tags.append(f'paragrafo-{n}')
    for r in ['I','II','III','IV','V','VI','VII','VIII']:
        if re.search(rf'\b{r}\s*[-–]', redacao):
            tags.append(f'inciso-{r.lower()}')
    if cap_num:
        tags.append(f'capitulo-{cap_num.lower()}')

    fm = {
        'artigo':     str(num),
        'lei':        LEI_NOME,
        'tipo':       'direito-civil',
        'livro':      'D9830',
        'capitulo':   f'Capítulo {cap_num} — {cap_nome}' if cap_num else '',
        'status':     'vigente',
        'planalto_url': planalto,
        'tags':       tags,
        'created':    datetime.now().strftime('%Y-%m-%d'),
    }
    fm_str = yaml.dump(fm, allow_unicode=True, default_flow_style=False, sort_keys=False)

    art_ant = max(1, num - 1)
    art_seg = num + 1
    cap_str = f'Capítulo {cap_num} — {cap_nome}' if cap_num else ''

    corpo = f"""# D9830 Art. {num} — {titulo}

**Decreto:** {LEI_NOME}
**{'Capítulo: ' + cap_str if cap_str else ''}**
**Status:** VIGENTE
**Planalto:** [Texto oficial]({planalto})

---

## REDACAO LEGAL

> {redacao}

---

## ANALISE TECNICA

### Conceito Central

[Síntese do conteúdo normativo deste artigo do Decreto 9.830/2019]

### Elementos-Chave

| Elemento | Descrição |
|----------|-----------|
| **Âmbito** | Regulamentação dos Arts. 20-30 LINDB |
| **Destinatário** | Agentes e autoridades públicas |

---

## ARTIGOS CORRELATOS

### Mesmo Decreto
- [[Art. {art_ant} — D9830]] — artigo anterior
- [[Art. {art_seg} — D9830]] — artigo seguinte

### LINDB (regulamentada)
- [[Art. 20 — LINDB]] — consequências práticas da decisão
- [[Art. 28 — LINDB]] — responsabilização do agente público

### Legislação Superior
- [[CF Art. 37 — CF]] — princípios da administração pública
- [[CF Art. 5 — CF]] — legalidade e segurança jurídica

---

## JURISPRUDENCIA

[STJ / STF sobre responsabilização de agentes públicos e segurança jurídica]

---

**Última atualização:** {datetime.now().strftime('%Y-%m-%d')}
**Fonte:** [planalto.gov.br]({planalto})
"""
    return f'---\n{fm_str}---\n\n{corpo}'


def main():
    sep = '=' * 60
    print(f'\n{sep}')
    print('GERADOR D9830: D9830.html -> Markdown')
    print(f'{sep}\n')

    artigos = extrair_artigos(HTML_PATH.read_bytes())

    if not artigos:
        print('ERRO: Nenhum artigo extraído!')
        return

    nums = [a['numero'] for a in artigos]
    print(f'{len(artigos)} artigos: {nums}\n')

    OUTPUT_BASE.mkdir(parents=True, exist_ok=True)
    salvos = 0

    for art in artigos:
        conteudo = gerar_md(art)
        fname = f"Art. {art['numero']} — D9830.md"
        (OUTPUT_BASE / fname).write_text(conteudo, encoding='utf-8')
        cap_info = f"[Cap. {art['capitulo']}]" if art['capitulo'] else ''
        print(f"  ✔ {fname} {cap_info}")
        salvos += 1

    # INDEX
    idx = [
        '---\n',
        'tags: [d9830, lindb, direito-civil, index, seguranca-juridica]\n',
        f'created: {datetime.now().strftime("%Y-%m-%d")}\n',
        '---\n\n',
        '# INDEX — Decreto 9.830/2019\n\n',
        f'**Decreto:** {LEI_NOME}\n',
        f'**Planalto:** [Texto oficial]({PLANALTO_URL})\n',
        '**Regulamenta:** Arts. 20-30 do Decreto-Lei 4.657/1942 (LINDB)\n\n',
        '---\n\n',
    ]

    cap_atual = None
    for art in artigos:
        if art['capitulo'] != cap_atual:
            cap_atual = art['capitulo']
            idx.append(f"\n### Capítulo {cap_atual} — {art['cap_nome']}\n\n")
        titulo_curto = art['titulo'][:65]
        idx.append(f"- [[Art. {art['numero']} — D9830]] — {titulo_curto}\n")

    idx += [
        '\n---\n\n',
        '## Links\n\n',
        '- [[INDEX-LINDB]] — Decreto-Lei 4.657/1942 (LINDB)\n',
        '- [[INDEX — CF/88 Completo]] — Hierarquia normativa\n',
        '- [[00_NAVIGATOR]] — Busca por código\n',
    ]
    (OUTPUT_BASE / 'INDEX-D9830.md').write_text(''.join(idx), encoding='utf-8')

    print(f'\n{sep}')
    print(f'CONCLUIDO: {salvos} artigos + INDEX-D9830.md')
    print(f'Saída: {OUTPUT_BASE}')
    print(sep)


if __name__ == '__main__':
    main()

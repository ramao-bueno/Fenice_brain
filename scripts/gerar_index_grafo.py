"""
gerar_index_grafo.py
Gera arquivos _INDEX_GRAPH.md em cada volume do vault com wikilinks para
todos os seus arquivos .md — habilita local graph (rápido) no GraphModal.

Uso: python scripts/gerar_index_grafo.py
"""

import os

VAULT = r"C:\Fenice_bRain"

VOLUMES = [
    {
        'pasta':  r"02_PENAL\Codigos\CP\DEL2848",
        'titulo': "CP DEL2848 — Índice para Grafo Local",
        'desc':   "Código Penal · 665 artigos atomizados",
        'excluir': ['_INDEX_GRAPH.md', 'CP-INDEX.md', 'INDEX.md'],
    },
    {
        'pasta':  r"00_APEX\SUMULAS STJ\Sumulas",
        'titulo': "Súmulas STJ — Índice para Grafo Local",
        'desc':   "674 súmulas do Superior Tribunal de Justiça",
        'excluir': ['_INDEX_GRAPH.md'],
    },
    {
        'pasta':  r"00_APEX\SUMULAS STF\Sumulas",
        'titulo': "Súmulas STF — Índice para Grafo Local",
        'desc':   "736 súmulas do Supremo Tribunal Federal",
        'excluir': ['_INDEX_GRAPH.md'],
    },
    {
        'pasta':  r"06_JURISCONSULTOS",
        'titulo': "Jurisconsultos — Índice para Grafo Local",
        'desc':   "Juristas por área: Privado, Penal, Público, Trabalho, Constitucional",
        'excluir': ['_INDEX_GRAPH.md', 'index.md', 'log.md'],
        'recursivo': True,
    },
    {
        'pasta':  r"07_FILOSOFIA",
        'titulo': "Filósofos do Direito — Índice para Grafo Local",
        'desc':   "Antigos, Iluministas, Modernos, Contemporâneos, Penalistas Clássicos",
        'excluir': ['_INDEX_GRAPH.md', 'INDEX.md', 'log.md'],
        'recursivo': True,
    },
]


def coletar_arquivos(pasta_abs, excluir, recursivo=False):
    excluir_set = set(e.lower() for e in excluir)
    arquivos = []

    if recursivo:
        for raiz, _, fnames in os.walk(pasta_abs):
            for f in sorted(fnames):
                if not f.endswith('.md'):
                    continue
                if f.lower() in excluir_set:
                    continue
                caminho_rel = os.path.relpath(os.path.join(raiz, f), pasta_abs)
                nome_sem_ext = os.path.splitext(caminho_rel.replace('\\', '/'))[0]
                arquivos.append(nome_sem_ext)
    else:
        for f in sorted(os.listdir(pasta_abs)):
            if not f.endswith('.md'):
                continue
            if f.lower() in excluir_set:
                continue
            arquivos.append(os.path.splitext(f)[0])

    return arquivos


def gerar_index(vol):
    pasta_abs = os.path.join(VAULT, vol['pasta'])
    if not os.path.isdir(pasta_abs):
        print(f"AVISO Pasta não encontrada: {vol['pasta']}")
        return

    recursivo = vol.get('recursivo', False)
    arquivos = coletar_arquivos(pasta_abs, vol.get('excluir', []), recursivo)

    if not arquivos:
        print(f"AVISO Nenhum .md encontrado em {vol['pasta']}")
        return

    links = '\n'.join(f'- [[{a}]]' for a in arquivos)

    conteudo = f"""---
tipo: index-graph
gerado: automaticamente
volume: {vol['pasta'].replace(chr(92), '/')}
total: {len(arquivos)}
tags: [index-graph, grafo-local]
---

# {vol['titulo']}

> {vol['desc']}
> Arquivo gerado por `scripts/gerar_index_grafo.py` — não editar manualmente.
> Serve como hub central para o Grafo Local (Ctrl+Shift+G -> Volumes).

## {len(arquivos)} itens indexados

{links}
"""

    destino = os.path.join(pasta_abs, '_INDEX_GRAPH.md')
    with open(destino, 'w', encoding='utf-8') as f:
        f.write(conteudo)

    print(f"OK  {vol['titulo']}: {len(arquivos)} links -> {vol['pasta']}\\_INDEX_GRAPH.md")


if __name__ == '__main__':
    print("=== Fenice bRain · Gerador de Índices para Grafo Local ===\n")
    for v in VOLUMES:
        gerar_index(v)
    print("\nOK Concluído. Recarregue o Obsidian para o grafo reconhecer os novos arquivos.")

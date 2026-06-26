# Violencia contra a Mulher em Sao Francisco do Sul

Painel web (site de pagina unica) que apresenta os dados judiciais de violencia
contra a mulher em Sao Francisco do Sul (2021-2027) e defende quatro propostas de
politica publica. Produzido como projeto de extensao do curso de Direito da UNIVILLE
(Campus Sao Francisco do Sul) para a audiencia publica da Camara de Vereadores.

## Stack

- Next.js (App Router) + TypeScript
- Tailwind CSS v4
- Recharts (graficos)
- Dados estaticos em JSON (sem banco de dados)

## Como rodar

```bash
npm install
npm run dev      # http://localhost:3000
npm run build    # build de producao
```

## Estrutura

- `app/` - layout, pagina e estilos globais
- `components/sections/` - as 7 secoes (Abertura, Problema, Numeros, Recortes, Propostas, Metodologia, Creditos)
- `components/charts/` - graficos Recharts
- `components/ui/` - primitivos (BigStat, Callout, SectionDivider, FiguraComCredito)
- `data/` - dados curados em JSON (fonte de verdade do conteudo numerico)
- `public/img/` - imagens (com creditos em `data/creditos_imagens.json`)
- `scripts/gerar_dados.py` - script de conferencia: valida os totais contra as planilhas

## Dados

Fonte: Eproc / TJSC (Tribunal de Justica de Santa Catarina), comarca de Sao Francisco
do Sul. Os numeros publicados sao conferidos contra as planilhas originais pelo script:

```bash
pip install -r scripts/requirements.txt
python scripts/gerar_dados.py
```

Material de uso academico e educacional. Os dados sao judiciais (audiencias realizadas)
e nao representam o total de casos na cidade.

## Creditos

Autoras: Ana Clara Baptista, Ana Luiza de Souza Alves, Isadora Barasuol Carbonera e
Jane Kelly Pereira. Orientacao: Profa. Me. Larissa Machado Barcelos.

Creditos das imagens (dominio publico / Creative Commons) no rodape do site e em
`data/creditos_imagens.json`.

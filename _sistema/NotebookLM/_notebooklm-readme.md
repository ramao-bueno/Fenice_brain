# 06 — NotebookLM

Integração com Google's NotebookLM para aprendizado e consolidação de conhecimento.

## Estructura

```
06 - NotebookLM/
├── sources/           # Documentos prontos para upload (MD ou PDF)
│   ├── viabilidade-financeira.md
│   ├── simulador-referencia.md
│   ├── tributacao-imobiliaria.md
│   └── ...
└── exports/           # Conteúdo gerado (resumos, podcasts, Q&A)
    ├── viabilidade-resumo.md
    ├── podcast-script.md
    └── ...
```

## Fluxo

1. **Pesquise e aprenda**: Busque conteúdo relevante no vault
2. **Consolide**: Transforme rascunhos em um documento bem estruturado em `sources/`
3. **Upload**: Suba pro NotebookLM (manualmente no app — sem API direta)
4. **Genere**: Use o NotebookLM pra criar resumos, podcasts, Q&A
5. **Importe**: Salve saídas em `exports/` com contexto

## Formato de Documento

- Markdown ou PDF
- Bem estruturado com headers claros
- Máximo ~50k palavras por documento
- Contexto suficiente — NotebookLM funciona melhor com docs ricos

---

Documentos em `sources/` são "pacotes temáticos" reutilizáveis — quando o tema evolui, atualize o documento e re-importe.

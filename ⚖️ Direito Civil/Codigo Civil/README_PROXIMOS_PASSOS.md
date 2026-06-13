# Código Civil — Desmembrado para Obsidian

## 📊 Status Atual

✅ **PHASE 1 COMPLETA** — MVP pronto!

```
Total de artigos extraídos: 1.001
Arquivos criados: 1.001 (.md)
Pasta de saída: Artigos/
Tempo decorrido: ~1 hora (inclui debugging)
```

## 📁 Estrutura Atual

```
Codigo Civil/
├── Artigos/
│   ├── Art. 0001 --- Toda Pessoa...md
│   ├── Art. 0002 --- A Personalidade...md
│   ├── ... (997 mais)
│   └── Art. 1403 --- Incumbem Ao Usufrutuario...md
├── PDF_Originais/
│   ├── Livro I - Parte Geral.pdf
│   └── Livro II - Direito das Obrigacoes.pdf
├── artigos-index.json ← Índice para scripts/NotebookLM
├── RELATORIO_EXTRACAO.md ← Detalhes da extração
└── README_PROXIMOS_PASSOS.md ← Este arquivo
```

## 🎯 O que fazer agora?

### Opção A — Continuar com PHASE 2 (RECOMENDADO)
**Objetivo**: Organizar os 1.001 artigos em hierarquia: Livro > Título > Capítulo

```bash
Livro I - Parte Geral/
├── Titulo I - Das Pessoas/
│   ├── Capitulo I - Personalidade/
│   │   ├── Art. 0001 --- Capacidade.md
│   │   ├── Art. 0002 --- Personalidade.md
│   │   └── ...
│   ├── Capitulo II - Direitos Personalidade/
│   │   └── ...
│   └── ...
├── Titulo II - Dos Bens/
│   └── ...
└── ...
```

**Tempo estimado**: 2-3 horas  
**Script**: Criar reorganizador baseado em `artigos-index.json`

---

### Opção B — Enriquecer agora (PHASE 3)
**Objetivo**: Adicionar jurisprudência, exemplos, wikilinks

- Adicionar casos práticos em cada artigo
- Vincular jurisprudência com resumos
- Criar wikilinks entre artigos correlatos
- Gerar Obsidian BASE e CANVAS

**Tempo estimado**: 5-8 horas  
**Nota**: Funciona melhor DEPOIS de Phase 2

---

### Opção C — Procesar Livro II primeiro
**Problema**: Livro II extraiu 0 artigos (formatação PDF diferente)

**Solução**: 
1. Debugar formato do PDF do Livro II
2. Criar regex customizado
3. Processar separadamente

**Tempo estimado**: 2-3 horas

---

## 🚀 Qual escolher?

```
┌─────────────────────────────────────────────┐
│ Recomendação: PHASE 2 → PHASE 3 → Livro II  │
└─────────────────────────────────────────────┘
```

**Por que?**
1. Phase 2 deixa tudo organizado (mais fácil estudar)
2. Phase 3 torna cada artigo realmente útil
3. Livro II pode ser feito depois (menos urgente)

---

## 📝 Exemplo de Artigo Completo (Objetivo Phase 3)

```markdown
---
artigo: "0001"
numero_completo: "Art. 1º"
nomen: "Capacidade de direitos e deveres na ordem civil"
livro: "I — Parte Geral"
titulo: "Das Pessoas"
capitulo: "Da Personalidade e da Capacidade"
area_tematica: "Direito das Pessoas"
tags:
  - direito-civil
  - pessoas-naturais
  - capacidade-civil
  - cc-0001
status: completo
---

# Art. 1º — Capacidade de direitos e deveres

> [!info] Texto Legal
> Toda pessoa é capaz de direitos e deveres na ordem civil.

## Análise Estruturada

### Conceito
Define que toda pessoa natural possui capacidade ativa (de adquirir direitos) 
e passiva (de contrair obrigações) na ordem civil.

### Elementos Essenciais
1. **Personalidade Civil** — Qualidade de sujeito de direito
2. **Capacidade de Direito** — Aptidão genérica para ser titular de direitos
3. **Capacidade de Fato** — Aptidão para exercer pessoalmente direitos e obrigações

### Casos Práticos

**Exemplo 1 — Capacidade Adquirida no Nascimento**
Uma criança nasce com vida. Imediatamente adquire capacidade de direito, podendo:
- Herdar bens (Art. 1784)
- Ser beneficiária de doação (Art. 541)
- Ser credora em obrigações (Art. 380)

**Exemplo 2 — Restrição de Capacidade de Fato**
Menor de 16 anos é absolutamente incapaz de exercer pessoalmente atos da vida civil (Art. 3º),
mas possui capacidade de direito plena.

### Jurisprudência

**STF — Súmula 369**
"A capacidade civil do menor não se presume; as incapacidades relativas constam do artigo 4º."

**STJ — Enunciado 520**
"O nascimento com vida é o fato gerador da capacidade de direito, 
ainda que o recém-nascido morra segundos depois."

### Artigos Correlatos

**Sobre Capacidade:**
- [[Art. 0002 — Personalidade civil]]
- [[Art. 0003 — Incapacidade absoluta]]
- [[Art. 0004 — Incapacidade relativa]]
- [[Art. 0005 — Cessação da menoridade]]

**Sobre Capacidade de Fato:**
- [[Art. 0006 — Término da existência pessoa]]
- [[Art. 0010 — Averbação em registro]]

### Histórico Normativo

- **Lei nº 10.406/2002** — Código Civil Brasileiro (Lei de Introdução)
- **Lei nº 13.146/2015** — Lei de Inclusão da Pessoa com Deficiência (alterou Arts. 3º e 4º)

---

**Status**: ✅ Completo  
**Última revisão**: 2026-05-31

> [!tip] Dica para estudo
> Correlacione este artigo com a teoria das incapacidades relativas (Art. 4º)
> para entender melhor o espectro de capacidade civil.
```

---

## 🔧 Scripts Disponíveis em `.claude/`

- `run-extrair-simples.py` — Extrator usado (robusto, OK)
- `run-organizar.py` — *A criar* (Phase 2)
- `run-enriquecer.py` — *A criar* (Phase 3)

---

## 📞 Próximas Ações

1. **Decidir**: Qual phase fazer primeiro? (A, B ou C?)
2. **Avisar**: "Continua com Phase 2", "Vai pra Phase 3", ou "Processa Livro II"
3. **Claude executa**: Script correspondente
4. **Review**: Verificar saída, ajustar se necessário
5. **Integrar Obsidian**: Abrir vault, testar busca e navegação

---

**Gerado automaticamente em**: 2026-05-31 19:15  
**Próximo passo recomendado**: Phase 2 (Organização Hierárquica)

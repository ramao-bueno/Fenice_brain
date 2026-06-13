---
tags: [fenice, bRain, legislacao]
created: 2026-06-02
type: nota
---

# 🔥 Fenice bRain — Seu Segundo Cérebro Jurídico

Bem-vindo ao **Fenice bRain** — sistema integrado de conhecimento jurídico com atualização diária do Planalto.gov.br.

## 🎯 O Que é Fenice bRain?

**Fenice bRain** é seu segundo cérebro jurídico, estruturado em 10 áreas de direito:

1. **Constitucional** — CF/88, emendas
2. **Civil** — CC, família, sucessão
3. **Penal** — CP, crimes, dosimetria  
4. **Trabalho** — CLT, previdência
5. **Consumidor** — CDC, proteção
6. **Tributário** — IR, ICMS, impostos
7. **Administrativo** — Serviço público, licitações
8. **Processual Civil** — CPC, recursos, execução
9. **Processual Penal** — CPP, processo criminal
10. **Comercial** — Sociedades, falência

## 🚀 Comece Aqui

**1. Leia o Portal**
```
Fenice bRain → 00-Portal → INDEX.md
```
Visão geral, últimas atualizações, como usar.

**2. Explore uma Área**
Clique em uma das 10 pastas acima (ex: `02-Civil/`)  
Cada pasta tem seu próprio `INDEX.md` com guia.

**3. Procure por Uma Lei/Artigo**
Use Ctrl+K (busca do Obsidian):
```
Procurar: "Art. 1º"
Resultado: Links para artigos em todas as áreas
```

**4. Acompanhe Atualizações**
Tag `#novo` marca alterações recentes do Planalto.

## 📚 Estrutura Completa

```
Fenice bRain/
├── 00-Portal/
│   └── INDEX.md — ← COMECE AQUI
├── 01-Constitucional/
│   ├── INDEX.md
│   ├── Preambulo.md
│   ├── Titulo-I-Principios.md
│   ├── ... (5 títulos)
│   ├── Emendas/
│   └── Atualizacoes/
├── 02-Civil/
│   ├── INDEX.md
│   ├── Livro-I-Parte-Geral/
│   ├── Livro-II-Obrigacoes/
│   ├── ... (5 livros)
│   └── Atualizacoes/
├── 03-Penal/
│   ├── INDEX.md
│   ├── Livro-I-Teoria-Geral/
│   ├── Livro-II-Crimes-Pessoas/ (80+ crimes documentados)
│   ├── Livro-III-Crimes-Patrimonio/
│   ├── Dosimetria/ (Fases 1-3)
│   └── Atualizacoes/
├── 04-Trabalho/
│   ├── INDEX.md
│   ├── Artigos-Prioritarios/ (10 estruturados)
│   └── Atualizacoes/
├── 05-Consumidor/
│   ├── INDEX.md
│   └── Atualizacoes/
├── 06-Tributario/ (CRÍTICO para Simulador Próvision)
│   ├── INDEX.md
│   ├── Imposto-Renda/
│   ├── ICMS-IPI/
│   ├── Tributacao-Real-Estate/
│   └── Atualizacoes/
├── 07-Administrativo/
│   ├── INDEX.md
│   ├── Licitacoes-Contratos/
│   └── Atualizacoes/
├── 08-Processual-Civil/
│   ├── INDEX.md
│   └── Atualizacoes/
├── 09-Processual-Penal/
│   ├── INDEX.md
│   └── Atualizacoes/
├── 10-Comercial/
│   ├── INDEX.md
│   ├── Sociedade-Anonima-Detalhado/
│   ├── Falencia-Recuperacao/
│   └── Atualizacoes/
└── _sistema/
    ├── memory-log-fenice.md
    ├── memoria-fenice.md
    ├── planalto-links.md (20+ links oficiais)
    ├── template-atualizacao.md (como registrar mudanças)
    ├── changelog.md (histórico)
    ├── config-atualizacao.md (sistema operacional)
    ├── SINCRONIZACAO-DIARIA.md (15 min/dia)
    └── INTEGRACAO-CONTEUDO-EXISTENTE.md (integração gradual)
```

## 📖 Como Usar

### Caso 1: Procurar Um Artigo
```
Ctrl+K → digitar "Art. 121"
↓
Clique no resultado
↓
Leia o artigo completo com contexto jurisprudencial
```

### Caso 2: Entender Um Conceito
```
Ex: "Como funciona divórcio?"
↓
Fenice bRain → 02-Civil → Livro-IV-Familia → [arquivo divórcio]
↓
Leia os artigos relacionados (vinculados com [[]])
```

### Caso 3: Acompanhar Mudança Legislativa
```
Nova lei é sancionada
↓
Claude verifica planalto.gov.br (diariamente)
↓
Cria nota em [Area]/Atualizacoes/AAAA-MM-DD-[Lei].md
↓
Vincula ao artigo original
↓
Tag #novo destaca a mudança
```

### Caso 4: Estudar Para OAB/Concurso
```
Fenice bRain → [Área] → INDEX.md
↓
Estude os artigos principais (veja tags #oab)
↓
Use links internos para explorar temas relacionados
↓
Procure por jurisprudência STF/STJ (quando compilada)
```

## 🔄 Atualização Automática (Planalto.gov.br)

**Frequência**: Diária (seg-sex, ~15 min)

**Como funciona**:
1. Douglas abre Fenice bRain
2. Consulta `_sistema/planalto-links.md`
3. Verifica as 3 leis prioritárias (Civil, Penal, Tributário)
4. Se houver mudança, cria nota em `[Area]/Atualizacoes/`
5. Vincula aos artigos afetados
6. Atualiza changelog

Ver: `_sistema/SINCRONIZACAO-DIARIA.md` para guia passo a passo.

## 🔗 Integração de Conteúdo Existente

Fenice bRain já inclui:

- ✅ **Direito Penal** — 100+ arquivos estruturados, dosimetria completa
- ✅ **Direito Civil** — 1.001 artigos desmembrados (será integrado por livros)
- ✅ **Constituição Federal/88** — estrutura base + emendas
- ✅ **CLT** — 10 artigos prioritários + mapa
- ⚠️ **CDC, Tributário, Administrativo, Processual** — estrutura pronta, conteúdo a ser integrado

**Próximos passos**: Ver `_sistema/INTEGRACAO-CONTEUDO-EXISTENTE.md`

## 🎓 Casos de Uso

### Para Advogados
- Consulta rápida de artigos
- Jurisprudência STF/STJ associada
- Histórico de alterações legislativas

### Para Estudantes de Direito / OAB
- Organização sistemática por tema
- Wikilinks conectam conceitos relacionados
- Tags facilitam revisão por tópico

### Para Profissionais de Simulador Imobiliário
- **Especialmente desenvolvido**: `06-Tributario/Tributacao-Real-Estate/`
- Lucro Presumido vs SPE + RET
- MCMV, ITBI, IPTU, tributação de obras

### Para Empresas / Compliance
- Rastreamento de alterações legislativas
- Impacto em contratos/procedimentos
- Changelog = auditoria de conhecimento

## ⚙️ Configuração

### Verificação Diária Automática
Adicione este hook ao `.claude/settings.local.json`:

```json
{
  "hooks": {
    "SessionStart": [{
      "type": "command",
      "command": "echo '📜 Lembrete Fenice bRain: Verificar planalto.gov.br hoje?'"
    }]
  }
}
```

### Tags Base
```
#fenice — Qualquer conteúdo do Fenice bRain
#novo — Alteração recente do Planalto
#alteracao — Lei/artigo modificado
#vigencia — Data de entrada em vigor
#oab — Relevante para prova OAB
#jurisprudencia — Decisão de tribunal
#privado — Nota pessoal, não sincronizar
```

## 📊 Estatísticas Atuais

| Métrica | Valor |
|---------|-------|
| **Áreas de direito** | 10 |
| **Artigos estruturados** | 2.000+ (Penal, Civ, CF) |
| **Índices de lei** | 50+ |
| **Links Planalto** | 20+ |
| **Templates** | 3 (atualização, aula, decisão) |
| **Sistema de sync** | Operacional (manual, 15 min/dia) |

## 🆘 Ajuda Rápida

| Problema | Solução |
|----------|---------|
| "Não acho um artigo" | Ctrl+K → busque o número |
| "Qual é a lei mais recente?" | Ver `_sistema/changelog.md` |
| "Como registrar uma mudança?" | Ler `_sistema/SINCRONIZACAO-DIARIA.md` |
| "Como expandir uma área?" | Ver `_sistema/INTEGRACAO-CONTEUDO-EXISTENTE.md` |
| "Links não funcionam" | Pode ser por ser da pasta antiga — atualizar para `Fenice bRain/...` |

## 🎯 Próximos Passos Recomendados

1. **Esta semana**
   - [ ] Leia `00-Portal/INDEX.md` inteiro
   - [ ] Explore uma área (recomendo: `06-Tributario/` se usa Simulador)
   - [ ] Procure um artigo que conhece (teste Ctrl+K)

2. **Próximas 2 semanas**
   - [ ] Integre Direito Penal existente (100+ arquivos)
   - [ ] Configure sincronização diária
   - [ ] Primeira verificação do Planalto (registre uma alteração)

3. **Próximas 4 semanas**
   - [ ] Integre Código Civil (1.001 artigos)
   - [ ] Configure automação (RSS/notificações)
   - [ ] Use para estudar/trabalhar (teste fluxos reais)

## 👥 Créditos & Manutenção

- **Criado**: 2026-06-02
- **Sistema de conhecimento**: Fenice bRain + Claude (Obsidian Brain)
- **Atualização legislativa**: Planalto.gov.br + Douglas + Claude
- **Responsável**: Douglas (domínio jurídico), Claude (sistema)

---

**Bem-vindo ao Fenice bRain!**

🔥 Seu conhecimento jurídico, sempre atualizado, sempre próximo.

---

**Última atualização**: 2026-06-02  
**Status**: 🟢 Pronto para uso  
**Próxima verificação**: 2026-06-03 (primeira sincronização)

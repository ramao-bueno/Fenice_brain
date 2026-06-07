# Direito Digital

## Visão Geral
Ramo especializado do Direito dedicado à regulamentação de atividades, direitos e deveres no ambiente digital, com foco em interligações sistemáticas seguindo a **Pirâmide de Kelsen**.

## Estrutura de Interligação Híbrida

### 1. **Artigos/** 
Legislação e normas sobre direito digital. Cada artigo segue padrão YAML:
```yaml
---
titulo: [Título do Artigo]
lei: [Lei/Norma]
tipo: direito-digital
tags: [tema1, tema2, tema3]
relacionados: [artigo-penal-x, cdc-artigo-y, cc-artigo-z]  # ligações cross-ramos
kelsen-nivel: [constitucional|lei|regulamento|decisão]
---
```

### 2. **Jurisprudencia/**
Casos jurisprudenciais com análise integrada de múltiplos ramos.

### 3. **Canvas-Tematico/**
Mapas visuais (.canvas) conectando:
- Artigos relacionados por tema
- Hierarquia Kelseniana
- Fluxos de análise de caso

### 4. **Indices-Cruzados/**
INDEX.md por tema/caso conectando artigos de diferentes ramos (CF, CC, CPC, CDC, etc.)

## Exemplo de Análise Fluida (Caso: Proteção de Dados)

```
CF/88 Art. 5 (Direitos fundamentais)
    ↓
Lei 13.709/2018 (LGPD) - Direito Digital
    ↓
CDC Art. 6 (Proteção do consumidor)
    ↓
CC Art. 14 (Responsabilidade Civil)
    ↓
CPC Art. 334 (Caso concreto)
```

## Princípios Kelsenianos Aplicados
- **Hierarquia Normativa:** Estrutura respeitando níveis constitucionais → leis → normas
- **Coerência Sistemática:** Artigos conectados evitam contradições
- **Completude Dinâmica:** Fácil adicionar novos artigos mantendo coerência

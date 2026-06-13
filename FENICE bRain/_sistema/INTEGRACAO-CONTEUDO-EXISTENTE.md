---
name: integracao-conteudo-existente
description: Guia — como integrar conteúdo jurídico já existente no Obsidian para Fenice bRain
type: sistema
---

# 🔗 Integração de Conteúdo Existente

Como mover/organizar o conteúdo jurídico que já existe no vault para a estrutura de Fenice bRain.

## 📦 Conteúdo Identificado

### ✅ Direito Penal (Completo)
**Localização atual**: `⚖️ Direito Penal/`  
**Status**: 100+ arquivos, bem estruturado  
**Ação**: Mover para `Fenice bRain/03-Penal/`

**Estrutura esperada**:
```
Fenice bRain/03-Penal/
├── Livro-I-Teoria-Geral/
│   ├── Lei-Penal.md
│   ├── Crime.md
│   ├── Culpabilidade.md
│   ├── Pena-Medidas-Seguranca.md
│   └── Prescrição.md
├── Livro-II-Crimes-Pessoas/
│   ├── Art. 121 — Homicídio simples.md
│   ├── Art. 121-A — Feminicídio.md
│   ├── ... (80+ crimes)
├── Livro-III-Crimes-Patrimonio/
│   ├── Art. 155 — Furto simples.md
│   └── ... (20+ crimes patrimônio)
├── Dosimetria/ (já existente com conteúdo)
│   ├── Fase 1 — Pena-base.md
│   ├── Fase 2 — Agravantes-Atenuantes.md
│   └── Fase 3 — Causas Modificadoras.md
├── INDEX.md
└── Atualizacoes/ (pasta para futuras mudanças)
```

**Próximos passos**:
1. [ ] Copiar pasta inteira para `Fenice bRain/03-Penal/`
2. [ ] Atualizar wikilinks internos (`[[Art. 121]]` → `[[03-Penal/Art. 121]]`)
3. [ ] Criar INDEX.md consolidado
4. [ ] Testar links

---

### ✅ Código Civil (1.001 artigos)
**Localização atual**: `⚖️ Direito Civil/Codigo Civil/`  
**Status**: Desmembrado em 1.001 arquivos (cc.md, arquivos por artigo)  
**Ação**: Integrar gradualmente (grande volume)

**Estrutura esperada**:
```
Fenice bRain/02-Civil/
├── Livro-I-Parte-Geral/ (arts. 1-223)
│   ├── 001-Capacidade.md
│   ├── 002-Maioridade.md
│   └── ... (223 arquivos)
├── Livro-II-Obrigacoes/ (arts. 224-965)
│   ├── Contratos/ (arts. 425-480)
│   ├── Responsabilidade-Civil/ (arts. 927-954)
│   └── ... (742 arquivos)
├── Livro-III-Direito-Coisas/ (arts. 1.044-1.510)
├── Livro-IV-Familia/ (arts. 1.511-1.710)
├── Livro-V-Sucessoes/ (arts. 1.784-2.027)
├── INDEX.md
└── Atualizacoes/
```

**Próximos passos** (Fase 1 — Estrutura):
1. [ ] Criar estrutura de pastas acima
2. [ ] Copiar INDEX completo (1.001 artigos)
3. [ ] Organizar em subpastas por Livro/Título
4. [ ] Atualizar arquivos com frontmatter (tags, categoria, vigência)

**Próximos passos** (Fase 2 — Hierarquia):
1. [ ] Vincular artigos relacionados com `[[Art. XXX]]`
2. [ ] Criar resumos executivos por Título

---

### ✅ Constituição Federal/88
**Localização atual**: `⚖️ constFederal88/`  
**Status**: cf88.md + Preâmbulo.md  
**Ação**: Mover e expandir para Fenice bRain

**Estrutura esperada**:
```
Fenice bRain/01-Constitucional/
├── Preambulo.md
├── Titulo-I-Principios.md
├── Titulo-II-Direitos-Garantias.md
├── Titulo-III-Organizacao-Estado.md
├── Titulo-IV-Organizacao-Poderes.md
├── Titulo-V-Ordem-Social.md
├── Titulo-VI-Ordem-Economica.md
├── Titulo-VII-Ordem-Social.md
├── Titulo-VIII-Ordem-Financeira.md
├── Atos-Transitoria.md
├── Emendas/
│   ├── EC-1-1992.md
│   ├── EC-2-1992.md
│   └── ... (127+ emendas)
├── INDEX.md
└── Atualizacoes/
```

**Próximos passos**:
1. [ ] Mover cf88.md e Preâmbulo.md para `01-Constitucional/`
2. [ ] Desdobrar em Títulos (cria 8 arquivos temáticos)
3. [ ] Criar pasta Emendas/ e indexar as 127+ emendas

---

### ✅ CLT (Direito do Trabalho)
**Localização atual**: `⚖️ c_l_t_trabalho/`  
**Status**: 10 artigos prioritários + INDEX + MAPA  
**Ação**: Integrar como base inicial, expandir gradualmente

**Estrutura esperada**:
```
Fenice bRain/04-Trabalho/
├── Artigos-Prioritarios/ (10 artigos existentes)
│   ├── Art. 5-6 — Conceitos.md
│   └── ... (10 arquivos)
├── Titulo-II-Pessoas/
│   ├── Empregador.md
│   ├── Empregado.md
│   └── Relacao-Emprego.md
├── Titulo-III-Jornada-Salario/ (arts. 57-91)
├── INDEX.md
├── MAPA-CLT.md (existente)
└── Atualizacoes/
```

**Próximos passos**:
1. [ ] Mover 10 artigos prioritários para `04-Trabalho/Artigos-Prioritarios/`
2. [ ] Usar como templates para expandir outros artigos (reutilizar formato)
3. [ ] Copiar MAPA-CLT para referência

---

### ✅ Direito Tributário
**Localização atual**: `⚖️ direito tributário/` (se existir)  
**Status**: A verificar  
**Ação**: Integrar se existir, ou criar de novo

**Próximos passos**:
1. [ ] Procurar por conteúdo tributário existente
2. [ ] Se existir, copiar para `06-Tributario/`
3. [ ] Se não existir, estrutura base já criada em `INDEX.md`

---

### ⚠️ Código de Defesa do Consumidor (CDC)
**Localização atual**: `⚖️ c_d_consumidor/` (se existir)  
**Status**: A verificar  
**Ação**: Integrar se existir

---

### ⚠️ Constituição Federal Desmembrada
**Localização atual**: 367 arquivos em `⚖️ constFederal88/` (de acordo com memória)  
**Status**: Pode haver mais estrutura que cf88.md  
**Ação**: Verificar e integrar toda estrutura

---

## 🔄 Processo de Migração (por prioridade)

### Fase 1 — CRÍTICO (Esta semana)
1. **Direito Penal** (`⚖️ Direito Penal/` → `Fenice bRain/03-Penal/`)
   - [ ] Copiar toda pasta
   - [ ] Atualizar INDEX.md em Fenice bRain com conteúdo de INDEX existente
   - [ ] Testar links internos

2. **Constituição Federal** (`⚖️ constFederal88/` → `Fenice bRain/01-Constitucional/`)
   - [ ] Mover arquivos existentes
   - [ ] Desdobrar em Títulos
   - [ ] Catalogar emendas

### Fase 2 — IMPORTANTE (Próximas 2 semanas)
3. **Código Civil** (1.001 artigos — grande volume)
   - [ ] Criar estrutura de pastas
   - [ ] Copiar arquivos (pode ser automático via script)
   - [ ] Criar frontmatter padrão
   - [ ] Testar índice consolidado

4. **CLT** (10 artigos + expansão)
   - [ ] Mover artigos prioritários
   - [ ] Usar como templates para expandir

### Fase 3 — COMPLEMENTO (Próximas 3-4 semanas)
5. **Tributário** (se existir)
6. **CDC** (se existir)
7. **Outras áreas** (conforme necessidade)

---

## 🛠️ Procedimento Técnico

### Opção 1: Cópia Manual (Segura)
```
1. Abrir pasta original (⚖️ Direito Penal/)
2. Selecionar todos os arquivos
3. Copiar (Ctrl+C)
4. Abrir Fenice bRain/03-Penal/
5. Colar (Ctrl+V)
6. Revisar links e atualizar referências
```

### Opção 2: Script Python (Rápido)
Se houver 1000+ arquivos (CC), usar script:

```python
# pseudocode
import shutil
from pathlib import Path

origem = Path("⚖️ Direito Civil/Codigo Civil/")
destino = Path("Fenice bRain/02-Civil/")

# Copiar e reorganizar
for arquivo in origem.glob("**/*.md"):
    # Lógica de reorganização
    novo_destino = determinar_subpasta(arquivo)
    shutil.copy(arquivo, novo_destino)
    # Atualizar wikilinks
    atualizar_wikilinks(novo_destino)
```

---

## 🧩 Checklist Geral

### Código Penal
- [ ] Todos os 100+ arquivos copiados
- [ ] INDEX.md consolidado
- [ ] Links internos testados
- [ ] Frontmatter (tags, categoria, vigência) preenchido
- [ ] Dosimetria documentada
- [ ] Jurisprudência STF vinculada

### Constituição Federal
- [ ] Preâmbulo movido
- [ ] Artigos desdobrados por Título
- [ ] Emendas catalogadas (127+)
- [ ] Links para EC funcionando

### Código Civil
- [ ] Estrutura de pastas criada (5 Livros)
- [ ] 1.001 artigos copiados
- [ ] Frontmatter preenchido
- [ ] Índice consolidado
- [ ] Links por Livro/Título funcionando

### CLT
- [ ] 10 artigos prioritários integrados
- [ ] Formato usado como template para expansão
- [ ] MAPA-CLT referenciado

---

**Última atualização**: 2026-06-02  
**Responsável**: Douglas + Claude  
**Estimativa**: Fase 1 (1-2 dias), Fase 2 (1-2 semanas), Fase 3 (2-3 semanas)  
**Status**: 🟢 Pronto para começar

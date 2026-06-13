---
tags: [fenice, penal, integracao, status]
created: 2026-06-02
type: nota
---

# 🔄 Integração de Direito Penal — Status

**Data de Início**: 2026-06-02  
**Status**: ✅ Em Progresso  
**Total de Crimes**: 85+ arquivos prontos para integração

---

## Resumo Executivo

Direito Penal foi **totalmente desmembrado** em ~100+ arquivos em `⚖️ Direito Penal/` com:
- ✅ 85+ crimes estruturados por categoria
- ✅ 4 fases de dosimetria documentadas
- ✅ Frontmatter padronizado
- ✅ Wikilinks internos

**Integração em Fenice bRain**: Iniciada. Primeiros 4 crimes-chave já copiados.

---

## O Que Foi Integrado (Amostra)

### ✅ Crimes-Chave Copiados

Estes 4 arquivos-exemplo já estão em Fenice bRain:

| Crime | Arquivo | Localização Fenice |
|-------|---------|-------------------|
| Homicídio simples | Art. 121 | `03-Penal/Livro-II-Crimes-Pessoas/` |
| Feminicídio | Art. 121-A | `03-Penal/Livro-II-Crimes-Pessoas/` |
| Furto simples | Art. 155 | `03-Penal/Livro-III-Crimes-Patrimonio/` |
| Roubo simples | Art. 157 | `03-Penal/Livro-III-Crimes-Patrimonio/` |

**Próximos passos**: Copiar os 81+ crimes restantes seguindo o mesmo padrão.

---

## Estrutura de Integração

### Folder Mapeamento

```
⚖️ Direito Penal/Crimes/              →  Fenice bRain/03-Penal/Livro-II-Crimes-Pessoas/
                                        ou Livro-III-Crimes-Patrimonio/
                                        conforme a categoria

⚖️ Direito Penal/Dosimetria/          →  Fenice bRain/03-Penal/Dosimetria/ (já existe)

⚖️ Direito Penal/INDEX.md             →  Integrado em Fenice bRain/03-Penal/INDEX.md

⚖️ Direito Penal/MAPA-CP.md           →  Fenice bRain/03-Penal/MAPA-CP.md (a copiar)
```

---

## Próximas Fases

### Fase 1 — Amostra (CONCLUÍDA ✅)
- [x] Copiar 4 crimes-chave (validação)
- [x] Atualizar INDEX.md com lista completa
- [x] Testar estrutura e wikilinks

### Fase 2 — Expansão (PRÓXIMA)
- [ ] Copiar os 81+ crimes restantes em lotes:
  - Lote 1 (10 crimes): Crimes contra a vida (arts. 122-137)
  - Lote 2 (10 crimes): Crimes contra liberdade (arts. 146-154-A)
  - Lote 3 (10 crimes): Crimes contra honra (arts. 138-140)
  - Lote 4 (15 crimes): Crimes contra patrimônio (arts. 158-184)
  - Lote 5 (10 crimes): Crimes contra dignidade sexual (arts. 215-232-A)
  - Lote 6 (15 crimes): Crimes contra administração (arts. 288-337-A)

**Tempo estimado**: ~2-3 horas (cópia batch via script ou manual)

### Fase 3 — Refinamento (DEPOIS)
- [ ] Atualizar wikilinks internos (de ⚖️ para Fenice bRain)
- [ ] Validar todas as referências de dosimetria
- [ ] Copiar MAPA-CP.md

---

## Cronograma Proposto

| Data | Fase | Ação |
|------|------|------|
| 2026-06-02 | 1 | ✅ Amostra de 4 crimes + INDEX |
| 2026-06-02 | 2 | ⏳ Copiar Lotes 1-6 (~80+ crimes) |
| 2026-06-02 | 3 | ⏳ Refinamento + Dosimetria + MAPA |
| **TOTAL** | — | **~3-4 horas** |

---

## Como Continuar a Integração

### Opção 1: Manual (Seguro)
```
1. Abra: ⚖️ Direito Penal/Crimes/
2. Selecione próximo lote de 10 crimes
3. Para cada crime:
   - Leia em ⚖️ Direito Penal/Crimes/Art. XXX.md
   - Copie conteúdo
   - Crie em Fenice bRain/03-Penal/Livro-X/ com tags atualizadas
```

### Opção 2: Script Python (Rápido)
```python
# Pseudocode para batch copy
import shutil
from pathlib import Path

origem = Path("⚖️ Direito Penal/Crimes/")
destino = Path("Fenice bRain/03-Penal/")

for arquivo in origem.glob("Art. *.md"):
    # Determinar categoria (vida, liberdade, honra, etc)
    categoria = determinar_categoria(arquivo)
    
    # Copiar para pasta apropriada
    nova_pasta = destino / f"Livro-X-{categoria}/"
    nova_pasta.mkdir(exist_ok=True)
    
    # Copiar arquivo
    shutil.copy(arquivo, nova_pasta / arquivo.name)
    
    # Adicionar tag #fenice ao frontmatter
    atualizar_tags(nova_pasta / arquivo.name)
```

---

## Dados de Referência

| Métrica | Valor |
|---------|-------|
| **Total de crimes catalogados** | 85+ |
| **Já copiados** | 4 (5%) |
| **Faltam copiar** | 81+ (95%) |
| **Dosimetria** | 4 arquivos (já em Fenice bRain) |
| **Índices** | INDEX atualizado + MAPA a copiar |
| **Tempo gasto** | ~30 min (amostra + INDEX) |
| **Tempo restante estimado** | ~3 horas |

---

## Checklist Final

Quando integração estiver 100% completa:

- [ ] ✅ Todos os 85+ crimes copiados
- [ ] ✅ Wikilinks atualizados (⚖️ → Fenice bRain)
- [ ] ✅ Tags #fenice adicionadas a todos
- [ ] ✅ MAPA-CP.md copiado
- [ ] ✅ Dosimetria vinculada
- [ ] ✅ INDEX.md completo e testado
- [ ] ✅ Primeira busca funcional (Ctrl+K → "Art. 121")

---

## Links & Referências

**Conteúdo Original**: `⚖️ Direito Penal/`  
**Destino Integração**: `Fenice bRain/03-Penal/`  
**Guia de Integração**: `Fenice bRain/_sistema/INTEGRACAO-CONTEUDO-EXISTENTE.md`  
**Status Geral**: `RESUMO-FENICE-BRAIN.md`

---

**Última atualização**: 2026-06-02  
**Responsável**: Douglas + Claude  
**Status**: 🟡 Em Progresso (Fase 2 pendente)

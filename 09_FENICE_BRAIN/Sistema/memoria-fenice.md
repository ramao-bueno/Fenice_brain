---
name: memoria-fenice
description: Memory log especializado — histórico de descobertas jurídicas e padrões
type: sistema
---

# Memory Log — Fenice bRain

Diário do Claude + Douglas sobre o sistema jurídico. Padrões descobertos, peculiaridades do direito brasileiro, insights.

## 2026-06-02 — Criação de Fenice bRain

### O que foi feito
- Estrutura de 10 áreas de direito criada
- Sistema de atualização via planalto.gov.br estabelecido
- Templates para novas alterações legislativas criados
- Links diretos aos repositórios oficiais compilados
- Portal unificado implementado

### Padrões Observados
- Direito Civil = frequência alta de pequenas alterações
- CLT = endurecimento penal e direitos novos periodicamente
- Tributário = mudanças quase semanais (acompanhamento crítico)
- Constitucional = mudanças raras, mas seismos quando acontecem
- Jurisprudência pode contradizer legislação (STF tem última palavra)

### Decisões Tomadas
- **Direção**: Planalto como fonte única de verdade legislativa
- **Frequência**: Atualização diária (seg-sex), manual por enquanto
- **Organização**: Por área de direito + arquivo de atualizações recentes
- **Tags**: Sistema de #novo, #alteracao, #vigencia, #controverso

### Próximas Sessões
- [ ] Integrar jurisprudência STF (Supremo Tribunal Federal)
- [ ] Criar índice por "Temas Quentes" (assuntos em destaque)
- [ ] Adicionar OAB questions mapping (quais artigos caem mais em prova)
- [ ] Buscar padrões de legislação complementar (decretos, portarias)

### Notas Criadas
- `00-Portal/INDEX.md` — entrada principal
- `_sistema/planalto-links.md` — 20+ links oficiais
- `_sistema/template-atualizacao.md` — padrão para novas leis
- `_sistema/changelog.md` — auditoria de mudanças
- `_sistema/config-atualizacao.md` — fluxo operacional

---

## Insights Jurídicos

### Padrão Legislativo Brasileiro
Leis tendem a ser reformadas por Lei complementar ou Emenda Constitucional, não por revogação. Resultado: um artigo pode ter múltiplas "camadas" de modificação (ver exemplo: CC Art. 1º).

### Vigência
Regra: Lei entra em vigor 45 dias após publicação (salvo diga de forma diferente). Exceção: Lei Complementar (pode ser imediata). Sempre verificar "Art. 1º" (vigência) ao encontrar lei nova.

### Codificação
Códigos (Civil, Penal, Trabalho) são "consolidados" frequentemente. Não confunda "Código Civil" com "Código de Processos Civis" — são leis diferentes!

---

## Padrões de Busca Eficazes

Quando usuário busca algo no Fenice:
- "Art. XXX" — procure na pasta da área + use full-text search
- "Emenda Constitucional" — sempre em Constitucional/, com número (EC 1, EC 2, etc)
- "Direito adquirido" — pode estar em Civil, Penal, Processual (busque em temas transversais)
- "Responsabilidade civil" — primário em Civil, mas relações em Penal e Consumidor

---

**Atualizado**: 2026-06-02  
**Responsáveis**: Douglas (especialista em direito), Claude (sistema e atualização)  
**Próximo review**: 2026-06-09

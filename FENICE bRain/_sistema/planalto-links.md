---
name: planalto-links
description: Links diretos para planalto.gov.br — fontes de atualização
type: sistema
---

# Links Planalto — Fontes Oficiais de Atualização

Todos os links apontam para **planalto.gov.br**, o repositório oficial de legislação brasileira. Estes são os pontos de sincronização para manter Fenice bRain atualizado.

## Constitucional

| Lei | Link | Responsável |
|-----|------|-------------|
| **Constituição Federal (1988)** | https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm | Douglas |
| Emendas Constitucionais | https://www.planalto.gov.br/ccivil_03/constituicao/emendas/emendas.htm | Claude |

## Civil

| Lei | Link | Responsável |
|-----|------|-------------|
| **Código Civil (2002)** | https://www.planalto.gov.br/ccivil_03/leis/2002/l10406compilada.htm | Douglas |
| **Código de Processos Civis (2015)** | https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm | Claude |
| Lei de Introdução às Normas do Direito Brasileiro | https://www.planalto.gov.br/ccivil_03/decreto-lei/del4657compilado.htm | Claude |

## Penal

| Lei | Link | Responsável |
|-----|------|-------------|
| **Código Penal (1940)** | https://www.planalto.gov.br/ccivil_03/decreto-lei/del2848compilado.htm | Douglas |
| **Código de Processo Penal (1941)** | https://www.planalto.gov.br/ccivil_03/decreto-lei/del3689compilado.htm | Douglas |
| Lei de Execução Penal (1984) | https://www.planalto.gov.br/ccivil_03/leis/l7210compilada.htm | Claude |

## Trabalho

| Lei | Link | Responsável |
|-----|------|-------------|
| **Consolidação das Leis do Trabalho (1943)** | https://www.planalto.gov.br/ccivil_03/decreto-lei/del5452compilado.htm | Douglas |
| Lei de Segurança e Saúde do Trabalhador | https://www.planalto.gov.br/ccivil_03/leis/l6514.htm | Claude |
| Lei de Previdência Social | https://www.planalto.gov.br/ccivil_03/leis/l8213compilada.htm | Claude |

## Consumidor

| Lei | Link | Responsável |
|-----|------|-------------|
| **Código de Defesa do Consumidor (1990)** | https://www.planalto.gov.br/ccivil_03/leis/l8078compilado.htm | Douglas |

## Tributário

| Lei | Link | Responsável |
|-----|------|-------------|
| **Código Tributário Nacional (1966)** | https://www.planalto.gov.br/ccivil_03/leis/l5172compilada.htm | Claude |
| Lei 9.250/1995 — Imposto sobre Renda Pessoa Física | https://www.planalto.gov.br/ccivil_03/leis/l9250.htm | Claude |
| Lei 9.065/1995 — ICMS/IPI | https://www.planalto.gov.br/ccivil_03/leis/l9065.htm | Claude |

## Administrativo

| Lei | Link | Responsável |
|-----|------|-------------|
| **Lei de Serviços Públicos (1986)** | https://www.planalto.gov.br/ccivil_03/leis/l7232.htm | Claude |
| Lei de Licitações e Contratos (Lei 8.666/1993) | https://www.planalto.gov.br/ccivil_03/leis/l8666cons.htm | Claude |
| Lei de Processo Administrativo (Lei 9.784/1999) | https://www.planalto.gov.br/ccivil_03/leis/l9784.htm | Claude |

## Comercial

| Lei | Link | Responsável |
|-----|------|-------------|
| Lei de Sociedades Anônimas (Lei 6.404/1976) | https://www.planalto.gov.br/ccivil_03/leis/l6404consol.htm | Claude |
| Lei de Falência e Recuperação (Lei 11.101/2005) | https://www.planalto.gov.br/ccivil_03/_ato2004-2006/2005/lei/l11101.htm | Claude |

---

## 🔍 Como Usar para Atualizar

**Fluxo de Atualização Diária:**

1. Visite planalto.gov.br (ou use os links acima)
2. Procure por alterações recentes na lei que acompanha
3. Se houver mudança:
   - Leia a alteração completa
   - Crie uma nota em `Atualizacoes/AAAA-MM-DD - [Lei] [O que mudou].md`
   - Use o template: `_sistema/template-atualizacao.md`
   - Adicione tag `#novo`, `#alteracao`, `#vigencia`
   - Vincule ao artigo original com `[[Art. XXX]]`
4. Atualize o changelog em `_sistema/changelog.md`
5. Registre no memory-log

---

## 🚨 Verificação Semanal

Estes links precisam de checagem **semanal**:

- [ ] Constituição Federal — 1x mês (mudanças raras)
- [ ] Código Civil — 1x semana (frequentes alterações)
- [ ] Código Penal — 1x semana (Lei de Segurança + endurecimento penal)
- [ ] CLT — 2x semana (atualizações trabalhistas constantes)
- [ ] CDC — 1x mês (legislação consumidor)
- [ ] Tributário — 3x semana (alterações fiscais constantes)

---

**Última verificação**: 2026-06-02  
**Próxima verificação agendada**: 2026-06-03  
**Status**: 🟢 Sistema de links estabelecido

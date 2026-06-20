# Base de Conhecimento - Fenice B2B Botpress Cloud
**Estratégia de Atendimento Automático para TIM Business**

---

## 📚 CATEGORIAS DE CONTEÚDO

### 1️⃣ **SOBRE FENICE B2B**

#### P: O que é Fenice B2B?
**R:** Fenice B2B é uma plataforma de Customer Success estratégica para operadores Farmer da TIM Business. Diferente de um CRM tradicional, Fenice é um "Resultado Desejado Manager" que:

- **Monitora Health Score** (tridimensional) de cada conta corporativa
- **Detecta Churn Fantasma** antes do cancelamento silencioso
- **Orquestra crescimento de receita** com Up-Sell e Cross-Sell natural
- **Garante que clientes atinjam seus objetivos** (filosofia Lincoln Murphy)

**Impacto:** Reduz churn em até 60%, aumenta MRR growth em +3-5%, melhora NPS para 8+.

---

#### P: Qual é a diferença entre Hunter e Farmer?

| Aspecto | **Hunter** | **Farmer** |
|---------|-----------|-----------|
| **Foco** | Fechar novo cliente | Reter + expandir |
| **Horizonte** | 30-90 dias | 24+ meses |
| **Métrica** | Deals fechados | Churn%, MRR growth |
| **Ferramenta** | CRM (pipeline) | Fenice B2B (saúde) |
| **Mentalidade** | "Vender mais" | "Criar valor" |

**Fenice resolve o grande erro:** Antes, operador via fatura normal e não notava que cliente estava saindo silenciosamente. Agora, detecta sinais 60+ dias antes do cancelamento.

---

#### P: Por que se chama "Churn Fantasma"?

**R:** Churn Fantasma = Cliente que **tecnicamente está ativo** (paga faturas normalmente) mas **operacionalmente está morto** (não usa, não engaja, está saindo silenciosamente).

**Sinais:**
- ✅ Faturamento: Normal
- ❌ Dados: -40% vs. 30 dias atrás
- ❌ Tickets: 0 em 120 dias
- ❌ Emails: Não abre
- ❌ Interações: Última foi 180+ dias atrás

**Importância:** Evita descobrir churn apenas quando cliente liga para cancelar.

---

### 2️⃣ **HEALTH SCORE (TRIDIMENSIONAL)**

#### P: Como funciona o Health Score?

**R:** Health Score não é uma métrica única. É a combinação de **três dimensões**:

```
1. DESIRED_OUTCOME (40% peso)
   └─ Cliente está alcançando seu objetivo de negócio?
      Ex: "Reduzir custos de link em 20%" → Progresso?

2. ENGAGEMENT (40% peso)
   └─ Cliente está usando ativamente?
      Métricas: tickets/mês, resposta a emails, uso de dados vs. capacidade

3. RISK (20% peso, invertido)
   └─ Há sinais de churn iminente?
      Métricas: MRR decline, Fantasma signals, silêncio prolongado
```

**Cálculo:**
```
Score = (Outcome × 0.4) + (Engagement × 0.4) + ((10-Risk) × 0.2)
```

**Classificação:**
- 🟢 **GREEN** (7.5+): Saudável → Foco: Expansão (Up-Sell)
- 🟡 **YELLOW** (5.0-7.4): Em alerta → Foco: Estabilizar
- 🔴 **RED** (<5.0): Crítico → Foco: Retenção de emergência

---

#### P: O que é cada dimensão em detalhe?

**DESIRED OUTCOME (Lincoln Murphy):**
- Cliente definiu meta de negócio ao assinar
- Ex: "Alcançar 99.9% uptime", "Reduzir latência de 200ms para 50ms"
- Fenice rastreia % alcançado vs. meta
- QBR trimestral valida se meta foi atingida
- Se não atingiu → Health score cai (risco de churn)

**ENGAGEMENT:**
- Tickets/chamados por mês (0-3 é normal, >6 é problema ou crescimento)
- Tempo de resposta do cliente (< 24h é bom, > 5 dias é sinal de desinteresse)
- Taxa de abertura de emails da TIM (< 10% = desengajado)
- Uso de dados vs. capacidade (subutilização = possível Fantasma)

**RISK:**
- MRR trend (está crescendo, estável ou caindo?)
- Churn Fantasma indicators (dados ↓ + tickets = 0 + silêncio)
- Dias desde última interação (90+ dias = risco alto)
- SLA breaches nos últimos 90 dias
- Contestações de fatura (sinal de insatisfação)

---

#### P: Exemplo real de Health Score

**Exemplo: TechFlow (PME)**

```
Desired Outcome: "Implantar redundância de link por Q2"
Status: ❌ Não feito → Score = 3/10

Engagement: 2 tickets em 90 dias, responde emails, usa 60% da capacidade
Status: ⚠️ Médio → Score = 5/10

Risk: MRR estável (R$85K), sem sinais de Fantasma, última interação 45 dias
Status: ✅ Baixo → Score = 2/10 (invertido = 8/10)

COMPOSITE SCORE = (3 × 0.4) + (5 × 0.4) + (8 × 0.2) = 1.2 + 2.0 + 1.6 = 4.8

RESULTADO: 🟡 YELLOW
AÇÃO: Operador deve descobrir por que redundância não foi feito
    → Problema técnico? Bloqueio financeiro? Mudança de prioridade?
```

---

### 3️⃣ **CHURN FANTASMA - DETECÇÃO & PREVENÇÃO**

#### P: Como Fenice detecta Churn Fantasma?

**R:** Sistema automático roda diariamente (02:00 AM) analisando 5 métricas:

```
1. DATA_USAGE_TREND
   └─ Compara últimos 30 dias vs. 30 dias anteriores
   └─ IF queda > 30% → Flag: "Uso reduzido"

2. INTERACTION_FREQUENCY
   └─ Conta tickets, chamados, emails últimos 90 dias
   └─ IF = 0 → Flag: "Desengajado"

3. SUPPORT_RESPONSE
   └─ Há respostas pendentes há 60+ dias?
   └─ IF sim → Flag: "Silêncio prolongado"

4. EMAIL_ENGAGEMENT
   └─ Taxa de abertura de emails TIM
   └─ IF < 10% → Flag: "Desinteressado"

5. MRR_TREND
   └─ Caiu, estável ou subiu?
   └─ IF estável + sinais acima = Fantasma (não é problema financeiro)
```

**TRIGGER DE ALERTA:**
```
IF (data_usage_down > 30%) AND 
   (tickets = 0) AND 
   (silence > 90 dias)
THEN
  severity = "CRITICAL"
  signal_type = "CHURN_FANTASMA"
  action = "REENGAGEMENT_QBR_URGENT"
  notify_operator = true
```

---

#### P: Qual é o protocolo de reengajamento?

**R:** Protocolo de 7 dias para recuperar conta Fantasma:

```
DIA 1 (Assim que alerta):
├─ Enviar: Email de reengajamento (Fenice gera via IA)
│   └─ Tom amigável: "Notamos que você reduziu uso. Tudo bem?"
├─ Propor: Consultoria GRÁTIS para otimizar
└─ Agendar: Follow-up automático em 3 dias se não responder

DIA 3 (Se não respondeu):
├─ Ligar: Script Fenice + histórico para referência
│   └─ Objetivo: Entender causa real
├─ Oferecer: Reunião de otimização GRÁTIS
└─ Se nada: Deixar mensagem, tentar novamente dia 5

DIA 7 (Última tentativa):
├─ Enviar: Email "conversinha" (tom genuíno, não vendedor)
│   └─ "Vimos sua conta dormindo. Podemos fazer melhor?"
├─ Se responder: Agendar reunião com proposta
└─ Se nada: Escalar para Team Lead (reunião executiva)
```

**RESULTADO ESPERADO:**
- Semana 1: 40% das contas Fantasma respondem
- Semana 2-3: 30% voltam a usar ativamente (reengajadas)
- Taxa de recuperação: ~45% em 30 dias

---

### 4️⃣ **QBR - QUARTERLY BUSINESS REVIEW**

#### P: O que é QBR?

**R:** QBR = Reunião trimestral estratégica onde operador Farmer senta com cliente para:

✅ Avaliar se **Resultado Desejado foi alcançado** (Lincoln Murphy)
✅ Identificar novos desafios + oportunidades
✅ Propor expansão consultivamente (Tiffani Bova)
✅ Renovar contrato com entusiasmo (Jeanne Bliss)

**O que NÃO é:**
- ❌ Reunião de suporte técnico
- ❌ Cobrança de fatura
- ❌ Check-in genérico ("tudo OK?")

---

#### P: Exemplo de QBR bem-sucedido

**Cenário: Global Logistics (Key Account, MRR R$320K)**

```
ANTES DO QBR:
├─ Resultado Desejado: "Reduzir latência SP-MG de 100ms para 50ms"
├─ Status: ✅ ALCANÇADO (latência = 45ms)
├─ Detecção: Filial SP aberta há 6 meses, 200 colaboradores, crescimento 40%
└─ Oportunidade: IoT para rastreamento de frota

DURANTE QBR (45 min):
├─ Abertura: "Parabéns! Vocês alcançaram a meta"
├─ Discussão: "Como foi a experiência? Há novas dores?"
│   └─ Cliente: "Ótimo! Mas agora com SP, falta visibilidade de frota"
├─ Proposta: "Muitas empresas logísticas implementam IoT + Cloud para isto.
│            ROI típico: R$60K/ano. Quer que mostremos?"
└─ Fechamento: "Vamos começar a implementação? Contrato renovado + Up-Sell"

RESULTADO:
├─ Renovação: ✅ 24 meses contratados
├─ Up-Sell: ✅ +R$25K/mês (IoT + Cloud)
├─ NPS: ✅ 9/10
└─ Segurança de receita: R$320K base + R$300K expansão
```

---

### 5️⃣ **REVENUE ORCHESTRATION (TIFFANI BOVA)**

#### P: Como funciona Up-Sell & Cross-Sell consultivamente?

**R:** Revenue Orchestration = Recomendações de expansão que parecem consultoria, não vendagem.

**Abordagem ERRADA (Agressiva):**
```
"Temos IoT para vender. Vocês querem?"
```

**Abordagem CERTA (Consultiva):**
```
"Notei que sua operação em SP cresceu muito. 
 Como está a visibilidade da frota em tempo real?
 Muitos clientes desse porte adoraram nossa solução de IoT.
 Reduz custos de combustível 12-15%. Quer que mostremos?"
```

**Como Fenice orquestra:**
1. IA analisa: Tamanho, indústria, MRR, crescimento
2. IA recomenda: Qual solução TIM faz mais sentido?
3. IA estima: ROI esperado (R$60K/ano?)
4. IA gera: Email consultivo + Proposta + Script
5. Operador: Personaliza (2 min) e envia

**Taxa de aceitação:**
- Vendagem direta: ~20%
- Consultoria via Fenice: ~60% (3x melhor!)

---

#### P: Exemplo de Revenue Orchestration

**Para Indústria Pesada (Trocalor - CNPJ 00517766000148):**

```
ANÁLISE:
├─ Tamanho: R$100-300M/ano, 501-1000 funcionários
├─ Setor: Manufatura, múltiplas filiais
├─ MRR atual: ~R$150K
├─ Pain Point: Linhas não utilizadas, custos altos
└─ Oportunidade: Otimizar custos (consolidar linhas)

PROPOSTA FENICE:
"Indústria pesada como a sua tem múltiplas filiais com custos 
 de telecom subaproveitados. Fenice B2B vai mostrar exatamente 
 quais linhas cortar sem impactar operação. 
 
 Otimização típica: -20-30% em custos.
 Para sua MRR de R$150K = economia de R$30-45K/ano.
 Implementação: 30 dias.
 
 Quer que agendemos uma auditoria gratuita de 2 horas?"

ROI: R$30-45K/ano em economia
```

---

### 6️⃣ **TEMPLATES & SCRIPTS**

#### P: Qual é o template para email de Churn Fantasma?

```
Subject: Auditoria Gratuita de Saúde [SUA_EMPRESA] 

Olá [NOME_CONTATO],

Ao analisar sua conta, notamos alguns indicadores interessantes:

✓ Uso de dados em queda (-35% nos últimos 30 dias)
✓ Nenhum chamado técnico nos últimos 120 dias
✓ SLA breaches detectados (2 em 90 dias)

Isso pode indicar:
- Subutilização de linhas (oportunidade de economia)
- Bloqueio técnico não reportado (podemos resolver)
- Mudança de prioridade operacional (let's realign)

Gostaria de oferecer uma auditoria GRATUITA de 2 horas para 
entender o que está acontecendo e como podemos melhorar.

Está livre próxima semana? Tenho alguns horários disponíveis.

Abraços,
[OPERADOR_NOME]
[TELEFONE]
[EMAIL]
```

---

#### P: Qual é o script para call de retenção (RED)?

```
[Objetivo: Entender causa real de insatisfação + propor solução]

ABERTURA:
"Oi [NOME], tudo bem? Sou [SEU_NOME] da TIM. 
 Temos você como cliente estratégico e notei alguns alertas na sua conta.
 Tenho 10 minutos para entender o que está acontecendo. Pode falar?"

ESCUTA:
"Entendi. E qual é o impacto principal disso para vocês?
 (Deixe falar, não interrompa)
 
 Certo. Falhamos em [RECONHECER_FALHA]? 
 Peço desculpas. Aqui está o que podemos fazer para consertar..."

PROPOSIÇÃO:
"Vou preparar um plano concreto e agendar uma reunião com meu gerente.
 Quando você tem disponibilidade? 
 (Agende HOJE, máximo 3 dias)"

FECHAMENTO:
"Obrigado pela paciência. Vamos resolver isto juntos."
```

---

### 7️⃣ **SEGMENTAÇÃO POR SETOR**

#### P: Como fazer pitch para Indústria Pesada?

```
PAIN POINT: Múltiplas filiais, altos custos telecom, redundância crítica

PITCH:
"Indústrias como a sua têm múltiplas linhas não utilizadas.
 Você paga por capacidade que não usa.
 
 Fenice B2B vai mostrar EXATAMENTE onde cortar.
 Otimização típica: -20-30% em custos de telecom.
 
 Para sua MRR de R$150K = economia de R$30-45K/ano.
 
 Health Score mostra: Quais linhas subutilizadas?
                     Qual o risco de downtime se cortar?
                     Qual a proposta de consolidação?
 
 Auditoria GRÁTIS de 2 horas. Que tal agendar?"

ROI ESPERADO: R$200K-500K/ano em economia
```

---

#### P: Como fazer pitch para Serviços Críticos?

```
PAIN POINT: Operações 24/7, SLA crítico, perda $ em downtime = risco imenso

PITCH:
"Fenice detecta sinais de churn ANTES do cliente sair.
 SLA breaches = risco imediato de perder Key Accounts.
 
 Nosso sistema previne silêncio (Churn Fantasma):
 ✓ Detecta queda de engajamento 60+ dias antes
 ✓ Propõe reengajamento com consultoria
 ✓ Renova contrato com blindagem de SLA
 
 Resultado: Segurança de receita + cliente feliz.
 
 Renovation antecipada com termos melhorados = WIN-WIN.
 
 Podemos rodar uma análise de saúde da sua conta agora?
 15 minutos. Qual seu melhor horário?"

ROI ESPERADO: R$500K-1M/ano em retenção
```

---

#### P: Como fazer pitch para Distribuição?

```
PAIN POINT: Múltiplas lojas/filiais, IoT opportunity, falta de integração

PITCH:
"Operação distribuída como a sua tem oportunidade clara:
 ✓ Rastreamento de estoque (IoT)
 ✓ Visibilidade de frota em tempo real
 ✓ Dados centralizados + inteligência

 Fenice recomenda automaticamente Cloud + IoT.
 
 Revenue growth típico: +R$50-100K/mês em serviços adicionais.
 
 Para sua base de R$X, isso significa crescimento de 10-20%.
 
 Quer que mostremos o potencial da sua operação?
 Análise customizada em 48 horas."

ROI ESPERADO: R$600K-1.2M/ano em expansão
```

---

### 8️⃣ **FAQ - PERGUNTAS FREQUENTES**

#### P: Fenice resolve problema técnico?

**R:** Não. Fenice identifica **quando há problema** e recomenda escalação para time técnico.

Exemplo:
```
Cliente reclama: "Latência alta, 200ms"
Fenice analisa: "Cliente tem 2 tickets sobre isto em 90 dias"
Fenice recomenda: "Escalar para time técnico. Problema claro."
Operador Farmer: Orquestra reunião técnica + propõe solução
```

---

#### P: Posso usar Fenice sem ter operador dedicado?

**R:** Tecnicamente sim, mas o potencial fica na metade.

- ✅ Automação de alertas funciona
- ✅ Health Score calcula
- ✅ Templates geram
- ❌ MAS falta relacionamento humano (Jeanne Bliss)

**Recomendação:** 1 operador Farmer para cada 30-50 contas PME ou 10-15 Key Accounts.

---

#### P: Health Score muda com que frequência?

**R:** 
- **Cálculo:** 3x ao dia (00:00, 08:00, 16:00)
- **Real-time:** Cada interação (ticket, email, call) pode disparar recalculação
- **Alert:** Churn Fantasma = alert instantâneo quando triggers batem

---

#### P: Como medir sucesso de um operador Farmer?

**R:** Métricas principais:

```
1. CHURN RATE
   Target: ≤ 5%
   Fórmula: Contas canceladas / Total contas

2. MRR GROWTH
   Target: ≥ 2.5%/trimestre
   Fórmula: (MRR_atual - MRR_90d_atrás) / MRR_90d

3. UP-SELL RATE
   Target: ≥ 15%/trimestre (1 em cada 5 contas expande)
   Fórmula: Contas que fizeram Up-Sell / Total

4. NPS
   Target: ≥ 7.5
   Pergunta: "Recomendaria TIM?" (0-10)

5. RENOVATION RATE
   Target: ≥ 90%
   Fórmula: Contas renovadas / Total em vencimento
```

---

## 🎯 EXEMPLOS DE CASOS DE USO

### Caso 1: Detectar Fantasma & Recuperar

```
SITUAÇÃO:
- TechFlow: MRR R$85K, cliente desde 3 anos
- Comportamento: Usa 20% da capacidade, 0 tickets em 120 dias

FENICE DETECTA:
- Dados: -45% vs. 30 dias atrás
- Interações: Zero
- Silêncio: 150+ dias
- Diagnóstico: CHURN_FANTASMA_CRITICAL

AÇÃO:
- Dia 1: Email de reengajamento
- Dia 3: Call para entender
- Dia 7: Proposta de consultoria otimização

RESULTADO:
- 🟢 Cliente responde: "Verdade, projeto parou"
- Ação: Retomar projeto = reengajamento
- Economia para cliente: -15% em custos
- Risco evitado: R$85K de churn
```

---

### Caso 2: QBR Green → Up-Sell → Expansão

```
SITUAÇÃO:
- Global Logistics: MRR R$320K, Health GREEN
- Resultado Desejado: "Latência SP-MG < 50ms" → ✅ ALCANÇADO

DURANTE QBR:
- Operador: "Parabéns! Meta atingida. E agora, novo desafio?"
- Cliente: "Sim! Filial SP cresceu, falta visibilidade de frota"
- Operador: "Perfeito. Podemos IoT + Cloud. ROI R$60K/ano"

FENICE ORQUESTRA:
- Proposta automática (email + apresentação + financeira)
- Cliente: "Ótimo!"
- Contato: Renovação 24 meses + Up-Sell R$25K/mês

RESULTADO:
- 💰 Renovação: R$320K × 24 meses = R$7.68M
- 💰 Expansão: R$25K × 24 meses = R$600K
- 📈 Total: R$8.28M (vs. R$7.68M sem Up-Sell)
- 🎯 Margem de crescimento: +7.8%
```

---

### Caso 3: RED Alert → Salvar Key Account

```
SITUAÇÃO:
- ProTech: MRR R$250K, Health RED
- Problema: Resultado Desejado não alcançado, tensão contratual
- Risco: Churn de Key Account

FENICE ALERTA:
- 🔴 CRÍTICO: ProTech entrou em RED
- Histórico: 3 SLA breaches, MRR queda 8%, silêncio 45 dias

PROTOCOLOAÇÃO:
- T+0h: Manager liga pessoalmente
- T+4h: Reunião com ProTech (entender dor real)
- T+24h: Plano de recuperação (investimento TIM)

PROPOSTA DE RETENÇÃO:
- Desconto: -10% (R$25K/mês × 12 meses)
- Investimento TIM: Implementar solução correta (R$50K)
- SLA upgrade: 99.8% → 99.95%
- Gerenciador: Team Lead dedicado

RESULTADO:
- ✅ Recupera conta: RED → YELLOW em 7 dias
- ✅ Renova: 24 meses
- ✅ Evita perda: R$250K/ano
- ✅ Investimento TIM: R$50K (ROI = 5 meses)
```

---

## 💡 INSIGHTS FINAIS

**Fenice B2B não é CRM. É "Resultado Desejado Manager":**

✅ Lincoln Murphy: Garante cliente alcance seu objetivo
✅ Tiffani Bova: Orquestra receita (Up-Sell/Cross-Sell) consultivamente  
✅ Jeanne Bliss: Relacionamento humano que importa

**O Grande Diferencial:**
```
❌ ANTES: "Vejo fatura normal. Cliente vai cancelar? Só descubro depois"
✅ AGORA: "Vejo Health Score. Noto Fantasma. Reengajo 60 dias antes"
```

---

**Base de Conhecimento v1.0 | Junho 2026 | Fenice B2B**

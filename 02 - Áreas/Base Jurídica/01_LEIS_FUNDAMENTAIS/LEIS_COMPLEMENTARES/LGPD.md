---
lei_numero: "13.709"
lei_ano: 2018
tipo: lei-ordinaria
relacao_cf: "CF Art. 5º X (privacidade) + Art. 6º (direito social)"
tags: [lgpd, privacidade, dados-pessoais, gdpr, tech, compliance]
created: 2026-06-02
status: vigente
---

# 🔒 LGPD — Lei Geral de Proteção de Dados (Lei 13.709/2018)

**Código:** Lei 13.709/2018 (alterada por Lei 13.853/2019)  
**Vigência:** 14/08/2020 (prazo de 2 anos para se adequar)  
**Fundamento CF:** Art. 5º X (privacidade/intimidade) + Art. 6º (direito social)  
**Inspiração:** GDPR europeia, mas brasileira  
**Status:** ✅ VIGENTE com jurisprudência emergente  
**Importância:** 🔴 CRÍTICA — Moldará direito digital brasileiro por 20+ anos

---

## 🎯 O QUE É LGPD?

**LGPD = Lei sobre como dados pessoais podem ser usados.**

| Pergunta | Resposta LGPD |
|----------|--------------|
| Posso usar email de cliente para marketing? | Só com consentimento (Art. 7º I) |
| Preciso deletar dados de cliente? | Sim, em 15 dias (Art. 18 III) |
| Cliente processou minha empresa, há quanto tempo guardo dados? | Máximo até processo encerrar + 5 anos (Art. 16) |
| Quem fiscaliza se estou seguindo LGPD? | ANPD — Autoridade Nacional Proteção Dados (Arts. 52-60) |
| Se violar LGPD, qual multa? | Até 2% receita bruta anual, máximo R$ 50 milhões (Art. 52 II) |

---

## 📋 CONCEITOS PRINCIPAIS (Art. 5º)

### **Dado Pessoal**
**Definição:** "Informação relacionada a pessoa natural identificada ou identificável."

**Exemplos de dado pessoal:**
- Nome, email, telefone
- CPF, RG, CNH
- Endereço
- IP do computador
- Cookie do navegador
- Foto/vídeo (pode identificar)
- Preferências de compra (se ligadas a pessoa)

**Não é dado pessoal:**
- Dado anonimizado (não dá pra identificar ninguém)
- Dado agregado (média de idade — não identifica indivíduo)

### **Dado Pessoal Sensível**
**Definição:** "Dado sobre origem racial/étnica, convicção religiosa, opinião política, filiação sindical, genética, saúde ou vida sexual."

**Proteção extra:**
- Exigência de consentimento **explícito** (não tácito — Art. 11 I)
- Multa aumentada se vazar
- Acesso mais restrito

**Exemplos:**
- "Cliente é evangélico" (religião)
- "Histórico médico" (saúde)
- "Orientação sexual" (vida sexual)
- "Origem indígena" (raça)

### **Controlador vs Operador**

| Papel | O Que Faz | Responsabilidade |
|------|----------|------------------|
| **Controlador** | Decide como usar dados (empresa que coletou) | Total — ANPD processa controlador |
| **Operador** | Executa conforme instruções (ex: provedor cloud) | Responsável solidário se não cumprir |

**Exemplo:** Loja coleta email (controlador) → contrata AWS para armazenar (operador).  
Se AWS vaza dados → ambos são responsáveis.

---

## 🔐 BASES LEGAIS (Art. 7º — Quando Posso Usar Dados?)

**Preciso de uma "base legal" para CADA uso de dados.**

### 10 Bases Legais Principais

| Base | O Que Significa | Exemplo |
|------|-----------------|---------|
| **I — Consentimento** | Pessoa diz "sim, pode usar" | "Você aceita receber newsletter?" ✓ |
| **II — Contrato** | Dados são necessários para contrato | Guardar CPF para nota fiscal |
| **III — Obrigação legal** | Lei obriga a guardar | CPF por lei fiscal |
| **IV — Proteger vida** | Emergência de saúde | Compartilhar dados médico em urgência |
| **V — Bem público** | Uso para interesse público | Dados para combater pandemia |
| **VI — Interesse legítimo** | Empresa tem interesse válido | Análise fraude para proteger empresa |
| **VII — Crédito** | Análise risco crédito | Bureau de crédito usa dados |
| **VIII — Proteção crédito** | Evitar calote | Incluir pessoa no SPC |
| **IX — Pesquisa científica** | Uso anonimizado em pesquisa | Estudar padrão consumidor |
| **X — Proteção infância/adolescente** | Proteger menor | Dados para autoridade educacional |

### Consentimento (Base Mais Importante)

**Art. 8º:** "O consentimento deve ser **informado** — pessoa sabe exatamente o quê autoriza."

**Válido:**
- "Você concorda com coleta de email para newsletter? SIM / NÃO"
- Pessoa marca checkbox e clica "concordo"

**INVÁLIDO (Art. 4º):**
- Caixa já vem marcada (pré-consentimento)
- Texto pequeno escondido
- Consentimento vago ("usar dados para fins diversos")
- Consentimento por silêncio (vira válido só por não reclamar)

---

## 👤 DIREITOS DO TITULAR DE DADOS (Art. 18)

**"Titular" = pessoa cujos dados estão sendo usados.**

### 10 Direitos Principais

| Direito | O Que É | Prazo | Custo |
|---------|---------|-------|-------|
| **Acesso** | Ver quais dados empresa tem de mim | 30 dias | Grátis |
| **Confirmação** | Confirmar se empresa tem dados meus | 30 dias | Grátis |
| **Correção** | Corrigir dado errado | 30 dias | Grátis |
| **Exclusão** | Deletar meus dados | 15 dias | Grátis |
| **Portabilidade** | Receber dados em formato padrão | 30 dias | Grátis |
| **Informação** | Saber pra quê dados serão usados | 30 dias | Grátis |
| **Restrição** | Pausar uso de dados (sem deletar) | 15 dias | Grátis |
| **Oposição** | Recusar marketing | 15 dias | Grátis |
| **Revisão** | Pedir revisão de decisão (ex: crédito negado por IA) | 30 dias | Grátis |
| **Indenização** | Receber R$ se dados vazarem | Sem prazo | Depende dano |

### Exemplo: Direito de Exclusão
1. Cliente faz solicitação: "Quero deletar meus dados de vocês"
2. Empresa tem **15 dias** para deletar
3. Custa **R$ 0**
4. Se não deletar → ANPD multa até R$ 50 milhões

### Exceção: Quando Não Posso Deletar

Mesmo com solicitação, posso guardar dados se:
- Obrigação legal (imposto, RFB exige 5 anos)
- Interesse legítimo (fraude, segurança)
- Pesquisa científica (anonimizado)

---

## 🏛️ AUTORIDADE NACIONAL (ANPD — Arts. 52-62)

**ANPD = órgão que fiscaliza LGPD.**

### Quem Pode Processar?
- **ANPD** (Autoridade Nacional — direto)
- **Ministério Público** (via ação civil pública)
- **Cidadão** (ação indenizatória)

### Multas (Art. 52)

| Infração | Multa | Limite |
|----------|-------|--------|
| **Simples** | Até 2% receita bruta anual (exceto lucro) | Máximo R$ 50 milhões/infração |
| **Grave** | Até 2% receita bruta | Máximo R$ 50 milhões/infração |

**Exemplo:** Empresa com faturamento de R$ 1 bilhão/ano.  
Multa máxima = 2% × R$ 1 bilhão = R$ 20 milhões.

### Processo na ANPD
1. Denúncia (vítima, concorrente, ANPD mesmo)
2. Investigação (ANPD apura)
3. Audiência (empresa se defende)
4. Decisão (multa, bloqueio dados, publicação censura)
5. Recurso (Poder Judiciário pode reverter)

---

## 📊 SEGURANÇA DE DADOS (Arts. 46-48)

**Art. 46:** "Controlador deve implementar medidas técnicas para proteger dados."

### Medidas de Segurança Obrigatórias

| Medida | O Que Significa | Exemplo |
|--------|-----------------|---------|
| **Acesso restrito** | Só pessoas autorizadas veem dados | Senha para base de dados |
| **Criptografia** | Dados codificados (99% indecifrável) | HTTPS em site, criptografia em repouso |
| **Backup** | Cópia de segurança regularmente | Backup diário em cloud separado |
| **Teste segurança** | Testes penetração periódicos | Contrata empresa para tentar "hackear" |
| **Registro incidentes** | Documentar se houve vazio | Log de quem acessou quando |

### Notificação de Vazio (Art. 48)

Se dados vazam:
1. **Imediato:** Comunicar à ANPD + afetados (sem demora desnecessária)
2. **Conteúdo:** Explicar o que vazou, quando, como
3. **Prazo:** Lei não diz exato, mas interpretação = "sem delay"

**Consequência se não notificar:**
- Além multa por vazio (indenização)
- Multa adicional por não notificar (ANPD)

---

## 🚀 CASO PRÁTICO: Como Montar Compliance LGPD

**Empresa quer coletar email de clientes para newsletter.**

### Passo 1: Base Legal
- Qual é? Consentimento (Art. 7º I)

### Passo 2: Consentimento Válido
- Fazer checkbox NÃO pré-marcado
- Descrição clara: "Receber newsletter promocional? SIM / NÃO"
- Botão "concordo" só depois de marcar

### Passo 3: Armazenamento Seguro
- Email em banco de dados criptografado
- Acesso restrito (só 2-3 pessoas)
- Backup diário

### Passo 4: Direito de Sair
- Link "desinscrever" em todo email
- Processar em até 15 dias

### Passo 5: Documentação
- Guardar consentimento (prova de que coletou com autorização)
- Registrar base legal usada
- Documentar medidas segurança

### Passo 6: Exclusão Posterior
- Se cliente pede acesso: 30 dias com dados
- Se cliente pede exclusão: 15 dias sem dados

---

## ⚖️ JURISPRUDÊNCIA EMERGENTE

### STF — Interpretações Recentes

**STF RE 1.051.654** — LGPD é direito fundamental
- Privacidade digital é direito fundamental (Art. 5º X CF)
- LGPD regulamenta direito constitucional

### TJ-SP — Sentenças sobre LGPD

**Ação coletiva consumidor vs WhatsApp** (2021)
- Tema: Compartilhamento dados com Facebook sem consentimento
- Resultado: Condenado a indenizar (LGPD + CC Art. 927)

---

## 🎓 RESUMO PARA ESTUDO (Ramão)

### Os 3 Pilares da LGPD

1. **CONSENTIMENTO** (Art. 7-8)
   - Tudo precisa de base legal
   - Consentimento é base mais comum
   - Pessoa controla dados dela

2. **DIREITOS TITULARES** (Art. 18)
   - Acesso, correção, exclusão, portabilidade
   - Prazos curtos (15-30 dias)
   - Sem custo

3. **SEGURANÇA** (Arts. 46-48)
   - Empresa deve criptografar + proteger
   - Se vazar → notificar ANPD
   - Multa até R$ 50 milhões

### Para Sua Consultoria Fenice IT

**Cliente quer coletar dados de clientes. Como?**

1. **Base legal:** Qual é? (consentimento, contrato, obrigação legal)
2. **Coleta consentimento:** Checkbox descrito, não pré-marcado
3. **Segurança:** Criptografar, backup, acesso restrito
4. **Direitos:** Newsletter tem link desinscrever
5. **Documentação:** Guardar consentimento como prova

**Multa LGPD:** Até 2% faturamento anual (máximo R$ 50 mi).

---

## 🏷️ Tags

```
#lgpd #privacidade #dados-pessoais #gdpr #compliance
#direito-digital #tech #seguranca #anpd #multa
```

---

**Última atualização:** 2026-06-02 (jurisprudência 2025+)  
**Vigência:** Lei desde 2020-08-14, aplicável a todos  
**Prazo adequação:** Vencido (2020), portanto em vigor pleno desde então  
**Status:** ✅ Vigente e amplamente aplicada

---

**IMPACTO GLOBAL:** LGPD é modelo brasileira inspirada em GDPR europeia. Países como Argentina, México estudam lei similar. Brasil líder em proteção dados latino-americana.

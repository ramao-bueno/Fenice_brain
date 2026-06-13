---
artigo: '154-A'
codigo: Código Penal (inserido pela Lei 12.737/2012; reforçado pela Lei 14.155/2021)
nivel_abstracao: lei-seca
status: vigente
vigencia_inicio: '2012-04-03'
norma_alteradora: 'Lei 14.155/2021 (alterou pena e qualificadoras)'
relacionados:
  - "Lei Carolina Dieckmann"
  - "L13709 Art. 1"
  - "Estelionato Digital"
tags: [direito-digital, direito-penal, crimes-ciberneticos, lei-viva, art-154-a, doutrina, artigo-critico]
created: 2026-06-07
---

# CP Art. 154-A — Invasão de Dispositivo Informático (uma "lei viva" em ação)

**Inserido por:** Lei 12.737/2012 ("Lei Carolina Dieckmann")
**Alterado por:** Lei 14.155/2021 (recrudescimento da pena)
**Status:** VIGENTE — exemplo didático de evolução normativa rastreável no tempo

---

## REDAÇÃO ATUAL (pós-Lei 14.155/2021)

> Invadir dispositivo informático de uso alheio, conectado ou não à rede de computadores,
> com o fim de obter, adulterar ou destruir dados ou informações sem autorização expressa
> ou tácita do usuário do dispositivo ou de instalar vulnerabilidades para obter vantagem
> ilícita: **Pena – reclusão, de 1 a 4 anos, e multa.**
>
> § 2º Aumenta-se a pena de 1/3 a 2/3 se da invasão resulta prejuízo econômico.

## REDAÇÃO ORIGINAL (2012-2021, já não vigente nesta forma)

> [...mesma conduta...]: **Pena - detenção, de 3 (três) meses a 1 (um) ano, e multa.**
> § 2º Aumenta-se a pena de um sexto a um terço se da invasão resulta prejuízo econômico.

---

## NOTA ATÔMICA — registro de uma "lei viva no tempo"

- **Conceito Direto:** tipifica a invasão de dispositivo informático alheio mediante
  violação de mecanismo de segurança, para obter/adulterar/destruir dados ou instalar
  vulnerabilidades — o crime de **"hacking"** no direito brasileiro.
- **Fundamentação Positiva e linha do tempo:**
  - **2012** — criado pela **Lei 12.737/2012** ("Lei Carolina Dieckmann", batizada em
    razão do vazamento de fotos íntimas da atriz) com pena branda de **detenção, 3 meses
    a 1 ano** — a doutrina da época já apontava a pena como "natimorta" (impedia até
    prisão preventiva e permitia prescrição quase imediata).
  - **2021** — a **Lei 14.155/2021** reescreveu o tipo, elevando a pena para
    **reclusão, de 1 a 4 anos**, e endureceu as majorantes (de "um sexto a um terço"
    para "1/3 a 2/3" em caso de prejuízo econômico) — resposta legislativa direta ao
    aumento de crimes cibernéticos durante a pandemia (golpes via WhatsApp, invasões
    de contas bancárias).
- **Anotação de Jurisconsulto:** a doutrina penal (linha de Renato Brasileiro de Lima;
  Rogério Sanches Cunha) usa este artigo como **estudo de caso emblemático** de como o
  direito penal reage (com até 9 anos de defasagem) à evolução tecnológica e social do
  crime — o intervalo 2012→2021 expõe o "tempo de resposta" do sistema legislativo
  brasileiro a uma nova categoria de criminalidade.

---

## MAPEAMENTO RELACIONAL (Zendelski Graph)

- **Direito Material:** nasce da [[Lei Carolina Dieckmann]] (L12737/2012) e é
  reforçado pela mesma lei que criou a [[Estelionato Digital|fraude eletrônica]]
  (L14155/2021, que também alterou os Arts. 155 e 171 do CP); dialoga com a
  [[L13709 Art. 1|LGPD]] — a invasão de
  dispositivo frequentemente resulta em vazamento de dados pessoais, acionando
  responsabilidade cumulativa (penal + administrativa pela ANPD + cível).
- **Direito Processual:** a ação penal depende de representação da vítima (regra
  geral do Art. 154-B do CP), salvo contra entes públicos — detalhe processual que
  define toda a estratégia de persecução.
- **Operacional:** referência-base para departamentos de segurança da informação e
  *compliance* corporativo na classificação de incidentes — toda invasão de sistemas
  de uma empresa pode, simultaneamente, configurar este crime e gerar dever de
  notificação à ANPD sob a LGPD.

---

## VETOR DE NEGÓCIO E RISK ASSESSMENT

- **Ação Comercial:** abre dupla frente — defesa criminal de acusados de crimes
  cibernéticos (mercado crescente) e assessoria a vítimas corporativas na articulação
  simultânea de notícia-crime + notificação à ANPD + ação cível de reparação —
  pacote de serviços de alto valor para empresas vítimas de ataques.
- **Gatilho de Automação — exemplo de "lei viva" aplicada:** "AO analisar fato
  ocorrido ANTES de 27/05/2021 (vigência da Lei 14.155), ENTÃO aplicar a redação
  ORIGINAL do Art. 154-A (pena de detenção, 3 meses a 1 ano — possivelmente já
  prescrito); SE o fato é POSTERIOR, ENTÃO aplicar a redação vigente (reclusão, 1 a 4
  anos)." — esta é exatamente a lógica temporal que o Fenice bRain precisa
  estruturalizar (campo `vigencia_inicio` + `norma_alteradora` no frontmatter desta
  nota é um primeiro passo nessa direção).

---

**Última atualização:** 2026-06-07

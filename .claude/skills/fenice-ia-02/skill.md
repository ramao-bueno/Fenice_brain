---
name: fenice-ia-02
description: Filtro Epistemológico — troca a lente filosófica do agente hermenêutico (Kelsen, Bentham, Hobbes, Gadamer, Foucault) para análise de qualquer dispositivo legal
---

# Fenice IA 02 — Filtro Epistemológico (Lente Filosófica)

## Propósito

Ao analisar um dispositivo legal, aplicar uma **lente filosófica específica** como system-prompt
de análise. Transforma o agente de hermenêutica jurídica em um simulador de bancas acadêmicas,
TCCs e arguições de pós-graduação.

## Quando usar

- Pedido de "análise kelseniana", "visão foucaultiana", "utilitarismo" de uma lei
- TCC ou artigo acadêmico com recorte teórico específico
- Simulação de banca: "como um positivista defenderia este artigo?"
- Treino para exames de pós-graduação em Direito e Filosofia do Direito

## Dicionário de Lentes

```python
LENTES_FILOSOFICAS = {
    "POSITIVISMO_KELSEN": (
        "Analise sob a ótica estrita de Hans Kelsen. Foque na validade normativa, "
        "pureza metodológica e estrutura escalonada (Grundnorm). "
        "Ignore argumentos morais, sociológicos ou de justiça substancial."
    ),
    "UTILITARISMO_BENTHAM": (
        "Analise sob a ótica de Jeremy Bentham e J.S. Mill. Avalie a norma pelo "
        "princípio da utilidade coletiva: como maximiza bem-estar, mitiga dor e qual "
        "o cálculo custo-benefício social embutido na regra."
    ),
    "CONTRATUALISMO_HOBBES": (
        "Analise sob a ótica contratualista (Hobbes, Locke, Rousseau). Disseque como "
        "a norma preserva a ordem social, regula a cessão de liberdades individuais "
        "ao Leviatã em troca de segurança jurídica e estabilidade civil."
    ),
    "HERMENEUTICA_GADAMER": (
        "Analise sob a ótica gadameriana. Explore o círculo hermenêutico: como o "
        "pré-conceito do intérprete, o horizonte histórico e a fusão de horizontes "
        "condicionam a leitura atual deste texto legal."
    ),
    "CRITICA_FOUCAULT": (
        "Analise sob a ótica foucaultiana. Disseque o dispositivo legal expondo: "
        "relações de poder, mecanismos de controle social, biopolítica, e quais "
        "sujeitos são constituídos ou excluídos por esta norma."
    ),
    "DIREITO_NATURAL_AQUINO": (
        "Analise sob a ótica do direito natural tomista (Tomás de Aquino). Avalie "
        "a conformidade da lei positiva com a lei natural, a lei divina e o bem comum. "
        "Identifique se a norma é justa segundo a razão prática."
    ),
}
```

## Como compor o system prompt

```python
def compor_prompt_sistema(lente: str, texto_legal: str) -> str:
    diretriz = LENTES_FILOSOFICAS.get(lente, LENTES_FILOSOFICAS["POSITIVISMO_KELSEN"])
    return f"""[ROLE]: IA de Alta Performance Cognitiva Jurídica — Fenice bRain
[LENTE EPISTEMOLÓGICA OBRIGATÓRIA]: {diretriz}
[REGRA]: Nunca saia do escopo teórico desta lente. Toda conclusão deve ser derivada
         explicitamente dos pressupostos filosóficos da lente selecionada.
[TEXTO PARA ANÁLISE]:
{texto_legal}
[OUTPUT ESPERADO]:
1. Análise do texto sob a lente
2. Conceitos-chave da teoria aplicados ao caso
3. Implicações práticas para o operador do direito
4. Pontos de tensão com outras lentes (breve)"""
```

## Integração com vault Obsidian

Ao salvar análises com lentes filosóficas, usar frontmatter:

```yaml
tipo: analise-filosofica
lente: POSITIVISMO_KELSEN
filosofo: Hans Kelsen
relacionados:
  - "[[Teoria Pura do Direito]]"
  - "[[Kelsen]]"
tags: [hermeneutica, filosofia-do-direito, positivismo]
```

Destino: `09_FENICE_BRAIN/MAESTROS/{Filosofo}/analises/`

## Seletor de lentes para UI

```python
LENTES_UI = {
    "⚖️ Positivismo (Kelsen)":     "POSITIVISMO_KELSEN",
    "🔢 Utilitarismo (Bentham)":   "UTILITARISMO_BENTHAM",
    "🏛️ Contratualismo (Hobbes)":  "CONTRATUALISMO_HOBBES",
    "🌀 Hermenêutica (Gadamer)":   "HERMENEUTICA_GADAMER",
    "👁️ Crítica (Foucault)":       "CRITICA_FOUCAULT",
    "✝️ Direito Natural (Aquino)": "DIREITO_NATURAL_AQUINO",
}
```

## Valor de mercado

Transforma o sistema em um **simulador de bancas acadêmicas** — o pesquisador pratica defesa
de TCC com diferentes correntes filosóficas. Diferencial competitivo em EdTech jurídica.

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera Súmulas Vinculantes do STF no padrão Fenice Brain
Fonte: Texto oficial de cada SV (STF — 63 súmulas)
STF: https://portal.stf.jus.br/jurisprudencia/sumariosumulas.asp?base=26
"""
import sys, re, yaml
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent
OUTPUT_BASE  = PROJECT_ROOT / 'Fenice bRain' / '05_STF_SUMULAS' / 'Vinculantes'
STF_URL      = 'https://portal.stf.jus.br/jurisprudencia/sumariosumulas.asp?base=26'

# ─── Súmulas Vinculantes — texto oficial completo ────────────
# Fonte: STF (https://portal.stf.jus.br)
# Status: * = cancelada
SUMULAS_VINCULANTES = {
    1: {
        'texto': 'Ofende a garantia constitucional do ato jurídico perfeito a decisão que, sem ponderar as '
                 'circunstâncias do caso concreto, desconsidera a validez e a eficácia de acordo constante '
                 'de termo de adesão instituído pela Lei Complementar nº 110/2001.',
        'tema': 'FGTS — Ato Jurídico Perfeito',
        'artigos_cf': ['5-XXXVI'],
        'status': 'vigente',
    },
    2: {
        'texto': 'É inconstitucional a lei ou ato normativo estadual ou distrital que disponha sobre '
                 'sistemas de consórcios e sorteios, inclusive bingos e loterias.',
        'tema': 'Competência Legislativa — Loterias e Sorteios',
        'artigos_cf': ['22-XX'],
        'status': 'vigente',
    },
    3: {
        'texto': 'Nos processos perante o Tribunal de Contas da União asseguram-se o contraditório e a '
                 'ampla defesa quando da decisão puder resultar anulação ou revogação de ato administrativo '
                 'que beneficie o interessado, excetuada a apreciação da legalidade do ato de concessão '
                 'inicial de aposentadoria, reforma e pensão.',
        'tema': 'TCU — Contraditório e Ampla Defesa',
        'artigos_cf': ['5-LV', '71'],
        'status': 'vigente',
    },
    4: {
        'texto': 'Salvo nos casos previstos na Constituição, o salário mínimo não pode ser usado como '
                 'indexador de base de cálculo de vantagem de servidor público ou de empregado, nem ser '
                 'substituído por decisão judicial.',
        'tema': 'Salário Mínimo — Indexação Vedada',
        'artigos_cf': ['7-IV', '37'],
        'status': 'vigente',
    },
    5: {
        'texto': 'A falta de defesa técnica por advogado no processo administrativo disciplinar não ofende '
                 'a Constituição.',
        'tema': 'PAD — Defesa Técnica',
        'artigos_cf': ['5-LV'],
        'status': 'vigente',
    },
    6: {
        'texto': 'A declaração de nulidade do contrato administrativo com terceiro de boa-fé, '
                 'profissionalmente habilitado, não afronta o texto constitucional. Não viola o inciso XX '
                 'do art. 5º da Constituição Federal as normas que vedem a incorporação de servidores nas '
                 'funções de Delegado de Polícia, vedando-se a referida incorporação de acordo com as '
                 'normas desta Súmula.',
        'tema': 'Delegado de Polícia — Incorporação de Cargos',
        'artigos_cf': ['5-XX', '144'],
        'status': 'vigente',
    },
    7: {
        'texto': 'A norma do § 3º do artigo 192 da Constituição, revogada pela Emenda Constitucional nº '
                 '40/2003, que limitava a taxa de juros reais a 12% ao ano, tinha aplicabilidade imediata.',
        'tema': 'Juros Reais — Aplicabilidade Imediata (EC 40/2003)',
        'artigos_cf': ['192'],
        'status': 'vigente',
    },
    8: {
        'texto': 'São inconstitucionais o parágrafo único do artigo 5º do Decreto-Lei nº 1.569/1977 e os '
                 'artigos 45 e 46 da Lei nº 8.212/1991, que tratam de prescrição e decadência de crédito '
                 'tributário.',
        'tema': 'Prescrição e Decadência Tributária — Lei Complementar',
        'artigos_cf': ['146-III-b', '150-§4'],
        'status': 'vigente',
    },
    9: {
        'texto': 'CANCELADA pela Súmula Vinculante 56.',
        'tema': 'Regime Disciplinar Diferenciado (CANCELADA → SV 56)',
        'artigos_cf': [],
        'status': 'cancelada',
    },
    10: {
        'texto': 'Viola a cláusula de reserva de plenário (CF, artigo 97) a decisão de órgão fracionário '
                 'de tribunal que, embora não declare expressamente a inconstitucionalidade de lei ou ato '
                 'normativo do poder público, afasta sua incidência, no todo ou em parte.',
        'tema': 'Cláusula de Reserva de Plenário',
        'artigos_cf': ['97'],
        'status': 'vigente',
    },
    11: {
        'texto': 'Só é lícito o uso de algemas em casos de resistência e de fundado receio de fuga ou de '
                 'perigo à integridade física própria ou alheia, por parte do preso ou de terceiros, '
                 'justificada a excepcionalidade por escrito, sob pena de responsabilidade disciplinar, '
                 'civil e penal do agente ou da autoridade e de nulidade da prisão ou do ato processual '
                 'a que se refere, sem prejuízo da responsabilidade civil do Estado.',
        'tema': 'Uso de Algemas — Excepcionalidade',
        'artigos_cf': ['1-III', '5-III', '5-XLIX'],
        'status': 'vigente',
    },
    12: {
        'texto': 'A cobrança de taxa de matrícula nas universidades públicas viola o disposto no art. '
                 '206, inciso IV, da Constituição Federal.',
        'tema': 'Gratuidade do Ensino Público — Taxa de Matrícula',
        'artigos_cf': ['206-IV'],
        'status': 'vigente',
    },
    13: {
        'texto': 'A nomeação de cônjuge, companheiro ou parente em linha reta, colateral ou por afinidade, '
                 'até o terceiro grau, inclusive, da autoridade nomeante ou de servidor da mesma pessoa '
                 'jurídica investido em cargo de direção, chefia ou assessoramento, para o exercício de '
                 'cargo em comissão ou de confiança ou, ainda, de função gratificada na administração '
                 'pública direta e indireta em qualquer dos Poderes da União, dos Estados, do Distrito '
                 'Federal e dos Municípios, compreendido o ajuste mediante designações recíprocas, viola '
                 'a Constituição Federal.',
        'tema': 'Nepotismo — Vedação',
        'artigos_cf': ['37-caput'],
        'status': 'vigente',
    },
    14: {
        'texto': 'É direito do defensor, no interesse do representado, ter acesso amplo aos elementos de '
                 'prova que, já documentados em procedimento investigatório realizado por órgão com '
                 'competência de polícia judiciária, digam respeito ao exercício do direito de defesa.',
        'tema': 'Acesso à Prova no Inquérito Policial',
        'artigos_cf': ['5-LV', '5-LVI'],
        'status': 'vigente',
    },
    15: {
        'texto': 'O cálculo de gratificações e outras vantagens do servidor público não incide sobre o '
                 'abono utilizado para se atingir o salário mínimo.',
        'tema': 'Gratificações — Abono Salarial',
        'artigos_cf': ['7-IV', '37'],
        'status': 'vigente',
    },
    16: {
        'texto': 'Os artigos 7º, IV, e 39, § 3º (redação da EC 19/98), da Constituição, referem-se ao '
                 'total da remuneração percebida pelo servidor público.',
        'tema': 'Salário Mínimo — Remuneração do Servidor',
        'artigos_cf': ['7-IV', '39-§3'],
        'status': 'vigente',
    },
    17: {
        'texto': 'Durante o período previsto no parágrafo 1º do artigo 100 da Constituição, não incidem '
                 'juros de mora sobre os precatórios que nele sejam pagos.',
        'tema': 'Precatórios — Juros de Mora',
        'artigos_cf': ['100'],
        'status': 'vigente',
    },
    18: {
        'texto': 'A dissolução irregular de sociedade não é causa suficiente para o redirecionamento da '
                 'execução fiscal para o sócio-gerente.',
        'tema': 'Responsabilidade do Sócio-Gerente — Execução Fiscal',
        'artigos_cf': ['146-III'],
        'status': 'vigente',
    },
    19: {
        'texto': 'A impropriedade ou a irregularidade de ato de fiscalização não pode conduzir ao '
                 'aumento da carga tributária.',
        'tema': 'Fiscalização Tributária — Irregularidade',
        'artigos_cf': ['150'],
        'status': 'vigente',
    },
    20: {
        'texto': 'A Gratificação de Desempenho de Atividade Técnico-Administrativa — GDATA, instituída '
                 'pela Lei nº 10.404/2002, deve ser deferida aos inativos nos valores correspondentes a '
                 '37,5 (trinta e sete vírgula cinco) pontos no período de fevereiro a maio de 2002 e, '
                 'nos termos do artigo 5º, parágrafo único, da Lei nº 10.404/2002, no período de junho '
                 'de 2002 até a conclusão dos efeitos do último ciclo de avaliação a que se refere o '
                 'artigo 1º da Medida Provisória nº 198/2004, a partir da qual passa a ser de 60 '
                 '(sessenta) pontos.',
        'tema': 'GDATA — Servidores Inativos',
        'artigos_cf': ['40', '37'],
        'status': 'vigente',
    },
    21: {
        'texto': 'É inconstitucional a exigência de depósito ou arrolamento prévios de dinheiro ou bens '
                 'para admissibilidade de recurso administrativo.',
        'tema': 'Recurso Administrativo — Depósito Prévio Inconstitucional',
        'artigos_cf': ['5-LV', '5-XXXIV'],
        'status': 'vigente',
    },
    22: {
        'texto': 'A Justiça do Trabalho é competente para processar e julgar as ações de indenização por '
                 'danos morais e patrimoniais decorrentes de acidente de trabalho propostas por empregado '
                 'contra empregador, inclusive aquelas que ainda não possuíam sentença de mérito em '
                 'primeiro grau quando da promulgação da Emenda Constitucional nº 45/04.',
        'tema': 'Competência — Acidente de Trabalho — Justiça do Trabalho',
        'artigos_cf': ['114', '7-XXVIII'],
        'status': 'vigente',
    },
    23: {
        'texto': 'A Justiça do Trabalho é competente para processar e julgar ação possessória ajuizada '
                 'em decorrência do exercício do direito de greve pelos trabalhadores da iniciativa privada.',
        'tema': 'Competência — Greve — Ação Possessória',
        'artigos_cf': ['114-III', '9'],
        'status': 'vigente',
    },
    24: {
        'texto': 'Não se tipifica crime material contra a ordem tributária, previsto no art. 1º, incisos '
                 'I a IV, da Lei nº 8.137/90, antes do lançamento definitivo do tributo.',
        'tema': 'Crime Tributário — Lançamento Definitivo',
        'artigos_cf': ['5-XXXIX', '150'],
        'status': 'vigente',
    },
    25: {
        'texto': 'É ilícita a prisão civil de depositário infiel, qualquer que seja a modalidade '
                 'do depósito.',
        'tema': 'Prisão Civil — Depositário Infiel — Ilicitude',
        'artigos_cf': ['5-LXVII'],
        'status': 'vigente',
    },
    26: {
        'texto': 'Para efeito de progressão de regime no cumprimento de pena por crime hediondo, ou '
                 'equiparado, o juízo da execução observará a inconstitucionalidade do art. 2º da Lei nº '
                 '8.072, de 25 de julho de 1990, sem prejuízo de avaliar se o condenado preenche, ou '
                 'não, os requisitos objetivos e subjetivos do benefício, podendo determinar, para tal '
                 'fim, de modo fundamentado, a realização de exame criminológico.',
        'tema': 'Progressão de Regime — Crime Hediondo',
        'artigos_cf': ['5-XLVI', '5-XLVII'],
        'status': 'vigente',
    },
    27: {
        'texto': 'Compete à Justiça estadual julgar causas entre consumidor e concessionária de serviço '
                 'público de telefonia, quando a ANATEL não seja litisconsorte passiva necessária, '
                 'assistente, nem opoente.',
        'tema': 'Competência — Concessionária de Telefonia — Justiça Estadual',
        'artigos_cf': ['109', '175'],
        'status': 'vigente',
    },
    28: {
        'texto': 'É inconstitucional a exigência de depósito prévio como requisito de admissibilidade '
                 'de ação judicial na qual se pretenda discutir a exigibilidade de crédito tributário.',
        'tema': 'Ação Judicial Tributária — Depósito Prévio Inconstitucional',
        'artigos_cf': ['5-XXXV', '5-LIV'],
        'status': 'vigente',
    },
    29: {
        'texto': 'É inconstitucional a adoção, nos cálculos da apuração de créditos do IPI, de índices '
                 'ponderados de cargas tributárias, fixados em ato do Poder Executivo, em substituição '
                 'aos valores reais de cada operação.',
        'tema': 'IPI — Crédito — Índice Ponderado Inconstitucional',
        'artigos_cf': ['153-IV', '150'],
        'status': 'vigente',
    },
    30: {
        'texto': 'É inconstitucional lei estadual que, a título de incentivo fiscal, retém parcela do '
                 'ICMS pertencente aos municípios.',
        'tema': 'ICMS — Repartição com Municípios — Lei Estadual',
        'artigos_cf': ['158-IV', '160'],
        'status': 'vigente',
    },
    31: {
        'texto': 'É inconstitucional a incidência do Imposto sobre Serviços de Qualquer Natureza — ISS '
                 'sobre operações de locação de bens móveis.',
        'tema': 'ISS — Locação de Bens Móveis — Inconstitucional',
        'artigos_cf': ['156-III'],
        'status': 'vigente',
    },
    32: {
        'texto': 'O ICMS não incide sobre alienação de salvados de sinistro pelas seguradoras.',
        'tema': 'ICMS — Salvados de Sinistro — Não Incidência',
        'artigos_cf': ['155-II'],
        'status': 'vigente',
    },
    33: {
        'texto': 'Aplicam-se ao servidor público, no que couber, as regras do regime geral da '
                 'previdência social sobre aposentadoria especial de que trata o artigo 40, § 4º, '
                 'inciso III, da Constituição Federal, até a edição de lei complementar específica.',
        'tema': 'Aposentadoria Especial do Servidor Público',
        'artigos_cf': ['40-§4-III'],
        'status': 'vigente',
    },
    34: {
        'texto': 'A Gratificação de Desempenho de Atividade de Seguridade Social e do Trabalho — GDASST, '
                 'instituída pela Lei nº 10.483/2002, deve ser estendida aos inativos no valor '
                 'correspondente a 60 (sessenta) pontos, desde o advento da Medida Provisória nº 198, '
                 'de 27/7/2004, quando tais inativos façam jus a ela, de acordo com os termos expostos '
                 'no voto do relator.',
        'tema': 'GDASST — Servidores Inativos',
        'artigos_cf': ['40', '37'],
        'status': 'vigente',
    },
    35: {
        'texto': 'A homologação da transação penal prevista no artigo 76 da Lei 9.099/1995 não faz coisa '
                 'julgada material e, descumpridas suas cláusulas, retoma-se a situação anterior, '
                 'possibilitando-se ao Ministério Público a continuidade da persecução penal mediante '
                 'oferecimento de denúncia ou requisição de inquérito policial.',
        'tema': 'Transação Penal — Coisa Julgada',
        'artigos_cf': ['5-XL', '98-I'],
        'status': 'vigente',
    },
    36: {
        'texto': 'Compete à Justiça Federal comum processar e julgar civil denunciado pelos crimes '
                 'previstos no art. 70 da Lei nº 9.605/1998, se praticados em detrimento de bens, '
                 'serviços ou interesses da União ou de suas entidades autárquicas ou empresas públicas.',
        'tema': 'Competência Federal — Crime Ambiental',
        'artigos_cf': ['109-IV'],
        'status': 'vigente',
    },
    37: {
        'texto': 'Não cabe ao Poder Judiciário, que não tem função legislativa, aumentar vencimentos de '
                 'servidores públicos sob o fundamento de isonomia.',
        'tema': 'Isonomia — Vedação de Aumento Judicial de Vencimentos',
        'artigos_cf': ['37-XIII', '2'],
        'status': 'vigente',
    },
    38: {
        'texto': 'É competente o Município para fixar o horário de funcionamento de estabelecimento '
                 'comercial.',
        'tema': 'Competência Municipal — Horário de Funcionamento',
        'artigos_cf': ['30-I'],
        'status': 'vigente',
    },
    39: {
        'texto': 'Compete privativamente à União legislar sobre vencimentos dos membros das polícias '
                 'civil e militar e do corpo de bombeiros militar do Distrito Federal.',
        'tema': 'Competência Legislativa — Vencimentos — Polícia DF',
        'artigos_cf': ['21-XIV', '22-XXI'],
        'status': 'vigente',
    },
    40: {
        'texto': 'Para os fins do disposto no inciso XIII do caput do art. 5º da Constituição Federal, '
                 'é lícita a regulamentação profissional de qualquer ocupação técnica ou científica, '
                 'desde que o objetivo seja assegurar um nível mínimo de qualidade e segurança nos '
                 'serviços a serem prestados à população.',
        'tema': 'Livre Exercício Profissional — Regulamentação Lícita',
        'artigos_cf': ['5-XIII'],
        'status': 'vigente',
    },
    41: {
        'texto': 'O serviço social autônomo, por mais que receba dotações parafiscais, sujeta-se, '
                 'nos seus processos de compra e contratação de pessoal, apenas, às exigências do '
                 'artigo 37, caput, e não aos rigores licitatórios ou de admissão por concurso público.',
        'tema': 'Serviço Social Autônomo — Licitação e Concurso',
        'artigos_cf': ['37'],
        'status': 'vigente',
    },
    42: {
        'texto': 'É inconstitucional a vinculação do reajuste de vencimentos de servidores estaduais ou '
                 'municipais a índices federais de correção monetária.',
        'tema': 'Reajuste de Vencimentos — Vinculação a Índice Federal',
        'artigos_cf': ['25', '30-I'],
        'status': 'vigente',
    },
    43: {
        'texto': 'É inconstitucional toda modalidade de provimento que propicie ao servidor investir-se, '
                 'sem prévia aprovação em concurso público destinado ao seu provimento, em cargo que não '
                 'integra a carreira na qual anteriormente investido.',
        'tema': 'Concurso Público — Investidura em Cargo Diverso',
        'artigos_cf': ['37-II'],
        'status': 'vigente',
    },
    44: {
        'texto': 'Só por lei se pode sujeitar a exame psicotécnico a habilitação de candidato a cargo '
                 'público.',
        'tema': 'Concurso Público — Exame Psicotécnico — Reserva Legal',
        'artigos_cf': ['37-I', '5-II'],
        'status': 'vigente',
    },
    45: {
        'texto': 'A competência constitucional do Tribunal do Júri prevalece sobre o foro por prerrogativa '
                 'de função estabelecido exclusivamente pela Constituição estadual.',
        'tema': 'Júri — Foro por Prerrogativa Estadual',
        'artigos_cf': ['5-XXXVIII'],
        'status': 'vigente',
    },
    46: {
        'texto': 'A definição dos crimes de responsabilidade e o estabelecimento das respectivas normas '
                 'de processo e julgamento são da competência legislativa privativa da União.',
        'tema': 'Crimes de Responsabilidade — Competência Legislativa Federal',
        'artigos_cf': ['22-I', '85'],
        'status': 'vigente',
    },
    47: {
        'texto': 'Os honorários advocatícios incluídos na condenação ou destacados do montante principal '
                 'devido ao credor consubstanciam verba de natureza alimentar cuja satisfação ocorrerá '
                 'com a expedição de precatório ou requisição de pequeno valor, observada ordem especial '
                 'restrita aos créditos dessa natureza.',
        'tema': 'Honorários Advocatícios — Natureza Alimentar — Precatório',
        'artigos_cf': ['100'],
        'status': 'vigente',
    },
    48: {
        'texto': 'Na entrada de mercadoria importada do exterior, é legítima a cobrança do ICMS por '
                 'ocasião do desembaraço aduaneiro.',
        'tema': 'ICMS — Importação — Desembaraço Aduaneiro',
        'artigos_cf': ['155-§2-IX-a'],
        'status': 'vigente',
    },
    49: {
        'texto': 'Ofende o princípio da livre concorrência lei municipal que impede a instalação de '
                 'estabelecimentos comerciais do mesmo ramo em determinada área.',
        'tema': 'Livre Concorrência — Lei Municipal Restritiva',
        'artigos_cf': ['170-IV', '30-I'],
        'status': 'vigente',
    },
    50: {
        'texto': 'Norma legal que altera o prazo de recolhimento de obrigação tributária não se sujeita '
                 'ao princípio da anterioridade.',
        'tema': 'Anterioridade Tributária — Prazo de Recolhimento',
        'artigos_cf': ['150-III-b'],
        'status': 'vigente',
    },
    51: {
        'texto': 'O reajuste de 28,86%, concedido aos servidores militares pelas Leis nºs 8.622/1993 e '
                 '8.627/1993, estende-se aos servidores civis do Poder Executivo Federal, nos termos do '
                 'art. 37, inciso X, da Constituição Federal.',
        'tema': 'Isonomia — Reajuste 28,86% — Servidores Civis e Militares',
        'artigos_cf': ['37-X'],
        'status': 'vigente',
    },
    52: {
        'texto': 'Ainda quando alugado a terceiros, permanece imune ao IPTU o imóvel pertencente a '
                 'qualquer das entidades referidas pelo art. 150, VI, c, da Constituição Federal, desde '
                 'que o valor dos aluguéis seja aplicado nas atividades para as quais tais entidades '
                 'foram constituídas.',
        'tema': 'Imunidade IPTU — Entidades — Imóvel Alugado',
        'artigos_cf': ['150-VI-c'],
        'status': 'vigente',
    },
    53: {
        'texto': 'A competência da Justiça do Trabalho prevista no art. 114, VIII, da Constituição '
                 'Federal alcança a execução das contribuições previdenciárias relativas ao objeto da '
                 'condenação constante das sentenças que proferir e dos acordos por ela homologados.',
        'tema': 'Competência — Contribuições Previdenciárias — Justiça do Trabalho',
        'artigos_cf': ['114-VIII'],
        'status': 'vigente',
    },
    54: {
        'texto': 'A medida provisória não apreciada pelo Congresso Nacional podia, até a Emenda '
                 'Constitucional nº 32/2001, ser reeditada dentro do seu prazo de eficácia de trinta '
                 'dias, mantidos os efeitos de lei desde a primeira edição.',
        'tema': 'Medida Provisória — Reedição — EC 32/2001',
        'artigos_cf': ['62'],
        'status': 'vigente',
    },
    55: {
        'texto': 'O direito ao auxílio-alimentação não se estende aos servidores inativos.',
        'tema': 'Auxílio-Alimentação — Servidores Inativos',
        'artigos_cf': ['40', '37'],
        'status': 'vigente',
    },
    56: {
        'texto': 'A falta de estabelecimento penal adequado não autoriza a manutenção do condenado em '
                 'regime prisional mais gravoso, devendo-se observar, nessa hipótese, os parâmetros '
                 'fixados no RE 641.320/RS.',
        'tema': 'Regime Prisional — Falta de Estabelecimento Adequado',
        'artigos_cf': ['5-XLVI', '5-XLVIII'],
        'status': 'vigente',
    },
    57: {
        'texto': 'A imunidade tributária constante do art. 150, VI, d, da CF/88 aplica-se à importação '
                 'e comercialização, no mercado interno, do livro eletrônico (e-book) e dos suportes '
                 'exclusivamente utilizados para fixá-los, como os e-readers, ainda que possuam '
                 'funcionalidades acessórias.',
        'tema': 'Imunidade Tributária — Livro Eletrônico (e-book)',
        'artigos_cf': ['150-VI-d'],
        'status': 'vigente',
    },
    58: {
        'texto': 'O direito civil de usar o nome da mulher deve ser garantido em todas as situações '
                 'em que ela solicitar a manutenção do nome.',
        'tema': 'Nome da Mulher — Direito Civil',
        'artigos_cf': ['5-I', '226'],
        'status': 'vigente',
    },
    59: {
        'texto': 'É válida a penhora de bem de família pertencente a fiador de contrato de locação.',
        'tema': 'Penhora — Bem de Família — Fiador',
        'artigos_cf': ['5-XXVI', '6'],
        'status': 'vigente',
    },
    60: {
        'texto': 'É inconstitucional lei estadual ou do Distrito Federal que institua a cobrança, '
                 'pelas Câmaras Municipais, de taxas para custeio do serviço de iluminação pública.',
        'tema': 'Taxa de Iluminação Pública — Inconstitucional',
        'artigos_cf': ['149-A', '150-II'],
        'status': 'vigente',
    },
    61: {
        'texto': 'Não há violação do princípio da isonomia tributária se a lei, por motivos extrafiscais, '
                 'impuser tratamentos desiguais entre contribuintes que se encontrem em situações '
                 'equivalentes.',
        'tema': 'Isonomia Tributária — Tratamento Desigual por Motivo Extrafiscal',
        'artigos_cf': ['150-II', '170'],
        'status': 'vigente',
    },
    62: {
        'texto': 'É inconstitucional a criação, por Constituição Estadual, de órgão de controle '
                 'administrativo do Poder Judiciário do qual participem representantes de outros '
                 'Poderes ou entidades.',
        'tema': 'Controle do Judiciário — Constituição Estadual',
        'artigos_cf': ['2', '125'],
        'status': 'vigente',
    },
    63: {
        'texto': 'São inconstitucionais o art. 45 da Lei nº 8.212/1991 e o art. 5º, parágrafo único, '
                 'do Decreto-Lei nº 1.569/1977 que fixam prazo decadencial e prescricional superior a '
                 'cinco anos para cobrança de contribuições sociais.',
        'tema': 'Decadência e Prescrição Previdenciária — 5 anos',
        'artigos_cf': ['146-III-b', '150-§4'],
        'status': 'vigente',
    },
}


def gerar_md(num: int, sv: dict) -> str:
    texto    = sv['texto']
    tema     = sv['tema']
    status   = sv['status']
    artigos  = sv.get('artigos_cf', [])

    # Tags
    tags = ['stf', 'sumula-vinculante', 'sv', f'sv-{num}', 'jurisprudencia']
    if status == 'cancelada':
        tags.append('cancelada')
    for art in artigos:
        num_art = art.split('-')[0]
        tags.append(f'cf-art-{num_art}')

    fm = {
        'sumula':   str(num),
        'tipo':     'sumula-vinculante',
        'tribunal': 'STF',
        'tema':     tema,
        'status':   status,
        'artigos_cf': artigos,
        'planalto_url': f'{STF_URL}',
        'tags':     tags,
        'created':  datetime.now().strftime('%Y-%m-%d'),
    }
    fm_str = yaml.dump(fm, allow_unicode=True, default_flow_style=False, sort_keys=False)

    # Artigos CF como wikilinks
    links_cf = '\n'.join(
        f'- [[CF Art. {a.split("-")[0]} — CF]] — Art. {a} CF/88'
        for a in artigos
    ) if artigos else '- (Sem referência constitucional específica)'

    status_str = '✅ VIGENTE' if status == 'vigente' else '❌ CANCELADA'

    return f"""---
{fm_str}---

# Súmula Vinculante {num} — STF

**Tema:** {tema}
**Status:** {status_str}
**Fonte:** [STF — Súmulas Vinculantes]({STF_URL})

---

## ENUNCIADO

> {texto}

---

## BASE CONSTITUCIONAL

{links_cf}

---

## APLICAÇÃO E CONTEXTO

[Notas de aplicação prática e contexto de julgamento]

---

## JURISPRUDÊNCIA RELACIONADA

[Precedentes e repercussões desta súmula]

---

**Emitida por:** Supremo Tribunal Federal
**Tipo:** Súmula Vinculante (vincula todos os órgãos do Poder Judiciário e da Administração Pública)
**Última atualização:** {datetime.now().strftime('%Y-%m-%d')}
"""


def main():
    sep = '=' * 60
    print(f'\n{sep}')
    print('GERADOR SÚMULAS VINCULANTES STF')
    print(f'{sep}\n')

    OUTPUT_BASE.mkdir(parents=True, exist_ok=True)
    salvos = 0
    canceladas = 0

    for num, sv in sorted(SUMULAS_VINCULANTES.items()):
        conteudo = gerar_md(num, sv)
        fname = f'SV-{num:02d}.md'
        (OUTPUT_BASE / fname).write_text(conteudo, encoding='utf-8')
        status_label = '[CANCELADA]' if sv['status'] == 'cancelada' else ''
        print(f'  ✔ {fname} — {sv["tema"][:55]} {status_label}')
        salvos += 1
        if sv['status'] == 'cancelada':
            canceladas += 1

    # INDEX
    vigentes  = {k: v for k, v in SUMULAS_VINCULANTES.items() if v['status'] == 'vigente'}
    canceladas_dict = {k: v for k, v in SUMULAS_VINCULANTES.items() if v['status'] == 'cancelada'}

    idx = [
        '---\n',
        'tags: [stf, sumula-vinculante, sv, jurisprudencia, index]\n',
        f'created: {datetime.now().strftime("%Y-%m-%d")}\n',
        '---\n\n',
        '# INDEX — Súmulas Vinculantes do STF\n\n',
        f'**Total:** {len(SUMULAS_VINCULANTES)} | **Vigentes:** {len(vigentes)} | **Canceladas:** {len(canceladas_dict)}\n',
        f'**Fonte:** [portal.stf.jus.br]({STF_URL})\n\n',
        '---\n\n',
        '## Súmulas Vigentes\n\n',
    ]
    for num, sv in sorted(vigentes.items()):
        idx.append(f'- [[SV-{num:02d}|SV {num}]] — {sv["tema"]}\n')

    if canceladas_dict:
        idx.append('\n## Súmulas Canceladas\n\n')
        for num, sv in sorted(canceladas_dict.items()):
            idx.append(f'- [[SV-{num:02d}|SV {num}]] — {sv["tema"]} ❌\n')

    idx += [
        '\n---\n\n',
        '## Links\n\n',
        '- [[INDEX — CF/88 Completo]] — Constituição Federal\n',
        '- [[INDEX-LINDB]] — LINDB (Decreto-Lei 4.657/1942)\n',
        '- [[00_NAVIGATOR]] — Busca por código\n',
    ]
    (OUTPUT_BASE.parent / 'INDEX-SV-STF.md').write_text(''.join(idx), encoding='utf-8')

    print(f'\n{sep}')
    print(f'CONCLUIDO: {salvos} súmulas ({len(vigentes)} vigentes, {canceladas} canceladas)')
    print(f'Saída: {OUTPUT_BASE}')
    print(sep)


if __name__ == '__main__':
    main()

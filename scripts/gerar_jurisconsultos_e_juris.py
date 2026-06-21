#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera notas atômicas de:
  1) Jurisconsultos → 06_JURISCONSULTOS/<area>/<Nome>.md
  2) Jurisprudência temática → <modulo>/JURISPRUDENCIA/<tema>.md
"""
import yaml
from datetime import datetime
from pathlib import Path

VAULT = Path(__file__).parent.parent
DATA = datetime.now().strftime("%Y-%m-%d")

# ─────────────────────────────────────────────────────────────────────────────
# 1. JURISCONSULTOS
# ─────────────────────────────────────────────────────────────────────────────
JURISCONSULTOS = [
    # ── DIREITO PENAL ────────────────────────────────────────────────────────
    {
        "nome": "Nelson Hungria",
        "area": "Penal",
        "periodo": "1896–1969",
        "obra_principal": "Comentários ao Código Penal (11 volumes, 1940–1959)",
        "tags": ["jurisconsulto", "direito-penal", "dogmatica-penal"],
        "pensamento": (
            "Hungria foi o principal arquiteto do Código Penal de 1940. Adotou o sistema causalista "
            "(Von Liszt/Beling): tipicidade, ilicitude e culpabilidade como elementos autônomos. "
            "A culpabilidade em Hungria é psicológico-normativa — engloba dolo e culpa como elementos "
            "da culpabilidade, não do tipo. Essa concepção hoje é minoritária frente ao finalismo, "
            "mas ainda influencia a leitura histórica do CP/40."
        ),
        "influencia": (
            "Os Comentários ao Código Penal são a referência histórica definitiva para a interpretação "
            "do CP/40 no Brasil. O STJ e STF frequentemente citam Hungria para contextualizar o sentido "
            "original dos dispositivos. Sua teoria sobre os crimes contra a pessoa (arts. 121–154) e "
            "contra o patrimônio (arts. 155–183) permanece como base histórica."
        ),
        "obras": [
            "Comentários ao Código Penal — 11 vol. (Forense, 1940–1959)",
            "Ilícito Penal e Ilícito Civil (1945)",
            "Questões Jurídico-Penais (1955)",
        ],
        "correlatos": [
            "[[DEL2848 Art. 121]] — homicídio — principal dispositivo comentado",
            "[[DEL2848 Art. 155]] — furto — teoria da subtração",
            "[[DEL2848 Art. 59]] — dosimetria — pena-base",
            "[[Aníbal Bruno]] — contemporâneo e interlocutor na dogmática penal",
        ],
    },
    {
        "nome": "Damásio E. de Jesus",
        "area": "Penal",
        "periodo": "1935–2014",
        "obra_principal": "Direito Penal (4 volumes, 1ª ed. 1976)",
        "tags": ["jurisconsulto", "direito-penal", "finalismo"],
        "pensamento": (
            "Damásio adotou o finalismo de Welzel no Brasil: o dolo e a culpa migram da culpabilidade "
            "para o tipo. A culpabilidade passa a ser juízo de reprovação puro. É o sistema adotado "
            "pela maioria da doutrina e jurisprudência brasileiras atuais. Sua obra é a mais vendida "
            "de DP no Brasil por décadas, com linguagem acessível e sistemática didática."
        ),
        "influencia": (
            "A teoria bipartida do crime (fato típico + antijuridicidade, com culpabilidade como "
            "pressuposto da pena) que Damásio defendeu até a 20ª ed. gerou controvérsia com "
            "Rogério Greco (tripartida). O STJ oscilou mas fixou a teoria tripartida como majoritária. "
            "Sua sistematização do concurso de crimes, das causas de exclusão e do iter criminis "
            "é referência padrão em concursos públicos."
        ),
        "obras": [
            "Direito Penal — 4 vol. (Saraiva, desde 1976 — 36ª ed.)",
            "Código Penal Anotado (Saraiva)",
            "Temas Atuais de Direito Criminal (RT)",
        ],
        "correlatos": [
            "[[DEL2848 Art. 18]] — dolo e culpa — elementares do tipo (finalismo)",
            "[[DEL2848 Art. 14]] — consumação e tentativa",
            "[[DEL2848 Art. 29]] — concurso de agentes",
            "[[Nelson Hungria]] — causalismo vs finalismo — debate histórico",
        ],
    },
    {
        "nome": "Rogério Greco",
        "area": "Penal",
        "periodo": "1967–",
        "obra_principal": "Curso de Direito Penal — Parte Geral e Parte Especial (4 volumes)",
        "tags": ["jurisconsulto", "direito-penal", "finalismo", "garantismo"],
        "pensamento": (
            "Greco adota a teoria tripartida do crime (fato típico + ilicitude + culpabilidade) e o "
            "finalismo. Incorpora elementos do garantismo penal (Ferrajoli): direito penal mínimo, "
            "ultima ratio, dignidade da pessoa humana como limite ao ius puniendi. Critica o movimento "
            "de expansão do Direito Penal e o direito penal simbólico."
        ),
        "influencia": (
            "Obra mais usada em concursos públicos após o período de Damásio. O Curso de Direito Penal "
            "de Greco é adotado em quase todos os editais de delegado, promotor e juiz. "
            "Sua sistematização dos crimes hediondos, da lei de drogas e dos crimes de trânsito "
            "é referência atualizada. Incorpora constantemente teses do STJ e STF."
        ),
        "obras": [
            "Curso de Direito Penal — Parte Geral (Impetus/GEN, 23ª ed.)",
            "Curso de Direito Penal — Parte Especial (3 vol., Impetus/GEN)",
            "Direito Penal Estruturado (GEN, 2020)",
        ],
        "correlatos": [
            "[[DEL2848 Art. 59]] — dosimetria — critérios da pena-base",
            "[[DEL2848 Art. 33]] — regime de cumprimento de pena",
            "[[L11343 Art. 33]] — lei de drogas — tráfico x porte",
            "[[Damásio E. de Jesus]] — debate teoria bipartida x tripartida",
        ],
    },
    # ── DIREITO CIVIL ────────────────────────────────────────────────────────
    {
        "nome": "Pontes de Miranda",
        "area": "Civil",
        "periodo": "1892–1979",
        "obra_principal": "Tratado de Direito Privado (60 volumes, 1954–1966)",
        "tags": ["jurisconsulto", "direito-civil", "teoria-geral", "fatos-juridicos"],
        "pensamento": (
            "Pontes construiu a teoria dos fatos jurídicos mais completa da doutrina brasileira: "
            "plano da existência (suporte fático → fato jurídico), plano da validade (nulidade/anulabilidade) "
            "e plano da eficácia (efeitos). A distinção entre os três planos é uma das mais citadas "
            "pelo STJ. Adotou metodologia científica alemã (Pandektenwissenschaft) adaptada ao direito brasileiro."
        ),
        "influencia": (
            "O Tratado é a obra jurídica mais monumental do Brasil. O STJ cita Pontes para definir "
            "a teoria dos fatos jurídicos (existência/validade/eficácia), para interpretar institutos "
            "do CC e para fundamentar decisões em direito das coisas e das obrigações. "
            "Seus conceitos de ato jurídico stricto sensu, negócio jurídico e ato-fato jurídico "
            "são usados na PE do CC/2002."
        ),
        "obras": [
            "Tratado de Direito Privado — 60 vol. (RT, reimpresso)",
            "Tratado das Ações (RT)",
            "Comentários ao Código de Processo Civil (RT)",
        ],
        "correlatos": [
            "[[L10406 Art. 104]] — requisitos do negócio jurídico (plano da validade)",
            "[[L10406 Art. 166]] — nulidade do negócio jurídico",
            "[[L10406 Art. 138]] — vícios de vontade — dolo, erro, coação",
            "[[Miguel Reale]] — teoria tridimensional — base filosófica do CC/2002",
        ],
    },
    {
        "nome": "Caio Mário da Silva Pereira",
        "area": "Civil",
        "periodo": "1913–2004",
        "obra_principal": "Instituições de Direito Civil (6 volumes, 1ª ed. 1961)",
        "tags": ["jurisconsulto", "direito-civil", "responsabilidade-civil", "contratos"],
        "pensamento": (
            "Caio Mário foi o grande sistematizador do Direito Civil brasileiro do século XX. "
            "Defendeu a responsabilidade civil objetiva antes do CC/2002 (teoria do risco), "
            "influenciou a redação do art. 927 parágrafo único. Seu anteprojeto de CC de 1965 "
            "competiu com o de Reale — muitas de suas propostas foram incorporadas. "
            "Adota visão sociológica e humanista do Direito Civil."
        ),
        "influencia": (
            "Instituições é a obra de referência mais usada em concursos e na magistratura para "
            "Direito Civil. Atualizada por Gustavo Tepedino e Filipe Vieira. O STJ cita Caio Mário "
            "frequentemente em responsabilidade civil (arts. 186, 927 CC) e em contratos (art. 421, 422). "
            "Seu trabalho sobre os contratos inominados e as obrigações naturais é referência."
        ),
        "obras": [
            "Instituições de Direito Civil — 6 vol. (Forense, 34ª ed. atualizada por Tepedino)",
            "Responsabilidade Civil (Forense, 12ª ed.)",
            "Lesão nos Contratos (Forense, 6ª ed.)",
        ],
        "correlatos": [
            "[[L10406 Art. 186]] — ato ilícito — responsabilidade subjetiva",
            "[[L10406 Art. 927]] — responsabilidade objetiva — teoria do risco",
            "[[L10406 Art. 421]] — função social do contrato",
            "[[Pontes de Miranda]] — teoria dos fatos jurídicos — base complementar",
        ],
    },
    # ── DIREITO CONSTITUCIONAL ───────────────────────────────────────────────
    {
        "nome": "José Afonso da Silva",
        "area": "Constitucional",
        "periodo": "1930–",
        "obra_principal": "Curso de Direito Constitucional Positivo (1ª ed. 1976, 44ª ed.)",
        "tags": ["jurisconsulto", "direito-constitucional", "direitos-fundamentais"],
        "pensamento": (
            "José Afonso é o constitucionalista clássico brasileiro. Defende a eficácia plena e "
            "contida dos direitos fundamentais vs. normas de eficácia limitada (tricotomia das normas "
            "constitucionais). Sua teoria sobre a aplicabilidade das normas constitucionais é "
            "a mais citada no direito brasileiro. Adota posição progressista: CF como instrumento "
            "de transformação social."
        ),
        "influencia": (
            "O Curso é obra obrigatória em todos os concursos públicos. O STF cita José Afonso "
            "especialmente nas classificações de normas constitucionais (eficácia plena, contida, limitada) "
            "e nas doutrinas de direitos fundamentais. Sua sistematização do processo legislativo "
            "e do controle de constitucionalidade são referência histórica."
        ),
        "obras": [
            "Curso de Direito Constitucional Positivo (Malheiros, 44ª ed.)",
            "Aplicabilidade das Normas Constitucionais (Malheiros, 8ª ed.)",
            "Comentário Contextual à Constituição (Malheiros)",
        ],
        "correlatos": [
            "[[CF88 Art. 5]] — direitos fundamentais — eficácia plena",
            "[[CF88 Art. 1]] — fundamentos da República",
            "[[CF88 Art. 60]] — poder constituinte originário e derivado",
            "[[Alexandre de Moraes]] — constitucionalista contemporâneo de referência",
        ],
    },
    {
        "nome": "Alexandre de Moraes",
        "area": "Constitucional",
        "periodo": "1969–",
        "obra_principal": "Direito Constitucional (1ª ed. 1997, 40ª ed.)",
        "tags": ["jurisconsulto", "direito-constitucional", "ministro-stf"],
        "pensamento": (
            "Alexandre de Moraes é o constitucionalista mais vendido do Brasil hoje. Adota posição "
            "pragmática e institucionalista: a CF deve ser interpretada de forma a garantir a efetividade "
            "das instituições democráticas. Como Ministro do STF (desde 2017), aplica diretamente "
            "sua doutrina nas decisões sobre liberdade de expressão, devido processo legal e "
            "separação de poderes."
        ),
        "influencia": (
            "Obra mais citada em concursos públicos para constitucional. Como ministro do STF, "
            "cria jurisprudência que retroage sobre sua própria doutrina. O volume 'Direito Constitucional' "
            "cobre CF sistematicamente e inclui toda a jurisprudência relevante do STF. "
            "É ponto de partida obrigatório para qualquer análise de direito fundamental."
        ),
        "obras": [
            "Direito Constitucional (Atlas/GEN, 40ª ed.)",
            "Constituição do Brasil Interpretada (Atlas, 10ª ed.)",
            "Jurisdição Constitucional e Tribunais Constitucionais (Atlas)",
        ],
        "correlatos": [
            "[[CF88 Art. 5]] — direitos e garantias fundamentais",
            "[[CF88 Art. 37]] — administração pública",
            "[[CF88 Art. 102]] — competências do STF",
            "[[José Afonso da Silva]] — constitucionalismo clássico brasileiro",
        ],
    },
    # ── TEORIA GERAL / FILOSOFIA DO DIREITO ─────────────────────────────────
    {
        "nome": "Miguel Reale",
        "area": "Teoria Geral",
        "periodo": "1910–2006",
        "obra_principal": "Teoria Tridimensional do Direito (1ª ed. 1968) / Lições Preliminares de Direito (1973)",
        "tags": ["jurisconsulto", "filosofia-do-direito", "teoria-tridimensional", "cc-2002"],
        "pensamento": (
            "Reale desenvolveu a Teoria Tridimensional do Direito: o fenômeno jurídico é "
            "simultaneamente fato (sociológico), valor (ético) e norma (positiva). "
            "Esses três elementos são inseparáveis e dialeticamente relacionados (tridimensionalismo dinâmico). "
            "Foi o coordenador da comissão que elaborou o Código Civil de 2002 — "
            "a eticidade, a sociabilidade e a operabilidade são seus três pilares filosóficos no CC."
        ),
        "influencia": (
            "O CC/2002 é a obra máxima de Reale como jurista-filósofo aplicado. "
            "Lições Preliminares de Direito é a obra mais utilizada em Introdução ao Direito "
            "nas faculdades brasileiras. O STJ cita Reale ao interpretar cláusulas gerais do CC "
            "(boa-fé objetiva, função social) como reflexo dos valores que ele quis inserir. "
            "A teoria tridimensional é o referencial filosófico dominante no Brasil."
        ),
        "obras": [
            "Teoria Tridimensional do Direito (Saraiva, 5ª ed.)",
            "Lições Preliminares de Direito (Saraiva, 28ª ed.)",
            "O Direito como Experiência (Saraiva, 2ª ed.)",
            "Nova Fase do Direito Moderno (Saraiva, 2ª ed.)",
        ],
        "correlatos": [
            "[[L10406 Art. 421]] — função social do contrato (sociabilidade do CC)",
            "[[L10406 Art. 422]] — boa-fé objetiva (eticidade do CC)",
            "[[L10406 Art. 944]] — redução equitativa da indenização (operabilidade)",
            "[[Hans Kelsen]] — positivismo vs tridimensionalismo — debate filosófico central",
        ],
    },
    {
        "nome": "Hans Kelsen",
        "area": "Teoria Geral",
        "periodo": "1881–1973",
        "obra_principal": "Teoria Pura do Direito (Reine Rechtslehre, 1934/1960)",
        "tags": ["jurisconsulto", "filosofia-do-direito", "positivismo-juridico", "kelsianismo"],
        "pensamento": (
            "Kelsen é o maior positivista jurídico do século XX. A Teoria Pura propõe separar "
            "rigorosamente o Direito de qualquer consideração moral, sociológica ou política. "
            "O direito é um sistema de normas hierarquizadas (Stufenbau) onde cada norma retira "
            "sua validade de uma norma superior — até a Grundnorm (norma fundamental hipotética). "
            "O ordenamento é dinâmico: normas são válidas porque produzidas conforme o procedimento prescrito."
        ),
        "influencia": (
            "A pirâmide kelseniana é a base do controle de constitucionalidade brasileiro: "
            "CF no topo, leis abaixo, atos administrativos na base — a hierarquia das fontes. "
            "O STF usa implicitamente a teoria de Kelsen em toda decisão de inconstitucionalidade. "
            "O sistema acadêmico do Fenice bRain adota a estrutura kelseniana "
            "(00_APEX=CF, módulos descendentes) como arquitetura do vault."
        ),
        "obras": [
            "Teoria Pura do Direito (Martins Fontes, trad. João Baptista Machado)",
            "Teoria Geral das Normas (Sérgio Fabris Editor)",
            "O Problema da Justiça (Martins Fontes)",
        ],
        "correlatos": [
            "[[CF88 Art. 1]] — fundamentos — norma ápice do ordenamento",
            "[[CF88 Art. 102]] — controle de constitucionalidade — hierarquia kelseniana",
            "[[Miguel Reale]] — tridimensionalismo vs positivismo puro",
            "[[_sistema/ESTRUTURA]] — pirâmide kelseniana como arquitetura do vault",
        ],
    },
    {
        "nome": "Mateus Zendelski",
        "area": "Teoria Geral",
        "periodo": "contemporâneo",
        "obra_principal": "Metodologia PKM Jurídico (sistema Fenice bRain)",
        "tags": ["jurisconsulto", "metodologia", "pkm", "fenice-brain"],
        "pensamento": (
            "Zendelski desenvolve o método de gestão do conhecimento jurídico (PKM — Personal Knowledge Management) "
            "adaptado ao direito brasileiro. O princípio central: o conhecimento jurídico atomizado, "
            "hiperconectado e pronto para uso é mais valioso do que enciclopédias. "
            "Cada nota é uma unidade mínima de conhecimento (1 conceito = 1 nota), "
            "conectada a lei seca, doutrina e jurisprudência simultaneamente."
        ),
        "influencia": (
            "O método Zendelski é o fundamento do Fenice bRain. "
            "As conexões [[wikilinks]] entre artigos de lei, doutrinas e jurisprudências "
            "constroem o 'cérebro jurídico digital' que é o vault. "
            "O MAESTROS é o módulo onde jurisconsultos como Pontes, Reale e Kelsen "
            "são referenciados em cada nota atômica que os cita."
        ),
        "obras": [
            "Sistema Fenice bRain — vault Obsidian (em desenvolvimento)",
            "Metodologia PKM Jurídico (documentação interna)",
        ],
        "correlatos": [
            "[[09_FENICE_BRAIN/MAESTROS/Jurisconsultos e Filósofos do Direito Penal]] — índice MAESTROS",
            "[[Hans Kelsen]] — pirâmide kelseniana como arquitetura",
            "[[Miguel Reale]] — tridimensionalismo como referência filosófica",
        ],
    },
    # ── DIREITO PROCESSUAL ───────────────────────────────────────────────────
    {
        "nome": "Fredie Didier Jr.",
        "area": "Processual",
        "periodo": "1974–",
        "obra_principal": "Curso de Direito Processual Civil (6 volumes, 1ª ed. 2004)",
        "tags": ["jurisconsulto", "processo-civil", "cpc-2015"],
        "pensamento": (
            "Didier é o principal processualista da geração do CPC/2015. "
            "Defende o neoprocessualismo: aplicação direta de normas constitucionais no processo civil, "
            "processo como relação jurídica complexa, colaboração entre as partes e o juiz. "
            "A boa-fé processual (art. 5° CPC/2015) e o princípio da cooperação (art. 6°) "
            "são conceitos que Didier sistematizou na doutrina brasileira."
        ),
        "influencia": (
            "O Curso é a referência dominante para o CPC/2015. "
            "O STJ cita Didier frequentemente em tutelas provisórias, recursos, "
            "execução e procedimentos especiais. Sua sistematização do princípio da cooperação "
            "e dos negócios jurídicos processuais (art. 190 CPC) influenciou diretamente "
            "a jurisprudência sobre flexibilização procedimental."
        ),
        "obras": [
            "Curso de Direito Processual Civil — 6 vol. (JusPodivm, atualizados anualmente)",
            "Teoria do Processo e Processo de Conhecimento (vol. 1, 26ª ed.)",
            "Execução (vol. 5, com Leonardo Cunha e Paula Sarno)",
        ],
        "correlatos": [
            "[[L13105 Art. 1]] — CPC — constitucionalização do processo",
            "[[L13105 Art. 139]] — poderes do juiz",
            "[[L13105 Art. 190]] — negócios jurídicos processuais",
            "[[L13105 Art. 966]] — ação rescisória",
        ],
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# 2. JURISPRUDÊNCIA TEMÁTICA
# ─────────────────────────────────────────────────────────────────────────────
JURIS_TEMATICAS = [
    {
        "tema": "STJ-Teses-Responsabilidade-Civil",
        "titulo": "STJ — Teses de Responsabilidade Civil (Arts. 186, 927 CC)",
        "ramo": "Direito Civil",
        "output": VAULT / "01_PRIVADO" / "JURISPRUDENCIA",
        "tags": ["jurisprudencia", "stj", "responsabilidade-civil", "direito-civil"],
        "teses": [
            ("Art. 186 CC — Dano moral in re ipsa",
             "O dano moral prescinde de prova do prejuízo em si; é presumido da própria ofensa à "
             "dignidade, honra ou imagem. Basta demonstrar o ato ilícito e o nexo causal.\n"
             "  → STJ, REsp 1.631.508 (Tese repetitiva nº 548)"),
            ("Art. 186 CC — Pessoa jurídica e dano moral",
             "A pessoa jurídica pode sofrer dano moral quando há lesão à sua honra objetiva "
             "(reputação, credibilidade comercial), desde que haja efetivo abalo.\n"
             "  → STJ Súmula 227"),
            ("Art. 186 CC — Cumulação dano moral e material",
             "São cumuláveis as indenizações por dano material e dano moral oriundos do mesmo fato.\n"
             "  → STF Súmula 37"),
            ("Art. 927 CC — Responsabilidade objetiva — atividade de risco",
             "A responsabilidade objetiva do parágrafo único do art. 927 aplica-se a atividades "
             "que, por sua natureza, representem risco anormal para os direitos de outrem. "
             "O risco deve ser inerente à atividade, não mero risco genérico.\n"
             "  → STJ, EREsp 1.0 49.027 (Tese repetitiva nº 456)"),
            ("Art. 932 CC — Responsabilidade dos pais",
             "A responsabilidade dos pais por atos dos filhos menores (art. 932, I CC) é objetiva "
             "— independe de culpa in vigilando. O pai não precisa estar presente no momento do ato.\n"
             "  → STJ, REsp 1.436.401"),
            ("Art. 944 CC — Compensatio lucri cum damno",
             "É possível deduzir do valor da indenização os benefícios que a vítima auferiu "
             "em decorrência do evento danoso (compensação do lucro com o dano), "
             "mas apenas quando dano e benefício decorrem do mesmo fato.\n"
             "  → STJ, EREsp 1.488.705 (Tese repetitiva nº 878)"),
        ],
        "correlatos": [
            "[[L10406 Art. 186]] — ato ilícito",
            "[[L10406 Art. 927]] — obrigação de indenizar",
            "[[L10406 Art. 944]] — extensão do dano",
            "[[STJ-Teses-Contratos]] — responsabilidade contratual",
        ],
    },
    {
        "tema": "STJ-Teses-Contratos",
        "titulo": "STJ — Teses de Contratos (Arts. 421, 422, 478 CC)",
        "ramo": "Direito Civil",
        "output": VAULT / "01_PRIVADO" / "JURISPRUDENCIA",
        "tags": ["jurisprudencia", "stj", "contratos", "boa-fe", "direito-civil"],
        "teses": [
            ("Art. 421 CC — Função social do contrato",
             "A função social impede cláusulas abusivas que gerem desequilíbrio excessivo, "
             "mesmo entre partes iguais. Não elimina a autonomia privada — opera como limite.\n"
             "  → STJ, REsp 1.631.703; Enunciado CJF 22"),
            ("Art. 421 CC — Liberdade econômica (§ único, Lei 13.874/2019)",
             "Nas relações contratuais paritárias (partes em igualdade), a intervenção judicial "
             "deve ser mínima. Distinguir contratos de adesão (sujeitos ao CDC) de contratos civis paritários.\n"
             "  → STJ, REsp 2.011.874"),
            ("Art. 422 CC — Boa-fé objetiva e deveres anexos",
             "A boa-fé objetiva impõe deveres laterais (anexos) de informação, lealdade, cuidado e proteção, "
             "mesmo na fase pré-contratual e pós-contratual (culpa post factum finitum).\n"
             "  → STJ, Enunciado CJF 25; REsp 1.723.690"),
            ("Art. 422 CC — Venire contra factum proprium",
             "O comportamento contraditório que viola a confiança legítima da outra parte "
             "configura abuso de direito (venire contra factum proprium). "
             "Decorre da boa-fé objetiva e do art. 187 CC.\n"
             "  → STJ, REsp 1.787.274"),
            ("Art. 478 CC — Revisão por onerosidade excessiva",
             "A revisão contratual por onerosidade excessiva exige: (1) superveniência do fato, "
             "(2) imprevisibilidade, (3) desequilíbrio manifesto, (4) não imputação ao credor. "
             "Pandemia COVID foi reconhecida como fato imprevisível em alguns casos.\n"
             "  → STJ, REsp 1.985.766; EREsp 1.645.844"),
        ],
        "correlatos": [
            "[[L10406 Art. 421]] — função social do contrato",
            "[[L10406 Art. 422]] — princípio da boa-fé",
            "[[L10406 Art. 478]] — resolução por onerosidade excessiva",
            "[[STJ-Teses-Responsabilidade-Civil]] — responsabilidade contratual e extracontratual",
        ],
    },
    {
        "tema": "STJ-Teses-Familia-Sucessoes",
        "titulo": "STJ — Teses de Família e Sucessões (Arts. 1.696, 1.829, 1.845 CC)",
        "ramo": "Direito Civil",
        "output": VAULT / "01_PRIVADO" / "JURISPRUDENCIA",
        "tags": ["jurisprudencia", "stj", "familia", "sucessoes", "direito-civil"],
        "teses": [
            ("Art. 1.696 CC — Alimentos — cessação pela maioridade",
             "A obrigação de prestar alimentos não cessa automaticamente aos 18 anos. "
             "Para manter os alimentos após a maioridade, o filho deve provar necessidade. "
             "O cancelamento exige decisão judicial com contraditório.\n"
             "  → STJ Súmula 358; REsp 1.198.105"),
            ("Art. 1.694 CC — Alimentos entre ex-cônjuges",
             "Os alimentos entre ex-cônjuges têm caráter transitório; devem cessar quando "
             "o credor recupera a capacidade de se sustentar ou inicia nova união. "
             "A pensão não é vitalícia como regra.\n"
             "  → STJ, REsp 1.205.408 (Tese repetitiva nº 499)"),
            ("Art. 1.829 CC — Concorrência do cônjuge com descendentes",
             "O cônjuge concorre com descendentes na herança. A fração depende do regime de bens: "
             "no regime de separação legal obrigatória, o cônjuge NÃO herda (STJ Súmula 655). "
             "No regime de comunhão parcial, herda apenas nos bens particulares.\n"
             "  → STJ Súmula 655; REsp 1.472.945 (Tese repetitiva nº 809)"),
            ("Art. 1.829 CC — Companheiro e herança (STF — tese vinculante)",
             "O companheiro em união estável tem direito à herança nas mesmas condições do cônjuge. "
             "A diferenciação entre cônjuge e companheiro nas regras de herança é inconstitucional.\n"
             "  → STF, RE 878.694 (Tese vinculante — repercussão geral)"),
            ("Art. 1.845 CC — Legítima dos herdeiros necessários",
             "Descendentes, ascendentes e cônjuge são herdeiros necessários e têm direito à "
             "legítima (50% da herança líquida). Testamento não pode afastar a legítima. "
             "Companheiro é equiparado a cônjuge (STF RE 878.694).\n"
             "  → STJ, REsp 1.582.438"),
        ],
        "correlatos": [
            "[[L10406 Art. 1696]] — alimentos — reciprocidade",
            "[[L10406 Art. 1829]] — ordem da vocação hereditária",
            "[[L10406 Art. 1845]] — herdeiros necessários e legítima",
            "[[STJ-Teses-Responsabilidade-Civil]] — danos no direito de família",
        ],
    },
    {
        "tema": "STJ-Teses-Direito-Penal",
        "titulo": "STJ — Teses de Direito Penal (Parte Geral e Parte Especial)",
        "ramo": "Direito Penal",
        "output": VAULT / "02_PENAL" / "JURISPRUDENCIA",
        "tags": ["jurisprudencia", "stj", "direito-penal", "dosimetria"],
        "teses": [
            ("Art. 59 CP — Dosimetria — pena-base",
             "Na fixação da pena-base, cada circunstância judicial desfavorável justifica o "
             "aumento de 1/6 a 1/3 da pena mínima cominada. "
             "Fundamentação vaga ou genérica (só menciona 'personalidade negativa') é nula.\n"
             "  → STJ, HC 306.818 (Tese nº 65 da jurisprudência em teses)"),
            ("Art. 59 CP — Bis in idem na dosimetria",
             "É vedado usar o mesmo fato tanto como circunstância judicial desfavorável "
             "quanto como agravante ou qualificadora. A mesma elementar não pode ser valorada "
             "duas vezes em fases diferentes da dosimetria.\n"
             "  → STJ Súmula 241 (aplicação analógica); REsp 1.739.593"),
            ("Art. 157 CP — Roubo — causa de aumento — arma de brinquedo",
             "Arma de brinquedo NÃO configura a majorante do art. 157, §2°, I CP, "
             "pois não há lesividade real. O STJ cancelou a Súmula 174 e assentou que "
             "a ausência de aptidão real para disparar afasta a majorante.\n"
             "  → STJ (cancelamento Súmula 174); HC 179.631"),
            ("Art. 155 CP — Furto qualificado e privilégio (concurso aparente)",
             "É possível furto qualificado-privilegiado quando o valor é ínfimo "
             "e o réu é primário com bons antecedentes. As qualificadoras e o privilégio "
             "não são incompatíveis por natureza.\n"
             "  → STJ Súmula 511"),
            ("Art. 312 CP — Peculato culposo — reparação do dano",
             "No peculato culposo (art. 312, §2° CP), a reparação do dano até a sentença "
             "de 1° grau extingue a punibilidade; após a sentença, reduz a pena pela metade.\n"
             "  → STJ, REsp 1.182.294"),
            ("Art. 33 CP — Progressão de regime — fração",
             "Condenado por crime comum: 1/6 para progressão ao regime semiaberto; "
             "condenado por crime hediondo sem reincidência: 40% da pena. "
             "Com reincidência específica em crime hediondo: 60%. Após o Pacote Anticrime (Lei 13.964/2019).\n"
             "  → STJ, HC 601.837 (Tese repetitiva nº 7)"),
        ],
        "correlatos": [
            "[[DEL2848 Art. 59]] — dosimetria da pena",
            "[[DEL2848 Art. 155]] — furto",
            "[[DEL2848 Art. 157]] — roubo",
            "[[DEL2848 Art. 312]] — peculato",
            "[[STJ-Teses-Processo-Penal]] — tutelas cautelares e recursos",
        ],
    },
    {
        "tema": "STJ-Teses-Processo-Civil",
        "titulo": "STJ — Teses de Processo Civil (CPC/2015)",
        "ramo": "Processo Civil",
        "output": VAULT / "03_PROCESSO_CIVIL" / "JURISPRUDENCIA",
        "tags": ["jurisprudencia", "stj", "processo-civil", "cpc-2015"],
        "teses": [
            ("Art. 485 CPC — Extinção sem mérito — abandono de causa",
             "O abandono da causa (art. 485, II CPC) exige inércia por mais de 30 dias após "
             "intimação pessoal do autor. Não basta a intimação pelo DJe — é necessária "
             "intimação pessoal do patrono ou do próprio autor.\n"
             "  → STJ, REsp 1.724.453 (Tese repetitiva nº 917)"),
            ("Art. 966 CPC — Ação rescisória — prazo bienal",
             "O prazo de 2 anos da ação rescisória (art. 975 CPC) começa do trânsito em julgado "
             "da ÚLTIMA decisão proferida no processo. Cada acórdão de recurso tem seu próprio "
             "prazo se os pedidos são autônomos.\n"
             "  → STJ, EREsp 1.269.201"),
            ("Art. 1.022 CPC — Embargos de declaração — prequestionamento ficto",
             "A oposição de embargos de declaração, ainda que rejeitados, é suficiente para "
             "fins de prequestionamento (ficto). O recorrente não precisa reiterar a questão "
             "após o julgamento dos embargos.\n"
             "  → STJ Súmula 356 (STF) / REsp 1.133.719"),
            ("Art. 784 CPC — Título executivo extrajudicial — certidão de dívida ativa",
             "A CDA (certidão de dívida ativa) é título executivo extrajudicial (art. 784, IX CPC). "
             "Presunção de liquidez e certeza relativa — pode ser desconstituída por prova em contrário.\n"
             "  → STJ, REsp 1.111.982 (Tese repetitiva nº 338)"),
            ("Art. 139 CPC — Poderes do juiz — medidas atípicas de execução",
             "O juiz pode adotar medidas coercitivas atípicas para efetivação de decisões (art. 139, IV CPC): "
             "apreensão de passaporte, suspensão de CNH, bloqueio de cartão de crédito. "
             "Devem ser subsidiárias, proporcionais e fundamentadas.\n"
             "  → STJ, HC 478.963; REsp 1.788.950"),
        ],
        "correlatos": [
            "[[L13105 Art. 485]] — extinção sem julgamento do mérito",
            "[[L13105 Art. 966]] — ação rescisória",
            "[[L13105 Art. 1022]] — embargos de declaração",
            "[[L13105 Art. 784]] — títulos executivos extrajudiciais",
            "[[Fredie Didier Jr.]] — neoprocessualismo e cooperação",
        ],
    },
    {
        "tema": "STF-Sumulas-Vinculantes-Principais",
        "titulo": "STF — Súmulas Vinculantes Principais (SV 1–60)",
        "ramo": "Direito Constitucional",
        "output": VAULT / "00_APEX" / "JURISPRUDENCIA",
        "tags": ["jurisprudencia", "stf", "sumula-vinculante", "direito-constitucional"],
        "teses": [
            ("SV 3 — TCU — contraditório em anuação de aposentadoria",
             "Nos processos do TCU que possam resultar em anulação ou revogação de ato "
             "que beneficie o interessado, assegura-se o contraditório e a ampla defesa."),
            ("SV 11 — Algemas — uso excepcional",
             "Só é lícito o uso de algemas em casos de resistência e de fundado receio de "
             "fuga ou de perigo à integridade física do preso. Caso contrário: nulidade."),
            ("SV 13 — Nepotismo — vedação",
             "Nomeação de cônjuge, companheiro ou parente até 3° grau para cargo de "
             "confiança na Administração Pública configura nepotismo vedado pelo art. 37 CF."),
            ("SV 14 — Investigado — acesso ao inquérito",
             "O investigado tem direito de acesso aos autos do inquérito policial, "
             "ainda que em sigilo, assegurada a prerrogativa do advogado."),
            ("SV 37 — Aumento de vencimentos por decisão judicial",
             "Não cabe ao Poder Judiciário, que não tem função legislativa, aumentar "
             "vencimentos de servidores públicos sob o fundamento de isonomia."),
            ("SV 56 — Cumprimento de pena em regime mais gravoso",
             "A falta de estabelecimento penal adequado não autoriza a manutenção do "
             "condenado em regime prisional mais gravoso, devendo-se adotar as medidas "
             "alternativas previstas (detração domiciliar ou relaxamento)."),
        ],
        "correlatos": [
            "[[CF88 Art. 103-A]] — súmulas vinculantes — previsão constitucional",
            "[[CF88 Art. 37]] — Administração Pública — SV 13 e SV 37",
            "[[CF88 Art. 5]] — direitos fundamentais — base das principais SVs",
            "[[STJ-Teses-Processo-Civil]] — eficácia das decisões",
        ],
    },
    {
        "tema": "STJ-Teses-Direito-Administrativo",
        "titulo": "STJ/STF — Teses de Direito Administrativo (Improbidade, Licitação, Servidor)",
        "ramo": "Direito Administrativo",
        "output": VAULT / "03_PUBLICO" / "JURISPRUDENCIA",
        "tags": ["jurisprudencia", "stj", "stf", "improbidade", "licitacao", "direito-administrativo"],
        "teses": [
            ("Lei 8.429/92 — Improbidade — dolo específico (Lei 14.230/2021)",
             "Após a Lei 14.230/2021, a ação de improbidade exige dolo específico do agente. "
             "A modalidade culposa foi extinta. A reforma retroage para beneficiar réus em ações "
             "em curso (norma mais benéfica).\n"
             "  → STF, ADI 7.236; STJ, REsp 1.952.586"),
            ("Lei 14.133/2021 — Nova Lei de Licitações — dispensa e inexigibilidade",
             "As hipóteses de dispensa (art. 75) e inexigibilidade (art. 74) são taxativas. "
             "A contratação direta sem procedimento válido configura dano ao erário "
             "e improbidade dolosa.\n"
             "  → TCU, Acórdão 1.628/2023"),
            ("CF art. 37 — Servidor concursado — estabilidade — prazo",
             "A estabilidade adquire-se após 3 anos de efetivo exercício (não de nomeação). "
             "O estágio probatório (que a partir da CF/88 é de 3 anos) é pressuposto da estabilidade. "
             "Cargo em comissão não gera estabilidade.\n"
             "  → STF, RE 1.027.633 (repercussão geral)"),
            ("CF art. 37 — Princípio da moralidade — licitação",
             "Empresa controlada pelos mesmos sócios não pode participar do mesmo certame. "
             "A fraude à licitação mediante empresas com sócios comuns viola o princípio da moralidade "
             "e gera nulidade do contrato.\n"
             "  → STJ, REsp 1.202.477"),
        ],
        "correlatos": [
            "[[CF88 Art. 37]] — princípios da Administração Pública",
            "[[CF88 Art. 41]] — estabilidade do servidor",
            "[[L8429 Art. 9]] — atos de improbidade que importam enriquecimento ilícito",
            "[[STF-Sumulas-Vinculantes-Principais]] — SVs relevantes para o direito administrativo",
        ],
    },
    {
        "tema": "STJ-Teses-Direito-Previdenciario",
        "titulo": "STJ/STF/TNU — Teses de Direito Previdenciário",
        "ramo": "Direito Previdenciário",
        "output": VAULT / "05_ESPECIAL" / "JURISPRUDENCIA",
        "tags": ["jurisprudencia", "stj", "tnu", "stf", "previdenciario", "inss"],
        "teses": [
            ("Art. 42 Lei 8.213 — Aposentadoria por invalidez — incapacidade parcial",
             "A aposentadoria por invalidez não exige incapacidade total e definitiva. "
             "Basta incapacidade para a atividade habitual com impossibilidade de reabilitação "
             "profissional a curto e médio prazo.\n"
             "  → STJ, REsp 1.369.764 (Tese repetitiva nº 7)"),
            ("Art. 57 Lei 8.213 — Aposentadoria especial — EPI eficaz",
             "O fornecimento de EPI eficaz que neutraliza totalmente o agente nocivo afasta "
             "o direito à aposentadoria especial. Mas a eficácia do EPI é questão de fato "
             "que deve ser comprovada pelo INSS — o simples fornecimento não basta.\n"
             "  → STF, ARE 664.335 (Tese vinculante — repercussão geral)"),
            ("Art. 74 Lei 8.213 — Pensão por morte — cônjuge separado",
             "A cônjuge separada ou divorciada que renunciou aos alimentos na separação "
             "tem direito à pensão por morte do ex-cônjuge, desde que comprove necessidade "
             "econômica superveniente.\n"
             "  → STJ Súmula 336"),
            ("Art. 15 Lei 8.213 — Período de graça — desempregado",
             "O segurado desempregado mantém a qualidade de segurado por até 36 meses "
             "(período de graça estendido). A perda da qualidade após o período de graça "
             "extingue os benefícios, salvo se cumprida nova carência.\n"
             "  → TNU Súmula 27; STJ, AgInt no REsp 1.880.296"),
            ("DCI — Data de início do benefício — DIB retroativa",
             "Regra geral: a DIB é a data do requerimento administrativo (DER). "
             "Se o requerimento for feito em até 30 dias do evento (invalidez, acidente), "
             "a DIB retroage à data do evento.\n"
             "  → STJ, REsp 1.310.034 (Tese repetitiva nº 6)"),
        ],
        "correlatos": [
            "[[L8213 Art. 42]] — aposentadoria por invalidez",
            "[[L8213 Art. 57]] — aposentadoria especial",
            "[[L8213 Art. 74]] — pensão por morte",
            "[[CF88 Art. 201]] — RGPS — previdência social",
        ],
    },
]


def gerar_nota_jurisconsulto(j: dict) -> tuple:
    """Retorna (path, conteudo) para a nota do jurisconsulto."""
    fm = {
        "nome": j["nome"],
        "area": j["area"],
        "periodo": j["periodo"],
        "obra_principal": j["obra_principal"],
        "tags": j["tags"],
        "created": DATA,
    }
    fm_str = yaml.dump(fm, allow_unicode=True, default_flow_style=False, sort_keys=False)

    correlatos_str = "\n".join(f"- {c}" for c in j["correlatos"])
    obras_str = "\n".join(f"- {o}" for o in j["obras"])

    corpo = f"""# {j["nome"]} — {j["area"]}

**Período:** {j["periodo"]}
**Obra principal:** {j["obra_principal"]}

---

## PENSAMENTO CENTRAL

{j["pensamento"]}

---

## INFLUÊNCIA NO DIREITO BRASILEIRO

{j["influencia"]}

---

## OBRAS DE REFERÊNCIA

{obras_str}

---

## ARTIGOS CORRELATOS

{correlatos_str}

---

## NOTAS PESSOAIS

[Anotações do caso concreto, passagens marcantes, teses favoritas]

---

**Última atualização:** {DATA}
"""
    conteudo = f"---\n{fm_str}---\n\n{corpo}"
    path = VAULT / "06_JURISCONSULTOS" / j["area"] / f"{j['nome']}.md"
    return path, conteudo


def gerar_nota_juris_tematica(jt: dict) -> tuple:
    """Retorna (path, conteudo) para a nota temática de jurisprudência."""
    fm = {
        "tema": jt["tema"],
        "ramo": jt["ramo"],
        "tribunal": "STJ/STF",
        "tags": jt["tags"],
        "created": DATA,
    }
    fm_str = yaml.dump(fm, allow_unicode=True, default_flow_style=False, sort_keys=False)

    teses_str = ""
    for titulo_tese, texto_tese in jt["teses"]:
        teses_str += f"\n### {titulo_tese}\n\n{texto_tese}\n"

    correlatos_str = "\n".join(f"- {c}" for c in jt["correlatos"])

    corpo = f"""# {jt["titulo"]}

**Ramo:** {jt["ramo"]}
**Fonte:** STJ Jurisprudência em Teses / STF Repercussão Geral

---

## TESES FIXADAS
{teses_str}

---

## ARTIGOS CORRELATOS

{correlatos_str}

---

## OBSERVAÇÕES PRÁTICAS

[Anotações de aplicação concreta — casos, clientes, dificuldades]

---

**Última atualização:** {DATA}
**⚠️ Verificar sempre:** STJ «Jurisprudência em Teses» (teses.stj.jus.br) — versão mais recente
"""
    conteudo = f"---\n{fm_str}---\n\n{corpo}"
    path = jt["output"] / f"{jt['tema']}.md"
    return path, conteudo


def main():
    total = 0

    print("=" * 60)
    print("GERANDO NOTAS DE JURISCONSULTOS")
    print("=" * 60)
    for j in JURISCONSULTOS:
        path, conteudo = gerar_nota_jurisconsulto(j)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(conteudo, encoding="utf-8")
        print(f"  ✅ {path.relative_to(VAULT)}")
        total += 1

    print()
    print("=" * 60)
    print("GERANDO NOTAS TEMÁTICAS DE JURISPRUDÊNCIA")
    print("=" * 60)
    for jt in JURIS_TEMATICAS:
        path, conteudo = gerar_nota_juris_tematica(jt)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(conteudo, encoding="utf-8")
        print(f"  ✅ {path.relative_to(VAULT)}")
        total += 1

    print()
    print(f"Total: {total} notas geradas")


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    main()

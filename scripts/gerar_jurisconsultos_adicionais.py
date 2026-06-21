#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Adiciona novos jurisconsultos ao módulo 06_JURISCONSULTOS/."""
import yaml
from datetime import datetime
from pathlib import Path

VAULT = Path(__file__).parent.parent
DATA = datetime.now().strftime("%Y-%m-%d")

NOVOS = [
    # ── DIREITO CIVIL ────────────────────────────────────────────────────────
    {
        "nome": "Clóvis Beviláqua",
        "area": "Civil",
        "periodo": "1859–1944",
        "obra_principal": "Código Civil dos Estados Unidos do Brasil Comentado (6 volumes, 1916)",
        "tags": ["jurisconsulto", "direito-civil", "cc-1916", "historia-do-direito"],
        "pensamento": (
            "Clóvis Beviláqua foi o redator do Código Civil brasileiro de 1916 — a obra "
            "legislativa mais importante do direito privado nacional até o CC/2002. "
            "Seguiu a tradição pandectista alemã (BGB de 1900) adaptada ao Brasil: "
            "Parte Geral + Partes Especiais (Família, Coisas, Obrigações, Sucessões). "
            "Adotou o método científico de Savigny: o direito como produto histórico do "
            "'espírito do povo' (Volksgeist). Foi professor da Faculdade de Direito do Recife."
        ),
        "influencia": (
            "O CC/1916 vigorou por 86 anos (até 2003). Beviláqua moldou o direito civil "
            "brasileiro por quase um século. Seus Comentários ao CC/1916 são fonte histórica "
            "obrigatória para interpretar institutos que migraram para o CC/2002 com texto "
            "semelhante (negócio jurídico, posse, propriedade, obrigações). "
            "O STJ ainda cita Beviláqua em questões de direito intertemporal e interpretação "
            "histórica de institutos civis."
        ),
        "obras": [
            "Código Civil dos Estados Unidos do Brasil Comentado — 6 vol. (1916, reimpresso Francisco Alves)",
            "Teoria Geral do Direito Civil (1906)",
            "Direito das Obrigações (1896)",
            "Direito da Família (1896)",
        ],
        "correlatos": [
            "[[L10406 Art. 104]] — negócio jurídico — instituto central de Beviláqua",
            "[[L10406 Art. 1228]] — direito de propriedade",
            "[[Pontes de Miranda]] — continuidade e superação do sistema de Beviláqua",
            "[[Miguel Reale]] — coordenador do CC/2002 que substituiu o CC/1916",
        ],
    },
    {
        "nome": "Maria Helena Diniz",
        "area": "Civil",
        "periodo": "1944–",
        "obra_principal": "Curso de Direito Civil Brasileiro (10 volumes)",
        "tags": ["jurisconsulto", "direito-civil", "enciclopedia-juridica"],
        "pensamento": (
            "Maria Helena Diniz é a maior enciclopedista do direito civil brasileiro. "
            "Seu método é o da doutrina sistemática: coleta, organiza e sintetiza toda a "
            "literatura jurídica e jurisprudência sobre cada instituto civil. "
            "Não desenvolve teoria própria marcante, mas é a fonte de consulta mais completa "
            "para doutrina e jurisprudência simultâneas sobre qualquer instituto do CC. "
            "Adota posição conservadora na bioética e no direito de família."
        ),
        "influencia": (
            "O Curso de Direito Civil Brasileiro em 10 volumes é a obra de referência mais "
            "completa do direito civil nacional. Usada em concursos e pela magistratura como "
            "fonte de consulta rápida de jurisprudência e doutrina. "
            "Seu Dicionário Jurídico (4 volumes) é referência terminológica. "
            "O STJ cita Maria Helena Diniz com frequência em responsabilidade civil, "
            "contratos e direito de família."
        ),
        "obras": [
            "Curso de Direito Civil Brasileiro — 10 vol. (Saraiva, atualizados anualmente)",
            "Código Civil Anotado (Saraiva, 18ª ed.)",
            "Dicionário Jurídico — 4 vol. (Saraiva, 3ª ed.)",
            "O Estado Atual do Biodireito (Saraiva, 10ª ed.)",
        ],
        "correlatos": [
            "[[L10406 Art. 186]] — responsabilidade civil — referência enciclopédica",
            "[[L10406 Art. 1511]] — casamento — direito de família",
            "[[Caio Mário da Silva Pereira]] — obra complementar em responsabilidade civil",
            "[[Pontes de Miranda]] — teoria dos fatos jurídicos — base teórica",
        ],
    },
    {
        "nome": "Orlando Gomes",
        "area": "Civil",
        "periodo": "1909–1988",
        "obra_principal": "Obrigações (1961) / Contratos (1959) / Direitos Reais (1958)",
        "tags": ["jurisconsulto", "direito-civil", "obrigacoes", "contratos"],
        "pensamento": (
            "Orlando Gomes foi o grande renovador do direito civil baiano e nacional. "
            "Trouxe para o Brasil as teorias modernas do direito civil europeu (especialmente "
            "italiano e francês). Defendeu a socialização do direito civil: propriedade "
            "com função social, contratos com revisão judicial, proteção dos economicamente "
            "fracos. Seu anteprojeto de CC de 1963 foi o precursor dos debates que levaram ao CC/2002."
        ),
        "influencia": (
            "As obras Obrigações e Contratos de Orlando Gomes são clássicos que ainda definem "
            "a estrutura analítica dessas matérias. O STJ cita Orlando Gomes em questões de "
            "formação dos contratos, defeitos do negócio jurídico e extinção das obrigações. "
            "Sua doutrina sobre a onerosidade excessiva influenciou o art. 478 CC/2002. "
            "É o jurista mais importante da Bahia no século XX."
        ),
        "obras": [
            "Contratos (Forense, 26ª ed.)",
            "Obrigações (Forense, 19ª ed.)",
            "Direitos Reais (Forense, 21ª ed.)",
            "Introdução ao Direito Civil (Forense, 21ª ed.)",
        ],
        "correlatos": [
            "[[L10406 Art. 421]] — função social do contrato",
            "[[L10406 Art. 478]] — resolução por onerosidade excessiva",
            "[[L10406 Art. 233]] — obrigações — objeto e classificação",
            "[[Caio Mário da Silva Pereira]] — contemporâneo — debates sobre reforma do CC",
        ],
    },
    # ── DIREITO PENAL ────────────────────────────────────────────────────────
    {
        "nome": "Guilherme de Souza Nucci",
        "area": "Penal",
        "periodo": "1963–",
        "obra_principal": "Manual de Direito Penal (1ª ed. 2005) / Código Penal Comentado",
        "tags": ["jurisconsulto", "direito-penal", "processo-penal", "juiz"],
        "pensamento": (
            "Nucci é desembargador aposentado do TJSP e o penalista mais lido em concursos hoje. "
            "Adota o finalismo tripartido mas com visão pragmática e garantista moderada. "
            "Defende o garantismo como limite ao poder punitivo — especialmente nas cautelares "
            "processuais penais. Seus comentários ao CPP são os mais detalhados disponíveis "
            "e incorporam sistemáticamente a jurisprudência do STJ e STF."
        ),
        "influencia": (
            "O Manual de Direito Penal e o Código Penal Comentado de Nucci são as obras mais "
            "adotadas nos editais de concursos para delegado, promotor e juiz. "
            "O Código de Processo Penal Comentado (2 volumes) é referência para "
            "questões de processo penal em todos os concursos. "
            "O STJ cita Nucci frequentemente em dosimetria, regime de penas e cautelares."
        ),
        "obras": [
            "Manual de Direito Penal (Forense/GEN, 20ª ed.)",
            "Código Penal Comentado (Forense/GEN, 23ª ed.)",
            "Código de Processo Penal Comentado — 2 vol. (Forense/GEN, 23ª ed.)",
            "Leis Penais e Processuais Penais Comentadas — 2 vol. (Forense/GEN)",
        ],
        "correlatos": [
            "[[DEL2848 Art. 59]] — dosimetria — pena-base — obra de referência",
            "[[DEL2848 Art. 33]] — regime de cumprimento de pena",
            "[[L7210 Art. 112]] — progressão de regime",
            "[[Rogério Greco]] — concorrente direto nos concursos — diferenças de posição",
        ],
    },
    {
        "nome": "Fernando Capez",
        "area": "Penal",
        "periodo": "1963–",
        "obra_principal": "Curso de Direito Penal — 4 volumes (1ª ed. 2001)",
        "tags": ["jurisconsulto", "direito-penal", "processo-penal", "promotor"],
        "pensamento": (
            "Fernando Capez é promotor de justiça em São Paulo e parlamentar. "
            "Seu Curso de Direito Penal é de linguagem extremamente acessível e didática, "
            "direcionado ao estudo para concursos. Adota o finalismo tripartido. "
            "Posição em geral conservadora no Direito Penal: defende expansão punitiva "
            "em crimes graves e crítica ao garantismo radical. "
            "Também escreveu sobre processo penal e legislação especial."
        ),
        "influencia": (
            "O Curso de Direito Penal de Capez é um dos mais vendidos para concursos de "
            "delegado, escrivão e agente policial. Sua linguagem direta e esquemática "
            "facilita a memorização dos institutos penais. "
            "Também é muito usado em cursinhos preparatórios para o Exame da OAB. "
            "O STJ eventualmente o cita em questões de parte especial do CP."
        ),
        "obras": [
            "Curso de Direito Penal — 4 vol. (Saraiva/GEN, 30ª ed.)",
            "Código Penal Comentado (Saraiva)",
            "Curso de Processo Penal (Saraiva, 30ª ed.)",
            "Legislação Penal Especial — 2 vol. (Saraiva)",
        ],
        "correlatos": [
            "[[DEL2848 Art. 14]] — tentativa — teoria objetiva e subjetiva",
            "[[DEL2848 Art. 20]] — erro de tipo — excludente de dolo",
            "[[DEL2848 Art. 121]] — homicídio — classificação e modalidades",
            "[[Guilherme de Souza Nucci]] — comparação de posições em concursos",
        ],
    },
    # ── DIREITO CONSTITUCIONAL ───────────────────────────────────────────────
    {
        "nome": "Luís Roberto Barroso",
        "area": "Constitucional",
        "periodo": "1958–",
        "obra_principal": "Interpretação e Aplicação da Constituição (1ª ed. 1996) / O Novo Direito Constitucional Brasileiro",
        "tags": ["jurisconsulto", "direito-constitucional", "neoconstitucionalismo", "ministro-stf"],
        "pensamento": (
            "Barroso é o principal teórico do neoconstitucionalismo brasileiro: "
            "a Constituição tem força normativa direta, os princípios são normas jurídicas "
            "vinculantes, e a ponderação (Robert Alexy) é o método para resolver colisões "
            "entre direitos fundamentais. Defende ativismo judicial moderado: "
            "o STF deve garantir direitos quando o processo político falha. "
            "Como Ministro do STF (desde 2013, Presidente desde 2023), aplica essa doutrina."
        ),
        "influencia": (
            "Barroso é o jurista brasileiro mais citado internacionalmente. "
            "Sua teoria sobre a interpretação constitucional, a ponderação de princípios "
            "e a eficácia dos direitos fundamentais nas relações privadas (eficácia horizontal) "
            "moldou a jurisprudência do STF da última década. "
            "O Supremo cita Barroso especialmente em colisões de direitos fundamentais "
            "(liberdade de expressão vs. privacidade, segurança vs. liberdade)."
        ),
        "obras": [
            "Interpretação e Aplicação da Constituição (Saraiva, 7ª ed.)",
            "O Novo Direito Constitucional Brasileiro (Fórum, 2013)",
            "Curso de Direito Constitucional Contemporâneo (Saraiva, 10ª ed.)",
            "A Razão sem Voto: O Supremo Tribunal Federal e o Governo da Maioria (2015)",
        ],
        "correlatos": [
            "[[CF88 Art. 5]] — direitos fundamentais — colisão e ponderação",
            "[[CF88 Art. 1]] — dignidade da pessoa humana — fundamento constitucional",
            "[[CF88 Art. 102]] — STF — controle concentrado",
            "[[Alexandre de Moraes]] — constitucionalista e ministro contemporâneo",
        ],
    },
    {
        "nome": "Gilmar Mendes",
        "area": "Constitucional",
        "periodo": "1955–",
        "obra_principal": "Curso de Direito Constitucional (com Paulo Gustavo Gonet Branco, 1ª ed. 2007)",
        "tags": ["jurisconsulto", "direito-constitucional", "controle-de-constitucionalidade", "ministro-stf"],
        "pensamento": (
            "Gilmar Mendes é o maior especialista brasileiro em controle de constitucionalidade. "
            "Sua tese de doutoramento (Controle de Constitucionalidade, 1990) é a obra "
            "definitiva sobre o sistema brasileiro de controle difuso e concentrado. "
            "Defende o diálogo entre os modelos difuso (americano) e concentrado (austríaco/kelseniano). "
            "Como Ministro do STF (desde 2002, ex-Presidente), criou jurisprudência "
            "sobre modulação de efeitos e ADI/ADPF."
        ),
        "influencia": (
            "O Curso de Direito Constitucional (com Branco) é a obra mais densa e completa "
            "sobre controle de constitucionalidade e direitos fundamentais para concursos "
            "de nível superior (juiz federal, promotor). "
            "O STF cita Gilmar Mendes especialmente em ADIs, ADPFs, modulação de efeitos "
            "e mandado de injunção. Sua doutrina sobre o silêncio inconstitucional "
            "(omissão do legislador) é referência."
        ),
        "obras": [
            "Curso de Direito Constitucional (Saraiva, com Branco, 19ª ed.)",
            "Controle Abstrato de Constitucionalidade (Saraiva, 2012)",
            "Jurisdição Constitucional (Saraiva, 6ª ed.)",
            "Direitos Fundamentais e Controle de Constitucionalidade (Saraiva, 4ª ed.)",
        ],
        "correlatos": [
            "[[CF88 Art. 102]] — STF — controle concentrado (ADI, ADC, ADPF)",
            "[[CF88 Art. 5]] — direitos fundamentais — âmbito de proteção",
            "[[CF88 Art. 103]] — legitimados ativos para controle abstrato",
            "[[Luís Roberto Barroso]] — neoconstitucionalismo — debate de métodos",
        ],
    },
    # ── DIREITO PROCESSUAL ───────────────────────────────────────────────────
    {
        "nome": "Humberto Theodoro Jr.",
        "area": "Processual",
        "periodo": "1938–",
        "obra_principal": "Curso de Direito Processual Civil (3 volumes, 1ª ed. 1974)",
        "tags": ["jurisconsulto", "processo-civil", "execucao", "cpc-2015"],
        "pensamento": (
            "Humberto Theodoro Jr. é o desembargador-professor mais influente do processo civil "
            "de Minas Gerais e um dos mais importantes do Brasil. "
            "Seu método é técnico-dogmático: sistematização rigorosa dos institutos processuais "
            "com ampla referência à doutrina italiana (Liebman, Chiovenda). "
            "Defende o processo como instrumento da jurisdição — meio para realizar o "
            "direito material, não um fim em si mesmo (instrumentalismo processual)."
        ),
        "influencia": (
            "O Curso de Direito Processual Civil em 3 volumes é a obra mais usada nos "
            "concursos da magistratura estadual e federal. Atualizado para o CPC/2015, "
            "cobre sistematicamente todos os procedimentos e recursos. "
            "O STJ e STF citam Humberto Theodoro Jr. especialmente em execução civil, "
            "tutelas provisórias e recursos. "
            "Seu volume sobre execução e processo cautelar é o mais detalhado disponível."
        ),
        "obras": [
            "Curso de Direito Processual Civil — 3 vol. (Forense/GEN, 65ª ed.)",
            "A Onda Reformista do Direito Positivo e suas Reflexões sobre o Processo (2007)",
            "Processo de Execução e Cumprimento de Sentença (LEUD, 30ª ed.)",
        ],
        "correlatos": [
            "[[L13105 Art. 784]] — títulos executivos extrajudiciais",
            "[[L13105 Art. 485]] — extinção sem mérito",
            "[[L13105 Art. 294]] — tutela provisória",
            "[[Fredie Didier Jr.]] — neoprocessualismo vs instrumentalismo — debate metodológico",
        ],
    },
    {
        "nome": "Cândido Rangel Dinamarco",
        "area": "Processual",
        "periodo": "1933–",
        "obra_principal": "A Instrumentalidade do Processo (1ª ed. 1987) / Instituições de Direito Processual Civil (4 volumes)",
        "tags": ["jurisconsulto", "processo-civil", "instrumentalismo", "teoria-geral"],
        "pensamento": (
            "Dinamarco é o grande teórico do processo civil brasileiro. "
            "Sua tese da instrumentalidade do processo — o processo existe para servir ao "
            "direito material e à pacificação social, não como valor em si — revolucionou "
            "a dogmática processual brasileira. É um dos autores da 'Escola Processual de São Paulo' "
            "(com Liebman, Ada Pellegrini, Kazuo Watanabe). "
            "Defende a relativização da coisa julgada inconstitucional."
        ),
        "influencia": (
            "As Instituições de Direito Processual Civil em 4 volumes são a obra teórica "
            "mais densa do processo civil nacional. Influenciou diretamente a redação do CPC/2015 "
            "(especialmente os princípios do art. 1°–12). "
            "A teoria da instrumentalidade é a base para o ativismo judicial moderado no processo "
            "(arts. 139, 536 CPC). O STJ e STF citam Dinamarco em questões de teoria geral "
            "do processo, ação, jurisdição e coisa julgada."
        ),
        "obras": [
            "A Instrumentalidade do Processo (Malheiros, 15ª ed.)",
            "Instituições de Direito Processual Civil — 4 vol. (Malheiros, 9ª ed.)",
            "A Reforma da Reforma (Malheiros, 6ª ed.)",
            "Coisa Julgada e sua Revisão (RT, 2023, com Rodrigo Mazzei)",
        ],
        "correlatos": [
            "[[L13105 Art. 1]] — CPC — constitucionalização e instrumentalidade",
            "[[L13105 Art. 139]] — poderes diretivos do juiz",
            "[[L13105 Art. 502]] — coisa julgada — limites",
            "[[Fredie Didier Jr.]] — neoprocessualismo como evolução da instrumentalidade",
        ],
    },
    # ── DIREITO DO TRABALHO ──────────────────────────────────────────────────
    {
        "nome": "Maurício Godinho Delgado",
        "area": "Trabalhista",
        "periodo": "1958–",
        "obra_principal": "Curso de Direito do Trabalho (1ª ed. 2002)",
        "tags": ["jurisconsulto", "direito-trabalho", "clt", "tst", "ministro-tst"],
        "pensamento": (
            "Godinho Delgado é Ministro do TST e o maior jurista do trabalho brasileiro. "
            "Defende o Direito do Trabalho como ramo protetivo e autônomo: "
            "o princípio protetivo é o fundamento de toda hermenêutica trabalhista "
            "(in dubio pro operario, norma mais favorável, condição mais benéfica). "
            "Critica a Reforma Trabalhista (Lei 13.467/2017) como retrocesso social "
            "e defende sua interpretação restritiva."
        ),
        "influencia": (
            "O Curso de Direito do Trabalho é a obra mais completa e mais usada em concursos "
            "para o Ministério Público do Trabalho, TRT e TST. "
            "Seu volume de 2.000+ páginas cobre toda a CLT, doutrina e jurisprudência. "
            "Como ministro do TST, Godinho aplica sua doutrina diretamente nas decisões. "
            "É referência obrigatória para qualquer advogado ou juiz trabalhista."
        ),
        "obras": [
            "Curso de Direito do Trabalho (LTr, 23ª ed.)",
            "A Reforma Trabalhista no Brasil (LTr, 2017, com Gabriela Delgado)",
            "Direito Coletivo do Trabalho (LTr, 9ª ed.)",
            "Tratado Jurisprudencial de Direito Constitucional do Trabalho (RT, 5 vol.)",
        ],
        "correlatos": [
            "[[CF88 Art. 7]] — direitos dos trabalhadores",
            "[[CF88 Art. 8]] — liberdade sindical",
            "[[CF88 Art. 114]] — competência da Justiça do Trabalho",
            "[[L5452 Art. 1]] — CLT — princípios do direito do trabalho",
        ],
    },
    # ── DIREITO TRIBUTÁRIO ───────────────────────────────────────────────────
    {
        "nome": "Roque Antonio Carrazza",
        "area": "Tributario",
        "periodo": "1943–",
        "obra_principal": "Curso de Direito Constitucional Tributário (1ª ed. 1989, 31ª ed.)",
        "tags": ["jurisconsulto", "direito-tributario", "icms", "competencia-tributaria"],
        "pensamento": (
            "Carrazza é o maior especialista em ICMS e em competência tributária do Brasil. "
            "Seu método é constitucionalista: o direito tributário deve ser interpretado "
            "a partir da CF/88, que rigidamente discrimina as competências de cada ente. "
            "Defende a estrita legalidade tributária (nullum tributum sine lege) "
            "e a tipicidade fechada: o legislador não pode usar conceitos vagos para "
            "criar tributos por analogia."
        ),
        "influencia": (
            "O Curso de Direito Constitucional Tributário é a obra mais densa sobre "
            "o sistema tributário nacional sob a ótica constitucional. "
            "O STF e STJ citam Carrazza especialmente em questões de ICMS, ISS, "
            "imunidades tributárias e competência legislativa. "
            "Seu livro sobre ICMS é a obra mais completa sobre esse tributo. "
            "Influenciou toda uma geração de advogados tributaristas."
        ),
        "obras": [
            "Curso de Direito Constitucional Tributário (Malheiros, 31ª ed.)",
            "ICMS (Malheiros, 17ª ed.)",
            "Reflexões sobre a Obrigação Tributária (Noeses, 2010)",
        ],
        "correlatos": [
            "[[CF88 Art. 150]] — limitações ao poder de tributar — imunidades",
            "[[CF88 Art. 155]] — ICMS — competência dos estados",
            "[[CF88 Art. 156]] — ISS — competência dos municípios",
            "[[L5172 Art. 3]] — CTN — conceito de tributo",
        ],
    },
    {
        "nome": "Sacha Calmon Navarro Coêlho",
        "area": "Tributario",
        "periodo": "1940–2022",
        "obra_principal": "Curso de Direito Tributário Brasileiro (1ª ed. 1999, 16ª ed.)",
        "tags": ["jurisconsulto", "direito-tributario", "ctn", "obrigacao-tributaria"],
        "pensamento": (
            "Sacha Calmon é o tributarista mineiro mais importante do século XX/XXI. "
            "Desenvolveu teoria sistemática do direito tributário a partir do CTN: "
            "obrigação tributária, lançamento, decadência e prescrição como núcleos. "
            "Defende a segurança jurídica como valor supremo do direito tributário: "
            "o contribuinte deve poder planejar sua atividade sem risco de surpresas fiscais. "
            "Critica a tributação confiscatória e o abuso das medidas provisórias em matéria tributária."
        ),
        "influencia": (
            "O Curso de Direito Tributário Brasileiro é a obra mais usada nos concursos "
            "de procurador da Fazenda Nacional, auditor-fiscal e juiz federal com especialização "
            "em tributário. O STJ cita Sacha Calmon em prescrição e decadência tributárias, "
            "lançamento por homologação e compensação de créditos tributários. "
            "Sua influência na advocacia tributária paulista e mineira é enorme."
        ),
        "obras": [
            "Curso de Direito Tributário Brasileiro (Forense/GEN, 16ª ed.)",
            "Comentários à Constituição de 1988 — Sistema Tributário (Forense, 10ª ed.)",
            "Obrigação Tributária (Saraiva, 3ª ed.)",
        ],
        "correlatos": [
            "[[L5172 Art. 3]] — CTN — conceito de tributo",
            "[[L5172 Art. 142]] — lançamento tributário",
            "[[L5172 Art. 173]] — decadência do crédito tributário",
            "[[Roque Antonio Carrazza]] — tributário constitucional — obra complementar",
        ],
    },
]


def gerar_nota_jurisconsulto(j: dict) -> tuple:
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


def main():
    print("=" * 60)
    print("ADICIONANDO NOVOS JURISCONSULTOS")
    print("=" * 60)
    total = 0
    for j in NOVOS:
        path, conteudo = gerar_nota_jurisconsulto(j)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(conteudo, encoding="utf-8")
        status = "✅ NOVO" if not path.exists() else "✅"
        print(f"  {status} {path.relative_to(VAULT)}")
        total += 1

    print()
    print(f"Total: {total} notas geradas")
    print()
    print("Módulos agora em 06_JURISCONSULTOS/:")
    areas = sorted(set(j["area"] for j in NOVOS))
    for a in areas:
        print(f"  • {a}")


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    main()

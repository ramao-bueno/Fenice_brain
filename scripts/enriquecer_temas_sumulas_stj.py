#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enriquece temas das Súmulas STJ por análise de texto.
Atualiza frontmatter com campo 'tema' e 'ramo' classificados por keywords.
Fonte de enriquecimento: texto da própria súmula (STJ bloqueia acesso automático ao BDJUR/SCON).
"""
import re
import sys
from pathlib import Path

SUMULAS_DIR = Path(__file__).parent.parent / "00_APEX" / "SUMULAS STJ" / "Sumulas"

# Mapeamento tema → keywords (ordem importa: mais específico primeiro)
TEMAS = [
    ("tributario",      ["tribut", "imposto", "icms", "iss", "ipi", "itr", "ir ", "irpj", "irpf",
                         "cofins", "pis", "csll", "cide", "iptu", "ipva", "itbi", "itcmd",
                         "contribuicao", "taxa ", "fiscal", "fisco", "receita federal",
                         "decadencia fiscal", "prescricao fiscal", "lancamento fiscal"]),
    ("previdenciario",  ["previdenc", "inss", "segurado", "aposentadori", "beneficio previdenc",
                         "auxilio-doenca", "auxilio doença", "pensao por morte", "salario-maternidade",
                         "acidente do trabalho", "beneficio assistencial", "loas", "bpc"]),
    ("trabalhista",     ["trabalhist", "empregado", "empregador", "clt", "tst", "jcj", "trt",
                         "salario", "rescisao", "fgts", "hora extra", "horas extras",
                         "adicional noturno", "adicional de insalubridade", "adicional de periculosidade",
                         "aviso previo", "ferias", "13", "dispensa", "reintegracao",
                         "sindicato", "negociacao coletiva", "convencao coletiva"]),
    ("penal",           ["crime", "delito", "pena ", "penal", "criminal", "criminoso",
                         "reu ", "ré ", "dolo", "culpa ", "culpos", "dano qualificado",
                         "furto", "roubo", "estelionato", "peculato", "corrupcao",
                         "trafico", "tráfico", "homicidio", "latrocinio", "estupro",
                         "lesao corporal", "ameaca", "sequestro", "extorsao",
                         "prescricao penal", "prescricao da pretensao punitiva",
                         "sursis", "livramento condicional", "semi-aberto", "regime",
                         "habeas corpus", "flagrante", "inquerito policial"]),
    ("processual-penal", ["habeas corpus", "prisao", "preso", "cautelar criminal",
                          "prisao preventiva", "prisao temporaria", "liberdade provisoria",
                          "fianca", "flagrante", "inquerito", "acao penal",
                          "competencia criminal", "juri", "tribunal do juri"]),
    ("administrativo",  ["administrac", "administracao publica", "ato administrativo",
                         "licitacao", "contrato administrativo", "servidor publico",
                         "funcionar", "cargo publico", "concurso publico",
                         "desapropriac", "tombamento", "poder de policia",
                         "sancao administrativa", "processo administrativo disciplinar",
                         "pad ", "demissao", "sindicancia", "licenca",
                         "municipio", "estado", "uniao ", "autarquia", "fundacao publica"]),
    ("consumidor",      ["consumidor", "cdc", "codigo de defesa", "fornecedor",
                         "relacao de consumo", "vicio do produto", "fato do produto",
                         "publicidade enganosa", "pratica abusiva", "responsabilidade do fornecedor",
                         "plano de saude", "seguro", "banco", "financeira",
                         "cartao de credito", "juros", "negativacao", "spc", "serasa",
                         "dano moral coletivo", "recall"]),
    ("civil",           ["civil", "contrato", "obrigac", "responsabilidade civil",
                         "indenizac", "dano moral", "dano material", "lucro cessante",
                         "prescricao civil", "decadencia civil", "posse", "propriedade",
                         "usucapiao", "hipoteca", "penhor", "alienacao fiduciaria",
                         "familia", "casamento", "divorcio", "alimentos", "guarda",
                         "adocao", "heranca", "inventario", "partilha", "testamento",
                         "sucessao", "locacao", "locador", "locatario", "inquilino"]),
    ("processual-civil", ["acao civil", "processo civil", "cpc", "competencia",
                          "recurso especial", "embargos", "agravo", "apelacao",
                          "execucao", "penhora", "arresto", "sequestro civil",
                          "tutela antecipada", "tutela cautelar", "liminar",
                          "honorarios advocaticios", "custas", "sucumbencia",
                          "coisa julgada", "litispendencia", "conexao",
                          "legitimidade", "interesse de agir", "condicoes da acao"]),
    ("ambiental",       ["ambient", "meio ambiente", "flora", "fauna", "floresta",
                         "area de preservacao", "app ", "reserva legal",
                         "poluicao", "dano ambiental", "licenca ambiental",
                         "ibama", "sisnama", "codigo florestal"]),
    ("empresarial",     ["empresa", "empresarial", "sociedade ", "falencia", "recuperacao judicial",
                         "concordata", "credito", "debito", "cheque", "nota promissoria",
                         "duplicata", "letra de cambio", "titulo de credito",
                         "marca", "patente", "propriedade intelectual", "pi "]),
    ("constitucional",  ["constituic", "constitucional", "direito fundamental",
                         "mandado de seguranca", "mandado de injuncao",
                         "acao popular", "acao civil publica", "acao direta",
                         "principio", "dignidade", "legalidade", "igualdade",
                         "isonomia", "devido processo legal", "contraditorio",
                         "ampla defesa", "presuncao de inocencia"]),
]


def classificar_tema(texto: str) -> tuple[str, str]:
    """Retorna (tema, ramo) classificados pelo texto da súmula."""
    t = texto.lower()
    # Remove acentos para matching mais robusto
    t = (t.replace("ã", "a").replace("ç", "c").replace("ê", "e")
          .replace("é", "e").replace("á", "a").replace("ó", "o")
          .replace("ú", "u").replace("í", "i").replace("â", "a")
          .replace("ô", "o").replace("û", "u").replace("î", "i")
          .replace("à", "a").replace("õ", "o").replace("ü", "u"))

    for tema, keywords in TEMAS:
        for kw in keywords:
            if kw in t:
                return tema, _ramo(tema)
    return "jurisprudencia-pacifica", "geral"


def _ramo(tema: str) -> str:
    RAMOS = {
        "tributario": "Direito Tributário",
        "previdenciario": "Direito Previdenciário",
        "trabalhista": "Direito do Trabalho",
        "penal": "Direito Penal",
        "processual-penal": "Direito Processual Penal",
        "administrativo": "Direito Administrativo",
        "consumidor": "Direito do Consumidor",
        "civil": "Direito Civil",
        "processual-civil": "Direito Processual Civil",
        "ambiental": "Direito Ambiental",
        "empresarial": "Direito Empresarial",
        "constitucional": "Direito Constitucional",
    }
    return RAMOS.get(tema, "Geral")


RE_FM_START = re.compile(r"^---\n")
RE_FM_END = re.compile(r"^---\n", re.MULTILINE)


def enriquecer_arquivo(filepath: Path, dry_run: bool = False) -> bool:
    """Lê o arquivo, classifica o tema, atualiza o frontmatter."""
    texto = filepath.read_text(encoding="utf-8")

    # Extrai o texto da súmula da seção ## TEXTO DA SÚMULA
    m_texto = re.search(r"## TEXTO DA SÚMULA\s*\n\n> (.*?)(?:\n---|\Z)", texto, re.DOTALL)
    if not m_texto:
        return False

    sumula_text = m_texto.group(1).strip()
    tema, ramo = classificar_tema(sumula_text)

    # Atualiza o frontmatter: substitui tema e adiciona ramo
    def _substituir_fm(m):
        fm = m.group(0)
        # Atualiza tema
        if re.search(r'^tema:', fm, re.MULTILINE):
            fm = re.sub(r'^tema:.*$', f'tema: {tema}', fm, flags=re.MULTILINE)
        else:
            fm = fm.rstrip('\n') + f'\ntema: {tema}\n'
        # Atualiza ou adiciona ramo
        if re.search(r'^ramo:', fm, re.MULTILINE):
            fm = re.sub(r'^ramo:.*$', f'ramo: {ramo}', fm, flags=re.MULTILINE)
        else:
            fm = fm.rstrip('\n') + f'\nramo: {ramo}\n'
        return fm

    novo_texto = re.sub(r"(?s)^---\n.*?---\n", _substituir_fm, texto, count=1)

    if novo_texto == texto:
        return False

    if not dry_run:
        filepath.write_text(novo_texto, encoding="utf-8")
    return True


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    print("=" * 70)
    print("ENRIQUECIMENTO DE TEMAS — SÚMULAS STJ")
    print("Classificação por análise de texto (BDJUR/SCON bloqueiam automação)")
    print("=" * 70)
    print()

    if not SUMULAS_DIR.exists():
        print(f"❌ Diretório não encontrado: {SUMULAS_DIR}")
        return

    arquivos = sorted(SUMULAS_DIR.glob("Sumula-STJ-*.md"))
    print(f"📂 Arquivos encontrados: {len(arquivos)}")
    print()

    contagem_temas = {}
    alterados = 0

    for arq in arquivos:
        # Extrai texto para classificação
        texto = arq.read_text(encoding="utf-8")
        m_texto = re.search(r"## TEXTO DA SÚMULA\s*\n\n> (.*?)(?:\n---|\Z)", texto, re.DOTALL)
        if m_texto:
            sumula_text = m_texto.group(1).strip()
            tema, ramo = classificar_tema(sumula_text)
            contagem_temas[ramo] = contagem_temas.get(ramo, 0) + 1
        else:
            tema, ramo = "jurisprudencia-pacifica", "Geral"

        if enriquecer_arquivo(arq):
            alterados += 1

    print(f"✅ Atualizados: {alterados}/{len(arquivos)} arquivos")
    print()
    print("📊 Distribuição por ramo:")
    for ramo, count in sorted(contagem_temas.items(), key=lambda x: -x[1]):
        barra = "█" * (count // 5)
        print(f"  {ramo:<30} {count:>3}  {barra}")
    print()
    print("=" * 70)


if __name__ == "__main__":
    main()

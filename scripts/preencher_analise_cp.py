#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
preencher_analise_cp.py
Preenche automaticamente as seções de análise técnica de todas as notas
do Código Penal (DEL2848) usando OpenAI API (gpt-4o-mini).

Uso:
  python scripts/preencher_analise_cp.py              # processa todos os vazios
  python scripts/preencher_analise_cp.py --limite 10  # processa só 10 artigos
  python scripts/preencher_analise_cp.py --artigo 121 # processa artigo específico
  python scripts/preencher_analise_cp.py --dry-run    # simula sem gravar

Retoma automaticamente do ponto onde parou (arquivo .done.json).
"""

import os
import re
import sys
import time
import json
import argparse
from pathlib import Path
from datetime import datetime

import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import sys as _sys
_sys.path.insert(0, str(__import__('pathlib').Path(__file__).parent))
from fenice_llm import FeniceClient
from dotenv import load_dotenv

# ─── Configuração ────────────────────────────────────────────────────────────

SCRIPT_DIR = Path(__file__).parent
VAULT      = SCRIPT_DIR.parent
CP_DIR     = VAULT / "02_PENAL" / "Codigos" / "CP" / "DEL2848"
LOG_FILE   = SCRIPT_DIR / "logs" / "preencher_analise_cp.log"
DONE_FILE  = SCRIPT_DIR / "logs" / "preencher_analise_cp.done.json"

load_dotenv(VAULT / ".env")

DELAY      = 0.5
MAX_TOKENS = 4000

# Marcadores que indicam seção ainda vazia (template original)
EMPTY_MARKERS = [
    "[Qual bem jurídico penal este artigo protege?",
    "[Pesquisar: STJ «Jurisprudência em Teses»",
    "[Aplicação na prática forense:",
]

# ─── Prompt ──────────────────────────────────────────────────────────────────

PROMPT = """\
Você é um especialista sênior em Direito Penal brasileiro. Analise o artigo do \
Código Penal abaixo e gere análise técnica completa para um vault Obsidian de \
estudos jurídicos avançados.

ARTIGO: Art. {num}
LEI: DL 2.848/1940 — Código Penal
REDAÇÃO LEGAL:
{redacao}

Gere a análise no formato exato abaixo (use os delimitadores === para cada seção):

=== BEM_JURIDICO ===
[Identifique o bem jurídico tutelado (vida, liberdade, honra, patrimônio, \
administração pública etc.). Mencione o fundamento constitucional (CF art. ...) \
quando relevante. Se o artigo é norma permissiva ou de extensão (não crime), \
explique sua natureza jurídica.]

=== TIPO_PENAL ===
[Estruture em tópicos:
- Sujeito ativo: quem pode praticar (crime comum, próprio, mão própria)
- Sujeito passivo: quem sofre a lesão
- Núcleo do tipo: verbo (matar, subtrair, fraudar etc.)
- Objeto material: sobre o que recai a conduta
- Elementos normativos e descritivos (se houver)
- Resultado exigido (crime material, formal ou de mera conduta)
- Nexo causal / imputação objetiva (quando relevante)
Se não é norma incriminadora, explique a estrutura jurídica.]

=== DOLO_CULPA ===
[Informe: dolo direto, dolo eventual, culpa consciente/inconsciente. \
Elemento subjetivo especial (dolo específico / especial fim de agir) se houver. \
Se admite modalidade culposa, indicar onde está tipificada. \
Se é norma permissiva, explicar o elemento subjetivo da causa justificante.]

=== TENTATIVA ===
[Momento da consumação. A tentativa é cabível (art. 14 CP)? \
Classificar: crime instantâneo ou permanente? Material, formal ou de mera conduta? \
Há desistência voluntária (art. 15) ou arrependimento posterior (art. 16) relevantes?]

=== PENAS ===
[Liste: pena do caput, qualificadoras, causas de aumento (§§), causas de diminuição. \
Regime inicial (aberto/semiaberto/fechado conforme os limites). \
Crime hediondo? Admite ANPP / transação penal / suspensão condicional do processo? \
Se não comina pena (norma permissiva), explicar.]

=== JURISPRUDENCIA ===
[Liste súmulas STJ/STF e teses firmadas que incidem diretamente sobre este artigo. \
Use o formato: "STJ — Súmula NNN: ..." ou "STF — Tese: ..." ou "STJ — Informativo NNN: ...". \
Se não há súmula específica, cite as principais teses firmes dos tribunais superiores. \
Inclua pelo menos 2 itens.]

=== OBSERVACOES ===
[Use bullets com negrito para cada perspectiva:
- **MP/Acusação:** como denunciar, provar, qualificar
- **Defesa:** teses frequentes, excludentes, desclassificações
- **Prática/Tribunais:** competência, procedimento, pontos de concurso]

REGRAS:
- Responda APENAS com o conteúdo nos blocos ===. Sem introdução nem conclusão.
- Português jurídico preciso e conciso.
- Máximo 250 palavras por seção.
- Use markdown (negrito, listas) mas NÃO use callouts Obsidian neste bloco.
"""

# ─── Helpers ─────────────────────────────────────────────────────────────────

def log(msg: str, level: str = "INFO"):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linha = f"[{ts}] [{level}] {msg}"
    print(linha)
    LOG_FILE.parent.mkdir(exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(linha + "\n")


def carregar_done() -> set:
    if DONE_FILE.exists():
        return set(json.loads(DONE_FILE.read_text(encoding="utf-8")))
    return set()


def salvar_done(done: set):
    DONE_FILE.parent.mkdir(exist_ok=True)
    DONE_FILE.write_text(json.dumps(sorted(done), ensure_ascii=False, indent=2),
                         encoding="utf-8")


def esta_vazio(texto: str) -> bool:
    return any(m in texto for m in EMPTY_MARKERS)


def extrair_redacao(texto: str) -> str:
    """Extrai a seção REDACAO LEGAL do arquivo .md."""
    m = re.search(r'## REDACAO LEGAL\s*\n\s*>\s*(.+?)(?=\n---|\Z)', texto,
                  re.DOTALL)
    if m:
        redacao = m.group(1).strip()
        # Remove o prefixo "> " das linhas continuation
        redacao = re.sub(r'\n>\s*', '\n', redacao)
        return redacao[:2000]  # limite de contexto
    return ""


def extrair_num_artigo(nome_arquivo: str) -> str:
    """Ex: 'DEL2848 Art. 128.md' → '128'"""
    m = re.search(r'Art\.\s*(\S+?)(?:\.md)?$', nome_arquivo)
    return m.group(1) if m else nome_arquivo.replace('.md', '')


def parse_resposta(resposta: str) -> dict:
    """Extrai as seções do texto retornado pelo modelo."""
    secoes = {}
    pattern = re.compile(
        r'===\s*(\w+)\s*===\s*\n(.*?)(?====\s*\w+\s*===|\Z)',
        re.DOTALL
    )
    for m in pattern.finditer(resposta):
        chave = m.group(1).strip()
        conteudo = m.group(2).strip()
        secoes[chave] = conteudo
    return secoes


def substituir_secoes(texto_orig: str, secoes: dict) -> str:
    """Substitui as seções de template vazio pelo conteúdo gerado."""

    mapeamento = {
        "BEM_JURIDICO": (
            r'### Bem Jurídico Tutelado\s*\n\[Qual bem jurídico[^\]]*\]',
            "### Bem Jurídico Tutelado\n\n{conteudo}"
        ),
        "TIPO_PENAL": (
            r'### Tipo Penal\s*\n\[Síntese do tipo penal[^\]]*\]',
            "### Tipo Penal\n\n{conteudo}"
        ),
        "DOLO_CULPA": (
            r'### Dolo/Culpa\s*\n\[Qual é a forma de imputação[^\]]*\]',
            "### Dolo/Culpa\n\n{conteudo}"
        ),
        "TENTATIVA": (
            r'### Tentativa e Consumação\s*\n\[Qual é o momento de consumação[^\]]*\]',
            "### Tentativa e Consumação\n\n{conteudo}"
        ),
        "PENAS": (
            r'### Penas Cominadas\s*\n\[Pena não localizada[^\]]*\]',
            "### Penas Cominadas\n\n{conteudo}"
        ),
        "JURISPRUDENCIA": (
            r'## JURISPRUDENCIA\s*\n\[Pesquisar: STJ[^\]]*\]',
            "## JURISPRUDENCIA\n\n{conteudo}"
        ),
        "OBSERVACOES": (
            r'## OBSERVACOES PRATICAS\s*\n\[Aplicação na prática forense[^\]]*\]',
            "## OBSERVACOES PRATICAS\n\n{conteudo}"
        ),
    }

    resultado = texto_orig
    for chave, (padrao, template) in mapeamento.items():
        if chave not in secoes:
            continue
        conteudo = secoes[chave]
        substituicao = template.format(conteudo=conteudo)
        novo = re.sub(padrao, substituicao, resultado, flags=re.DOTALL)
        if novo != resultado:
            resultado = novo

    # Atualiza data de atualização
    resultado = re.sub(
        r'\*\*Última atualização:\*\* \d{4}-\d{2}-\d{2}',
        f'**Última atualização:** {datetime.now().strftime("%Y-%m-%d")}',
        resultado
    )

    return resultado


# ─── Chamada LLM (Claude → OpenAI → Gemini) ─────────────────────────────────

def chamar_gemini(client: FeniceClient, num: str, redacao: str, _tentativa: int = 0) -> dict | None:
    prompt = PROMPT.format(num=num, redacao=redacao)
    try:
        resp = client.completar(prompt)
        log(f"  Art. {num}: provedor={resp.provedor} modelo={resp.modelo}")
        secoes = parse_resposta(resp.texto)
        if not secoes:
            log(f"  Art. {num}: resposta sem seções reconhecíveis", "WARN")
            return None
        return secoes
    except Exception as e:
        log(f"  Art. {num}: todos os provedores falharam — {e}", "ERROR")
        return None


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Preenche análise técnica dos artigos CP via Groq")
    parser.add_argument("--artigo", help="Processar apenas este artigo (ex: 121)")
    parser.add_argument("--limite", type=int, default=0,
                        help="Máximo de artigos a processar nesta execução (0=todos)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Simula sem gravar arquivos")
    parser.add_argument("--force", action="store_true",
                        help="Reprocessa mesmo artigos já marcados como done")
    parser.add_argument("--delay", type=float, default=DELAY,
                        help=f"Segundos entre chamadas API (padrão: {DELAY})")
    args = parser.parse_args()

    client = FeniceClient(max_tokens=MAX_TOKENS)
    done   = carregar_done() if not args.force else set()

    # Lista de arquivos a processar
    if args.artigo:
        # Busca arquivo pelo número do artigo
        candidatos = list(CP_DIR.glob(f"*Art. {args.artigo}.md")) + \
                     list(CP_DIR.glob(f"*Art. {args.artigo}*.md"))
        arquivos = [f for f in candidatos if "_INDEX_GRAPH" not in f.name]
    else:
        arquivos = sorted(
            [f for f in CP_DIR.glob("*.md") if "_INDEX_GRAPH" not in f.name],
            key=lambda f: (
                int(re.search(r'(\d+)', extrair_num_artigo(f.name)).group(1))
                if re.search(r'\d+', extrair_num_artigo(f.name)) else 9999,
                extrair_num_artigo(f.name)
            )
        )

    total = len(arquivos)
    processados = 0
    ignorados   = 0
    erros       = 0

    log(f"=== preencher_analise_cp.py iniciado — {total} arquivo(s) encontrado(s) ===")
    if args.dry_run:
        log("MODO DRY-RUN: nenhum arquivo será gravado")

    for arquivo in arquivos:
        if args.limite and processados >= args.limite:
            log(f"Limite de {args.limite} artigo(s) atingido. Parando.")
            break

        nome = arquivo.name
        num  = extrair_num_artigo(nome)

        # Pula se já processado
        if nome in done and not args.force:
            ignorados += 1
            continue

        texto = arquivo.read_text(encoding="utf-8")

        # Pula se não tem template vazio
        if not esta_vazio(texto):
            log(f"  Art. {num}: já preenchido — ignorando")
            done.add(nome)
            ignorados += 1
            continue

        redacao = extrair_redacao(texto)
        if not redacao or len(redacao) < 10:
            log(f"  Art. {num}: redação não encontrada — ignorando", "WARN")
            ignorados += 1
            continue

        log(f"→ Art. {num}: chamando LLM...")
        secoes = chamar_gemini(client, num, redacao)

        if not secoes:
            erros += 1
            time.sleep(args.delay)
            continue

        novo_texto = substituir_secoes(texto, secoes)

        if args.dry_run:
            log(f"  Art. {num}: dry-run — seções geradas: {list(secoes.keys())}")
        else:
            arquivo.write_text(novo_texto, encoding="utf-8")
            done.add(nome)
            salvar_done(done)
            log(f"  Art. {num}: ✓ gravado ({len(secoes)} seções)")

        processados += 1
        time.sleep(args.delay)

    log(f"=== Concluído — processados: {processados} | ignorados: {ignorados} | erros: {erros} ===")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
Geração de narração para vídeo Fenice bRain
via OpenAI TTS (tts-1-hd, voz nova — feminina, carioca)
v4 — acentuação brasileira completa + sotaque RJ
"""

import os
from pathlib import Path
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

ROTEIRO = """Você já parou pra pensar por que o conhecimento mais importante do mundo — aquele que protege a sua liberdade, a sua família, os seus direitos — é o mais difícil de acessar?

Por que a lei que rege a sua vida parece escrita em outro idioma?

Isso não é acidente. É escolha. E a gente decidiu mudar isso.

Bem-vindo ao Fenice bRain.

A gente não veio aqui pra ser mais um curso. Não veio pra entregar o mínimo aceitável. A gente veio pra ser o melhor. Pra fazer o que ninguém fez antes no Direito brasileiro: unir rigor acadêmico, profundidade filosófica, raiz espiritual e a inteligência artificial mais avançada do mundo — tudo a serviço de quem mais precisa.

Essa é a nossa busca. Todo dia. Sem descanso. Pela excelência.

A gente é herdeiro de Abraão, o pai da fé, o pai da coragem de acreditar quando o mundo inteiro duvida. A gente segue os passos de Ismael, o primogênito, que não herdou a terra prometida, mas herdou algo muito maior: a força de construir no deserto. E a gente ouve Isaac, porque a sabedoria não tem dono — ela pertence a quem a busca com sinceridade.

De Abraão a gente herdou a coragem de recomeçar. Do Direito, a estrutura. Da Filosofia, a profundidade. E da tecnologia, a velocidade pra chegar onde nenhuma editora jamais chegou.

Hans Kelsen ensinou que o Direito é uma pirâmide. Tudo parte de uma norma superior. Tudo tem hierarquia. Tudo tem lógica. E a gente construiu o Fenice bRain exatamente assim: do fundamento ao topo, sem pular etapa, sem enganar o aluno com atalho que não existe.

Na base: a prática. As questões. O cotidiano de quem precisa passar na OAB, no concurso, na prova da vida.

No meio: a teoria viva. Não o artigo frio decorado. O artigo entendido, sentido, aplicado.

No topo: a revisão cirúrgica. O essencial que fica quando o volume passa.

Isso é o Método 60-30-10. Sessenta por cento de questões. Trinta por cento de teoria. Dez por cento de revisão. Testado. Refinado. Entregue sem concessão.

E por trás de tudo isso, a inteligência artificial mais poderosa que existe trabalhando pra você. Claude, da Anthropic, raciocínio profundo e análise jurídica precisa. A OpenAI — a voz que você tá ouvindo agora, a linguagem que conecta máquina e humanidade. E o Google Gemini, velocidade e escala global. Três gigantes da inteligência artificial trabalhando em cadeia, a serviço de um único objetivo: fazer você entender.

Mais de vinte e três mil arquivos no vault. Cada artigo do Código Penal comentado. Cada súmula do STF e do STJ catalogada. Cada filósofo do Direito mapeado e conectado. Kelsen conversa com Aristóteles. Beccaria dialoga com o artigo 121. A Constituição Federal encontra a Torah. Porque o conhecimento não existe em compartimento. Ele é vivo. É orgânico. É uma rede.

Cinco pilares. Cinco promessas. Cinco razões pra você confiar no Fenice bRain.

Jurídico: a lei comentada em linguagem humana. Do primeiro ao último artigo, sem omissão, sem preguiça.

Filosófico: a lente que dá sentido à lei. Porque lei sem filosofia é instrumento de opressão. Com filosofia, é instrumento de libertação.

Teológico: a raiz ética que sustenta tudo. O Islã e o Judaísmo como as duas grandes fontes do pensamento jurídico ocidental — reconhecidas ou não.

Tecnológico: inteligência artificial como serva do conhecimento humano, nunca como substituta. A máquina amplifica. O ser humano decide.

Educacional: o método que funciona, no canal, no aplicativo, no flashcard, na nota atômica. O conhecimento onde você está — não onde o professor tem conforto de estar.

O Fenice bRain é para o estudante que trabalha oito horas e ainda abre o livro à meia-noite. É para o cidadão que quer entender os seus direitos sem pagar por isso. É para o profissional que recusa a mediocridade. É para o acadêmico que busca profundidade onde os outros param na superfície. É pra qualquer pessoa que acredita — que acredita de verdade — que o conhecimento é o maior ato de dignidade que um ser humano pode praticar.

A gratuidade não é campanha de marketing. É princípio sagrado. Conhecimento que se tranca atrás de muro não serve a Deus nem ao ser humano.

Buscar a excelência dói. Exige sacrifício. Exige que você se levante quando quer descansar. Que você revise quando quer parar. Que você aprenda com humildade o que vai distribuir com ousadia.

Mas é exatamente esse caminho que transforma estudante em mestre. Que transforma mestre em referência. Que transforma referência em legado.

A fênix não renasce por acaso. Ela renasce porque escolheu o fogo.

A gente escolheu o fogo. Todo dia.

Somos o Fenice bRain. Jurídico. Filosófico. Teológico. Tecnológico. Educacional.

Acesse agora: www.feniceia.br

Todo louvor pertence a Deus, Senhor dos mundos.

Estude. Cresça. Distribua. O conhecimento que não circula, morre. O que circula, transforma o mundo."""

OUTPUT_DIR = Path("C:/Fenice_bRain/09_FENICE_BRAIN/Videos/2026-06-27")
OUTPUT_FILE = OUTPUT_DIR / "narracao_fenice_brain.mp3"
MAX_CHARS = 4000


def dividir_texto(texto: str, max_chars: int) -> list[str]:
    paragrafos = texto.split("\n\n")
    partes = []
    parte_atual = ""
    for p in paragrafos:
        if len(parte_atual) + len(p) + 2 <= max_chars:
            parte_atual += ("\n\n" if parte_atual else "") + p
        else:
            if parte_atual:
                partes.append(parte_atual.strip())
            parte_atual = p
    if parte_atual:
        partes.append(parte_atual.strip())
    return partes


def gerar_audio():
    print("Gerando narracao via OpenAI TTS...")
    print("Voz: nova (feminina, energetica)")
    partes = dividir_texto(ROTEIRO, MAX_CHARS)
    print(f"Caracteres: {len(ROTEIRO)} | Partes: {len(partes)}")

    arquivos_parte = []
    for i, parte in enumerate(partes):
        arquivo_parte = OUTPUT_DIR / f"narracao_parte_{i+1:02d}.mp3"
        print(f"  Gerando parte {i+1}/{len(partes)} ({len(parte)} chars)...")
        with client.audio.speech.with_streaming_response.create(
            model="tts-1-hd",
            voice="nova",      # feminina, energética — mais próxima do ritmo carioca
            input=parte,
            speed=1.03,        # carioca fala com leveza e fluidez — ligeiramente mais rápido
        ) as response:
            response.stream_to_file(arquivo_parte)
        arquivos_parte.append(arquivo_parte)

    print(f"\nConcatenando {len(arquivos_parte)} partes...")
    with open(OUTPUT_FILE, "wb") as saida:
        for arq in arquivos_parte:
            saida.write(arq.read_bytes())
            arq.unlink()

    tamanho = OUTPUT_FILE.stat().st_size / 1024 / 1024
    print(f"\nNarracao gerada: {OUTPUT_FILE}")
    print(f"Tamanho: {tamanho:.1f} MB")


if __name__ == "__main__":
    gerar_audio()

"""
Geração de narração para vídeo Fenice bRain
via OpenAI TTS (tts-1-hd, voz alloy)
"""

import os
from pathlib import Path
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

ROTEIRO = """Existe um momento na vida de todo estudante em que o Direito para de ser teoria e começa a fazer sentido.

Não é na sala de aula. Não é no livro de mil páginas.

É quando você entende que a lei não existe para confundir — ela existe para proteger. Que a filosofia não existe para complicar — ela existe para iluminar. E que o conhecimento não é privilégio de poucos. Nunca foi.

Bem-vindo ao Fenice bRain.

O Fenice bRain nasceu de uma convicção simples, mas radical: todo ser humano tem direito de entender as leis que regem sua vida. Não os advogados. Não os juízes. Não os professores de universidade. Todo ser humano.

Somos herdeiros de Abraão, o pai da fé monoteísta, que atravessou o deserto carregando apenas uma verdade: que Deus é único, e que o conhecimento que d'Ele vem não pode ser aprisionado. Seguimos os passos de Ismael, o primogênito, que aprendeu com a areia, com o vento, com a vida. E não fechamos os ouvidos a Isaac, porque a sabedoria acumulada por milênios também é nossa herança.

De Abraão herdamos a coragem de começar do zero. Do Direito, a estrutura. Da Filosofia, a lente para enxergar mais longe. Da tecnologia, a velocidade para chegar a mais pessoas.

O Fenice bRain funciona como uma pirâmide. Assim como Hans Kelsen ensinou que toda lei tem uma norma superior que a sustenta, até chegar à Constituição Federal, o ápice de tudo, nós organizamos o conhecimento da mesma forma.

Na base: as questões. A prática. O cotidiano do estudante que precisa passar na OAB, no concurso, na prova. No meio: a teoria. Os artigos comentados. A doutrina explicada em linguagem humana. No topo: a revisão. O essencial. O que fica depois que tudo passa.

Chamamos isso de Método 60-30-10. Sessenta por cento do seu tempo em questões. Trinta por cento em teoria. Dez por cento em revisão. Simples assim. Eficaz assim.

Não inventamos nada. Aprendemos com os melhores e adaptamos para o Direito brasileiro. Porque humildade em aprender é a primeira condição para ensinar bem.

Por trás do Fenice bRain existe um sistema de inteligência artificial construído para servir o estudante, não para substituí-lo. Claude, da Anthropic. OpenAI. Google Gemini. Trabalhando juntos, em cadeia, para analisar legislação, identificar antinomias, gerar resumos, responder perguntas.

O vault do Obsidian tem mais de vinte e três mil arquivos. Cada artigo do Código Penal comentado. Cada súmula do STF e do STJ indexada. Cada filósofo do Direito mapeado. E tudo conectado, porque o conhecimento não existe em caixas separadas. Kelsen conversa com Aristóteles. O artigo 121 do Código Penal conversa com Beccaria. A Constituição Federal conversa com a Torah.

Cinco pilares sustentam tudo que construímos.

Jurídico: a legislação brasileira comentada, acessível e atualizada. Do artigo primeiro ao último, com linguagem para quem quer entender, não decorar.

Filosófico: de Aristóteles a Rawls, de Sócrates a Dworkin, a lente filosófica que dá sentido à lei. Porque a lei sem filosofia é letra morta.

Teológico: a tradição abraâmica como fundamento ético. Islam e Judaísmo como as duas raízes de onde todo o Direito ocidental bebeu, mesmo sem saber.

Tecnológico: inteligência artificial como ferramenta, não como oráculo. A máquina serve ao estudante. Nunca o contrário.

Educacional: o método. A repetição. O canal no YouTube. Os aplicativos. Os flashcards. O conhecimento onde o aluno está, não onde o professor quer estar.

O Fenice bRain é para o homem médio. Não o expert. Não o acadêmico. O cidadão que quer entender por que foi multado. Por que perdeu o emprego. Por que o vizinho pode ou não pode fazer o que faz. Por que a lei protege uns e esquece outros.

É para o estudante que trabalha o dia todo e estuda à noite. Que não tem dinheiro para cursinho premium mas tem disciplina e acesso à internet. É para o profissional que quer atualização sem perder a essência. É para qualquer pessoa que acredita que entender a lei é um ato de dignidade.

A gratuidade não é estratégia de marketing. É princípio. Conhecimento que não circula não serve a Deus nem ao homem.

A fênix renasce das cinzas.

O Fenice bRain nasceu das ruínas de um sistema jurídico inacessível. De uma educação que historicamente escolheu quem pode aprender. De uma filosofia esquecida nas prateleiras das bibliotecas.

Renascemos. Com tecnologia. Com fé. Com método. Com a convicção de que o conhecimento pertence a todos.

Somos o Fenice bRain. Jurídico. Filosófico. Teológico. Tecnológico. Educacional.

Todo louvor pertence a Deus, Senhor dos mundos.

Inscreva-se. Estude. Compartilhe. O conhecimento que não se distribui, morre."""

OUTPUT_DIR = Path("C:/Fenice_bRain/09_FENICE_BRAIN/Videos/2026-06-27")
OUTPUT_FILE = OUTPUT_DIR / "narracao_fenice_brain.mp3"
MAX_CHARS = 4000


def dividir_texto(texto: str, max_chars: int) -> list[str]:
    """Divide em partes respeitando parágrafos."""
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
    print("Gerando narração via OpenAI TTS (tts-1-hd, voz: alloy)...")
    partes = dividir_texto(ROTEIRO, MAX_CHARS)
    print(f"Total de caracteres: {len(ROTEIRO)} - dividido em {len(partes)} partes")

    arquivos_parte = []
    for i, parte in enumerate(partes):
        arquivo_parte = OUTPUT_DIR / f"narracao_parte_{i+1:02d}.mp3"
        print(f"  Gerando parte {i+1}/{len(partes)} ({len(parte)} chars)...")
        with client.audio.speech.with_streaming_response.create(
            model="tts-1-hd",
            voice="alloy",
            input=parte,
            speed=0.95,
        ) as response:
            response.stream_to_file(arquivo_parte)
        arquivos_parte.append(arquivo_parte)

    # Concatenar todas as partes em um único MP3
    print(f"\nConcatenando {len(arquivos_parte)} partes...")
    with open(OUTPUT_FILE, "wb") as saida:
        for arq in arquivos_parte:
            saida.write(arq.read_bytes())
            arq.unlink()

    tamanho = OUTPUT_FILE.stat().st_size / 1024 / 1024
    print(f"\n✅ Narração gerada: {OUTPUT_FILE}")
    print(f"   Tamanho: {tamanho:.1f} MB")
    print(f"   Pronto para mixar com o highlight reel Adobe!")


if __name__ == "__main__":
    gerar_audio()

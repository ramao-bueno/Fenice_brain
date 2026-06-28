# -*- coding: utf-8 -*-
"""
Narração: "Mallet e o Forte Guardião"
Voz: onyx (masculina, grave, cálida) — militar de idade avançada
Velocidade: 0.80 — cansado mas firme, esperançoso
Modelo: tts-1-hd (máxima qualidade)
"""

import os
from pathlib import Path
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

ROTEIRO = """
Quando você passa de muitos anos de serviço à pátria... o cansaço não vem dos pés.
Vem da alma que viu muito.

Sou um velho soldado.
Os joelhos já não dobram como deveriam.
A voz perdeu o trovão que um dia fez recrutas ficar firmes, à atenção.
Mas os olhos... os olhos ainda enxergam longe.
Muito longe.

E é daqui, do alto desse morro, olhando para a Baía Babitonga, que eu vejo vocês.
A mocidade desse Brasil imenso.
E é para vocês que eu preciso contar essa história.

Esse lugar onde eu estou sentado se chama Forte Marechal Luz.
Está aqui, na Ponta do João Dias, em São Francisco do Sul, em Santa Catarina.

Não é apenas um forte.
É uma promessa de pedra e cal, erguida ao longo de séculos por mãos que nunca duvidaram do que estavam construindo.

A história desse lugar começa antes de 1715.
Os portugueses instalaram aqui uma bateria rústica de canhões.
O motivo era simples: proteger esse litoral.
Manter a soberania.
Garantir que os navios espanhóis, ingleses e franceses não entrassem na Baía Babitonga
e levassem o que era nosso.

A madeira. A erva-mate. O escoamento do Planalto Norte.
O porto de São Francisco já era essencial, e precisava de alguém que o guardasse.

Em 1909, o governo federal comprou essas terras.
E em vinte de maio de 1913, a Quinta Bateria Independente de Artilharia de Costa foi formalmente instalada aqui.

O nome do forte homenageia o Marechal Francisco Carlos da Luz.
Um militar, intelectual e político catarinense.
Um homem do Sul. Um homem que construiu.

Ali no topo estão quatro canhões.
Vieram do Reino Unido.
Têm alcance de mais de dezoito quilômetros.
Nos dias de teste, as línguas de fogo que saíam deles incendiavam a vegetação ao redor.
A fumaça subia. A terra tremia. O som chegava do outro lado da baía.

E sabe o que é impressionante?

Esses canhões nunca foram usados em combate real.
Nunca.

Não porque faltou preparo.
Porque não faltou.
Mas porque a presença deles, a disciplina dos que os operavam, a seriedade do que esse forte representava...
era suficiente.
O inimigo olhava para cá de longe e decidia não entrar.

Isso é o que a força real faz.
Ela não precisa atirar para vencer.
Ela precisa estar pronta.

Aprendi muito aqui.

Aprendi com o meu comandante, um homem que nunca gritou com a tropa quando a tropa merecia um grito.
Ele dizia: Soldado que precisa de berro pra fazer o certo, não aprendeu nada ainda.

Aprendi que a calma na hora certa é a maior arma que qualquer pessoa pode ter.
Que a disciplina não é punição.
É liberdade.
A liberdade de agir com precisão quando o mundo ao redor está em caos.

O forte foi desativado em 1977.
Por décadas, ficou em silêncio.
Mas em 1996 reabriu.
E hoje, as casamatas subterrâneas onde guardávamos munição viraram museu.
Os alojamentos onde dormíamos viraram colônia de férias.
E daqui do alto, essa vista da entrada da Baía Babitonga e do Arquipélago da Graça...
continua sendo uma das mais bonitas do Sul do Brasil.

O forte mudou de função.
Mas não perdeu o propósito.
Ainda guarda.
Agora guarda memória. Guarda história. Guarda identidade.

Eu servi aqui.
Passei tardes subindo esse morro com a tropa, revistando posição, garantindo que cada canhão estava pronto.
Sabia que provavelmente nunca precisaria disparar.
Mas era exatamente essa prontidão que dava sentido a tudo.

E agora, décadas depois, eu me sento nesse velho banco
e fico pensando no que nós deixamos para vocês.

Deixamos um Brasil que ainda precisa de guardiões.
Deixamos fardas, honra, e uma história escrita com suor e com sangue
e com sacrifício silencioso, daquele que ninguém filma, que ninguém aplaude.
Deixamos um exemplo.

Mas exemplo sem continuação é apenas saudade.

Por isso, filho.
Por isso, filha.

Sim. Filha.

Porque algo mudou desde que eu era jovem.
Algo bonito mudou.

As mulheres desse Brasil ingressaram nas Forças Armadas.
E não de qualquer jeito.
Com mérito. Com coragem. Com competência que envergonha a mediocridade onde quer que ela esteja.
Vi recrutas em campo de treinamento que fariam qualquer veterano corar de orgulho.
Vi líderes que tomam decisões com uma precisão que eu só vi nos melhores que conheci em toda a minha vida.

A pátria não tem gênero.
A pátria tem alma.
E essa alma pede filhos e filhas à altura do que ela representa.

O que eu peço a vocês é simples.
Fácil de dizer. Difícil de fazer. Mas possível para quem se prepara.

Estudem.
Não pelo diploma. Não pelo salário.
Estudem porque o cidadão ignorante é o mais fácil de enganar.
Estudem porque no dia em que você entende a lei, ninguém mais te vende como mercadoria.
Estudem porque o país que você vai herdar vai precisar de você inteiro.
Não pela metade.

Sirvam.
Sirvam à pátria de alguma forma.
Não precisa ser na farda, embora eu recomende de coração.
Sirva na sala de aula. Sirva no hospital. Sirva no campo. Sirva onde você estiver.
Mas sirva.
Porque o cidadão que só recebe e nunca devolve é uma dívida que a nação inteira paga.

E sejam bons.
Bons de verdade.
Não a bondade mole que finge que tudo está bem quando não está.
A bondade firme, aquela que diz a verdade quando a mentira seria mais fácil.
Aquela que fica quando é mais simples ir embora.

Eu não sei quantas auroras mais vou acordar para ver.

Mas sei que toda manhã que esse forte ainda está de pé...
Toda manhã que alguém sobe esse morro e para diante desses canhões...
Toda manhã que um jovem olha para essa história e sente alguma coisa mexer no peito...

Vale a pena.

Toda batalha que eu travei.
Toda noite sem dormir.
Todo sacrifício que minha família fez por essa farda.
Vale a pena.

Porque a pátria não é um pedaço de terra.
A pátria é o que você decide fazer com o pedaço de terra que ela lhe deu.

Cuide dela.

Guarde-a.

E quando você não puder mais...

Passe para frente.

Como estou fazendo agora.

Para você.
"""

OUTPUT_DIR = Path(r"C:\Fenice_bRain\09_FENICE_BRAIN\Videos\2026-06-27")
OUTPUT_FILE = OUTPUT_DIR / "narracao_mallet_forte_guardiao.mp3"
MAX_CHARS = 4000


def dividir_texto(texto: str, max_chars: int) -> list[str]:
    paragrafos = [p.strip() for p in texto.strip().split("\n\n") if p.strip()]
    partes, atual = [], ""
    for p in paragrafos:
        if len(atual) + len(p) + 2 <= max_chars:
            atual += ("\n\n" if atual else "") + p
        else:
            if atual:
                partes.append(atual)
            atual = p
    if atual:
        partes.append(atual)
    return partes


def gerar_audio():
    print("=" * 55)
    print("Fenice — Narração: Mallet e o Forte Guardião")
    print("=" * 55)
    print(f"Voz:       onyx (masculina, grave)")
    print(f"Velocidade: 0.80 (cansado mas firme)")
    print(f"Modelo:    tts-1-hd")

    partes = dividir_texto(ROTEIRO, MAX_CHARS)
    total_chars = sum(len(p) for p in partes)
    print(f"Caracteres: {total_chars} | Partes: {len(partes)}\n")

    arquivos_parte = []
    for i, parte in enumerate(partes):
        arq = OUTPUT_DIR / f"_mallet_parte_{i+1:02d}.mp3"
        print(f"  Gerando parte {i+1}/{len(partes)} ({len(parte)} chars)...")
        with client.audio.speech.with_streaming_response.create(
            model="tts-1-hd",
            voice="onyx",
            input=parte,
            speed=0.85,
        ) as resp:
            resp.stream_to_file(arq)
        arquivos_parte.append(arq)

    print(f"\nConcatenando {len(arquivos_parte)} partes...")
    with open(OUTPUT_FILE, "wb") as out:
        for arq in arquivos_parte:
            out.write(arq.read_bytes())
            arq.unlink()

    tamanho = OUTPUT_FILE.stat().st_size / 1024 / 1024
    print(f"\n✅ Áudio gerado: {OUTPUT_FILE.name}")
    print(f"   Tamanho: {tamanho:.1f} MB")
    print(f"   Path:    {OUTPUT_FILE}")


if __name__ == "__main__":
    gerar_audio()

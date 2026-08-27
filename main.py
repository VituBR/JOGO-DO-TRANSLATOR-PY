import random as rd
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator
import time as t

words_by_level = {
    "fácil": [
    "gato", "cachorro", "maçã", "leite", "sol",
    "água", "casa", "carro", "mesa", "livro"
],

"médio": [
    "escola", "amigo", "janela", "amarelo", "cadeira",
    "comida", "cidade", "montanha", "sapato", "espelho"
],

"difícil": [
    "tecnologia", "universidade", "informação", "pronúncia", "imaginação",
    "conhecimento", "experiência", "responsabilidade", "desenvolvimento", "possibilidade"
],

"extremo": [
    "desenvolvimento", "desconhecimento", "empreendedorismo", "sustentabilidade",
    "extraordinário", "consequência", "aproximadamente", "incompatibilidade",
    "imprevisibilidade", "interdisciplinaridade", "biodiversidade", "vulnerabilidade",
    "conscientização", "representatividade", "constitucionalidade"
]
}

for rodada in range(1, 6):
    print(f"\nRodada {rodada} de 5")

    pontinis = 0

    duration = 4  # segundos de gravação
    sample_rate = 44100

    nivel = input("escolha um nivel de dificuldade (fácil, médio, difícil, extremo): ")

    escolhida = words_by_level[nivel]

    skol = rd.choice(escolhida)

    print(skol)
    t.sleep(2)

    preparado = input("Preparado(a)? vc vai falar esta palavra escolhida em inglês (s/n): ")

    if preparado.lower() == "s":
        print("Ok, vamos começar!")
        print("Fale agora...")
        recording = sd.rec(
            int(duration * sample_rate), # o número de amostras a serem registradas
            samplerate=sample_rate,      # taxa de amostras
            channels=1,                  # 1 significa gravação mono
            dtype="int16")               # tipo de dados para as amostras registradas
        sd.wait()  # aguardando o término da gravação


    wav.write("output.wav", sample_rate, recording)
    print("Gravação concluída, estou reconhecendo...")

    recognizer = sr.Recognizer()
    with sr.AudioFile("output.wav") as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio, language="en-US")

        lang = input("Para qual idioma devo traduzir? (por exemplo, 'en' - inglês, 'es' - espanhol): ")
        translator = Translator()
        translated = translator.translate(text, dest=lang)  # O 'en' aqui é um código para inglês
        print("🌍 Tradução para o português:", translated.text)
    
        if skol.lower() == translated.text.lower():
            print("Você acertou! Disse:", skol)
            if nivel == "extremo":
                pontinis += 20
            elif nivel == "difícil":
                pontinis += 15
            elif nivel == "médio":
                pontinis += 10
            elif nivel == "fácil":
                pontinis += 5
        elif skol.lower() != translated.text.lower():
            print("Você errou! Disse:", translated.text, "e a tradução correta é:", skol)
            if nivel == "extremo":
                pontinis -= 23
            elif nivel == "difícil":
                pontinis -= 18
            elif nivel == "médio":
                pontinis -= 13
            elif nivel == "fácil":
                pontinis -= 8
    except sr.UnknownValueError:             # - se o Google não conseguiu entender a fala devido a ruídos ou silêncio
        print("A fala não pôde ser reconhecida.")
    except sr.RequestError as e:             # - se não houver conexão com a Internet ou a API estiver indisponível
        print(f"Service error: {e}")

print(f"\nPontuação final: {pontinis}")

if pontinis == 100:
    print("bizarro 100 pontos... uau... você é americano ou brasileiro? só pra saber mesmo")
elif pontinis >= 80 and pontinis < 100:
    print("VOCÊ TEM 80 PONTOS OU MAIS?!! UAU! Você é um(a) excelente falante de inglês!")
elif pontinis >= 60 and pontinis < 80:
    print("você tem 60 pontos ou mais! Boa! Continue praticando para melhorar ainda mais!")
elif pontinis >= 40 and pontinis < 60:
    print("você tem 40 pontos ou mais, Ok Mas Continue praticando para melhorar mais!")
elif pontinis >= 20 and pontinis < 40:
    print("você tem 20 pontos ou mais, Isso não é tão bom..., Mas tudo bem! Continue praticando para melhorar mais!")
elif pontinis < 20 and pontinis > 0:
    print("você tem menos de 20 pontos... Isso não é NADA bom... Continue praticando um dia você vai conseguir!")
elif pontinis == 0 and pontinis > -20:
    print("você tem 0 pontos... Isso é péssimo... Mas eu acredito que um dia você vai conseguir alguns pontos pelo menos né? Se esforce!")
elif pontinis < 0 and pontinis > -20:
    print("você tem menos de 0 pontos, Ok agora já ta ficando bizarro, mas eu ainda acredito que você possa melhorar, por favor se ESFORCE Bastante!")
elif pontinis < -80 and pontinis > -100:
    print("você tem menos de -80 pontos, uau deixa eu adivinhar vc colocou tudo no extremo né?")
elif pontinis < -100 and pontinis > -115:
    print("você tem menos de -100 pontos, você pode ser um ótimo falante de português, mas de inglês você não sabe nada pode ter certeza disso")
elif pontinis == -115:
    print("você tem -115 pontos, eu me questiono se você é humano, você sequer sabe falar português direito, e ainda quer falar inglês? Um incrivel feito de não saber falar nada, parabéns!")

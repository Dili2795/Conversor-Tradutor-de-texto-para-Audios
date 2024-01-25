# Instalação:
    # pip install pyttsx3
    # pip install pygame
    # pip install googletrans==4.0.0-rc1

import gtts
import pyttsx3
import pygame
import time
import os
from googletrans import Translator

def escolher_voz(conversor):
    voices = conversor.getProperty('voices')
    print("Voices disponíveis:")
    for idx, voice in enumerate(voices):
        print(f"{idx + 1}. {voice.name}")
    while True:
        escolha = input("Escolha o número da voz desejada: ")
        try:
            voz_selecionada = voices[int(escolha) - 1]
            conversor.setProperty('voice', voz_selecionada.id)
            print(f"Voz selecionada: {voz_selecionada.name}")
            break
        except (ValueError, IndexError):
            print("Opção inválida. Tente novamente.")

def traduzir_texto(texto, idioma_destino='pt'):
    translator = Translator()
    try:
        traducao = translator.translate(texto, dest=idioma_destino)
        return traducao.text
    except Exception as e:
        print(f"Erro na tradução: {e}")
        return texto

conversor = pyttsx3.init(driverName='sapi5', debug=True,)
pygame.mixer.init()
pg = pygame.mixer.music
conversor.setProperty('rate', 150)
conversor.setProperty('volume', 1.0)

nome = input('Digite seu nome: ')
intro = f'Bem-vindo {nome} ao Conversor de Texto em Fala!\n----------------------------------'
print(intro)
conversor.say(intro)
conversor.runAndWait()

escolher_voz(conversor)

while True:
    print('[1] - Digitar o que deseja escutar\n[2] - Converter o texto.txt em voz\n[0] - Encerrar programa')
    opcao = input('Escolha uma das opções: ')
    
    try:
        opcao = int(opcao)
        if opcao == 1:
            while True:
                print('[1] - Digitar o que deseja escutar\n[2] - Converter o texto.txt em voz\n[0] - Encerrar programa')
                mensagem = input('Digite o que quer escutar ou "voltar" para ir para o Menu anterior: ')
                
                if mensagem.lower() == 'voltar':
                    break
                
                idioma_destino = input('Digite o idioma de destino (por exemplo, "pt" para português): ')
                mensagem_traduzida = traduzir_texto(mensagem, idioma_destino)
                
                conversor.say(mensagem_traduzida)
                conversor.runAndWait()

        elif opcao == 2:
            texto_completo = ""
            with open('texto.txt', 'r') as arquivo:
                for linha in arquivo:
                    texto_completo += linha

            if texto_completo:
                idioma_destino = input('Digite o idioma de destino (por exemplo, "pt" para português): ')
                texto_traduzido = traduzir_texto(texto_completo, idioma_destino)
                
                texto = gtts.gTTS(texto_traduzido, lang=idioma_destino)
                texto.save('texto.mp3')
                pg.load('texto.mp3')
                pg.play()

                while pg.get_busy():
                    pygame.time.Clock().tick(10)  # Aguarda 10 milissegundos

                pg.stop()
                pg.unload()
                os.remove('texto.mp3')

            else:
                print('O arquivo texto.txt está vazio!')

        elif opcao == 0:
            print('Encerrar programa!')
            break

        else:
            print('Opção inválida. Tente novamente.')

    except ValueError:
        print('Entrada inválida. Informe um número.')

    except Exception as e:
        print(f"Erro inesperado: {e}")

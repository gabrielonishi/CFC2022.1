#importe as bibliotecas
from suaBibSignal import *
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import sys

FREQUENCIAS = [697, 770, 852, 941, 1206, 1339, 1477, 1633]
TONS = {
    1: (FREQUENCIAS[0], FREQUENCIAS[4]),
    2: (FREQUENCIAS[0], FREQUENCIAS[5]),
    3: (FREQUENCIAS[0], FREQUENCIAS[6]),
    4: (FREQUENCIAS[1], FREQUENCIAS[4]),
    5: (FREQUENCIAS[1], FREQUENCIAS[5]),
    6: (FREQUENCIAS[1], FREQUENCIAS[6]),
    7: (FREQUENCIAS[2], FREQUENCIAS[4]),
    8: (FREQUENCIAS[2], FREQUENCIAS[5]),
    9: (FREQUENCIAS[2], FREQUENCIAS[6])
}

#funções a serem utilizadas
def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

#converte intensidade em Db, caso queiram ...
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

def main():
    
    #********************************************instruções*********************************************** 
    # seu objetivo aqui é gerar duas senoides. Cada uma com frequencia corresposndente à tecla pressionada
    # então inicialmente peça ao usuário para digitar uma tecla do teclado numérico DTMF
    # agora, voce tem que gerar, por alguns segundos, suficiente para a outra aplicação gravar o audio, duas senoides com as frequencias corresposndentes à tecla pressionada, segundo a tabela DTMF
    # se voce quiser, pode usar a funcao de construção de senoides existente na biblioteca de apoio cedida. Para isso, você terá que entender como ela funciona e o que são os argumentos.
    # essas senoides tem que ter taxa de amostragem de 44100 amostras por segundo, entao voce tera que gerar uma lista de tempo correspondente a isso e entao gerar as senoides
    # lembre-se que a senoide pode ser construída com A*sin(2*pi*f*t)
    # o tamanho da lista tempo estará associada à duração do som. A intensidade é controlada pela constante A (amplitude da senoide). Seja razoável.
    # some as senoides. A soma será o sinal a ser emitido.
    # utilize a funcao da biblioteca sounddevice para reproduzir o som. Entenda seus argumento.
    # grave o som com seu celular ou qualquer outro microfone. Cuidado, algumas placas de som não gravam sons gerados por elas mesmas. (Isso evita microfonia).
    
    # construa o gráfico do sinal emitido e o gráfico da transformada de Fourier. Cuidado. Como as frequencias sao relativamente altas, voce deve plotar apenas alguns pontos (alguns periodos) para conseguirmos ver o sinal
    
    print("Inicializando encoder")
    digit = int(input("Escolha um dígito para transmissão"))
    print("Aguardando usuário")
    print("Gerando Tons base")

    # gerador do tom
    fs = 44100
    f1 = FREQUENCIAS[0]
    f2 = FREQUENCIAS[4]
    f3 = FREQUENCIAS[5]
    f4 = FREQUENCIAS[6]
    meusignal = signalMeu()
    time = 10
    n = time * fs
    time_array, sin1 = meusignal.generateSin(f1, time, fs)
    _, sin2 = meusignal.generateSin(f2, time, fs)
    _, sin3 = meusignal.generateSin(f3, time, fs)
    _, sin4 = meusignal.generateSin(f4, time, fs)


    tone = sin1 + sin2 + sin3 + sin4
    tone = tone / max(tone)

    print("Executando as senoides (emitindo o som)")
    # print("Gerando Tom referente ao símbolo : {}".format(NUM))
    sd.play(tone, fs)
    # Exibe gráficos
    # aguarda fim do audio
    sd.wait()
    # plotFFT(self, signal, fs)
    

if __name__ == "__main__":
    main()

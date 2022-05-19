#!/usr/bin/env python3
"""Show a text-mode spectrogram using live microphone data."""

#importe as bibliotecas
from suaBibSignal import *
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import time
import peakutils

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

#funcao para transformas intensidade acustica em dB
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

def main():
    #declare um objeto da classe da sua biblioteca de apoio (cedida)
    signal = signalMeu()
    #declare uma variavel com a frequencia de amostragem, sendo 44100
    fs = 44100
    
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    
    sd.default.samplerate = fs #taxa de amostragem
    sd.default.channels = 2  #voce pode ter que alterar isso dependendo da sua placa
    
    #declare uma variavel "duracao" com a duracao em segundos da gravacao. poucos segundos ... 
    duration = 2 #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic


    # faca um printo na tela dizendo que a captacao comecará em n segundos. e entao 
    #use um time.sleep para a espera
    input("Pressione Enter quando quiser começar a captação (começa em 5s)")
    time.sleep(1)
    print("4")
    time.sleep(1)
    print("3")
    time.sleep(1)
    print("2")
    time.sleep(1)
    print("1")
    time.sleep(1)
    #faca um print informando que a gravacao foi inicializada
    print("Iniciando captação")
    #calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisicoes)
    numAmostras = fs*duration

    audio = sd.rec(int(numAmostras), fs, channels=1)
    sd.wait()
    print("...     FIM")
    
    #analise sua variavel "audio". pode ser um vetor com 1 ou 2 colunas, lista ...
    #grave uma variavel com apenas a parte que interessa (dados)
    dados = list()
    for amostra in audio:
        dados.append(amostra[0])

    # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!
    t = np.linspace(0, duration, numAmostras)
    

    # plot do gravico  áudio vs tempo!
    plt.figure()
    plt.title("Áudio no tempo")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Intensidade Sonora")
    plt.plot(t, dados)
    plt.show()
    
    # Calcula e exibe o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias
    xf, yf = signal.calcFFT(dados, fs)
    plt.plot(xf,yf)
    plt.grid()
    plt.title('Fourier audio')
    plt.show()
    
    # esta funcao analisa o fourier e encontra os picos
    # voce deve aprender a usa-la. ha como ajustar a sensibilidade, ou seja, o que é um pico?
    # voce deve tambem evitar que dois picos proximos sejam identificados, pois pequenas variacoes na
    # frequencia do sinal podem gerar mais de um pico, e na verdade tempos apenas 1.
   
    index = peakutils.indexes(yf, thres=0.5, min_dist=50)
    
    #printe os picos encontrados!
    
    lista_freq = []
    for freq in xf[index]:
        lista_freq.append(freq)

    print(lista_freq)

    tom_coletado = []
    for f_tabela in FREQUENCIAS:
        for f_teste in lista_freq:
            if f_tabela - 20 < f_teste < f_tabela + 20:
                tom_coletado.append(f_tabela)
    
    print(tom_coletado)
    ["fsaf", "asdf"]

    detectou = False
    for key in TONS:
        tom1 = TONS[key][0]
        tom2 = TONS[key][1]
        i = 0
        j = 1
        while i<len(tom_coletado) - 1:
            while j<len(tom_coletado):
                if (tom_coletado[i]==tom1 and tom_coletado[j]==tom2) or (tom_coletado[i]==tom2 and tom_coletado[j]==tom1):
                    print(f'O dígito escutado foi: {key}')
                    detectou=True
                j += 1
            i+=1
            j=i+1
    if not detectou:
        print("Não consegui detectar nenhum tom :(")
    
if __name__ == "__main__":
    main()
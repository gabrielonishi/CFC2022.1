import time
import utils
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt

from config import Config


def main():

    CONFIG = Config()
    
    sd.default.samplerate = CONFIG.SAMPLE_RATE
    sd.default.channels = CONFIG.CHANNELS
    duration = CONFIG.RECEIVE_TIME

    print("A gravação começará em breve.")
    time.sleep(1)
    print("Gravando...")
    audio = sd.rec(CONFIG.RECEIVE_TIME * CONFIG.SAMPLE_RATE, CONFIG.SAMPLE_RATE, channels=1)
    sd.wait()
    print("Pronto.")
    
    #analise sua variavel "audio". pode ser um vetor com 1 ou 2 colunas, lista ...
    #grave uma variavel com apenas a parte que interessa (dados)
    
    time_array = np.linspace(0, CONFIG.RECEIVE_TIME, CONFIG.RECEIVE_TIME * CONFIG.SAMPLE_RATE)   
    
    ## Calcula e exibe o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias
    #frequencies, intensities = utils.calculate_fft(audio, CONFIG.SAMPLE_RATE)
    
    plt.plot(time_array, audio)
    plt.grid()
    plt.title('Sinal')

    #esta funcao analisa o fourier e encontra os picos
    #voce deve aprender a usa-la. ha como ajustar a sensibilidade, ou seja, o que é um pico?
    #voce deve tambem evitar que dois picos proximos sejam identificados, pois pequenas variacoes na
    #frequencia do sinal podem gerar mais de um pico, e na verdade tempos apenas 1.
   
    #index = peakutils.indexes(,,)
    
    #printe os picos encontrados! 
    
    #encontre na tabela duas frequencias proximas às frequencias de pico encontradas e descubra qual foi a tecla
    #print a tecla.
    
  
    ## Exibe gráficos
    plt.show()

if __name__ == "__main__":
    main()

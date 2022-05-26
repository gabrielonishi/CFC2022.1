import soundfile as sf
import sounddevice as sd
import matplotlib.pyplot as plt
import utils
import numpy as np
import time
import math
import suaBibSignal

def main():
    # 1. Faça a leitura de um arquivo de áudio .wav de poucos segundos (entre 2 e 5) previamente gravado com uma taxa de amostragem de 44100 Hz.
    sinal = suaBibSignal.signalMeu()
    data, sample_rate = sf.read('./Projeto 8/chatuba.wav')
    time = len(data)/sample_rate
    time_array = np.linspace(0, time, len(data))
    # sd.play(data, 48000)
    # sd.wait()

    #Gerando Gráfico 1
    plt.figure("Gráfico 1: Sinal de áudio original normalizado – domínio do tempo")
    plt.plot(time_array, data)
    
    #2. Filtre e elimine as frequências acima de 2500 Hz.
    filtered_data = utils.filtro(data, sample_rate, 2500)

    # Gerando Gráfico 2
    plt.figure("Gráfico 2: Sinal de áudio filtrado – domínio do tempo")
    plt.plot(time_array, filtered_data)

    # Cálculo da FFT
    frequencies, intensities = utils.calculate_fft(filtered_data, sample_rate)

    # Gerando Gráfico 3
    plt.figure("Gráfico 3: Sinal de áudio filtrado – domínio da frequência")
    plt.plot(frequencies, intensities)
    plt.show()

    #3. Reproduza o sinal e verifique que continua audível (com menos qualidade).
    # sd.play(filtered_data, sample_rate)
    # sd.wait()

    #4. Module esse sinal de áudio em AM com portadora de 13.000 Hz. (Essa portadora deve ser uma senoide começando em zero)
    carrier = np.sin(13000*time_array*2*np.pi)
    transmitted_data = carrier*filtered_data
    
    plt.figure("Gráfico 4: sinal de áudio modulado – domínio do tempo")
    plt.plot(time_array, transmitted_data)
    
    # Cálculo da FFT
    t_f, t_i = utils.calculate_fft(transmitted_data, sample_rate)
    plt.figure("Gráfico 5: sinal de áudio modulado – domínio da frequência")
    plt.plot(t_f, t_i)
    plt.show()

    #5. Normalize esse sinal: multiplicar o sinal por uma constante (a maior possível), de modo que todos os pontos 
    #do sinal permaneçam dentro do intervalo[-1,1].
    y_max = max(abs(transmitted_data))
    normalized_transmitted_data = transmitted_data/y_max
    print(max(normalized_transmitted_data))
    print(min(normalized_transmitted_data))

    #6. Execute e verifique que não é perfeitamente audível. 
    sd.play(normalized_transmitted_data)
    sf.write("./Projeto 8/chatuba_encode.wav", normalized_transmitted_data, sample_rate)
    sd.wait()


if __name__ == "__main__":
    main()

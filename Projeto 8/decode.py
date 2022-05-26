#!/usr/bin/env python3
"""Show a text-mode spectrogram using live microphone data."""

#importe as bibliotecas
import utils
import numpy as np
import sounddevice as sd
import soundfile as sf
import matplotlib.pyplot as plt
import time
import peakutils

def main():
    #7. Execute o áudio e peça para que seu colega grave o áudio modulado. 
    data, sample_rate = sf.read("./Projeto 8/chatuba_encode.wav")
    time = len(data)/sample_rate
    time_array = np.linspace(0, time, len(data))
    sd.play(data, sample_rate)

    #8. Verifique que o sinal recebido tem a banda dentro de 10.500 Hz e 15.500 Hz (faça o Fourier).
    frequencies, intensities = utils.calcFFT(data, sample_rate)
    plt.figure("Gráfico 6: Sinal de áudio demodulado - domínio da frequência")
    plt.plot(frequencies, intensities)
    plt.grid()

    #9. Demodule o áudio enviado pelo seu colega.
    carrier = np.sin(13000*time_array*2*np.pi)
    demodulate = carrier * data

    #10. Filtre as frequências superiores a 2.500 Hz.
    chatuba = utils.filtro(demodulate, sample_rate, 2500)

    #11. Execute o áudio do sinal demodulado e verifique que novamente é audível.
    print("Play")
    sd.play(chatuba, sample_rate)
    sd.wait()
        
    print("...     FIM")
    #9. Demodule o áudio enviado pelo seu colega.
    #10. Filtre as frequências superiores a 2.500 Hz.
    #11. Execute o áudio do sinal demodulado e verifique que novamente é audível. 
    
if __name__ == "__main__":
    main()
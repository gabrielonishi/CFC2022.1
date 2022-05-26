import sys
import math
import utils
import sounddevice as sd
import matplotlib.pyplot as plt

def main():
    
    input("Pressione enter para gravar a música")

    # gerador do tom
    frequencies = (CONFIG.TONS[digit][0], CONFIG.TONS[digit][1])
    time_array, tone_array = utils.build_tone(
        frequencies,
        CONFIG.AMPLITUDE,
        CONFIG.TRANSMIT_TIME,
        CONFIG.SAMPLE_RATE
    )

    sd.play(tone_array, CONFIG.SAMPLE_RATE)
    sd.wait()

    # Exibe gráficos
    frequencies, intensities = utils.calculate_fft(tone_array, CONFIG.SAMPLE_RATE)
    plt.show()
    plt.figure(figsize=(12,4))
    plt.subplot(1,2,1)
    plt.plot(time_array[:200], tone_array[:200])
    plt.title('Sinal')
    plt.ylabel('Amplitude')
    plt.xlabel('Tempo (s)')
    plt.grid(True)
    plt.subplot(1,2,2)
    plt.plot(frequencies, intensities)
    plt.title('Transformada de Fourier')
    plt.xlabel('Frequência (Hz)')
    plt.ylabel('Intensidade')
    plt.xlim(0, max(CONFIG.FREQUENCIAS) * 2)
    plt.grid(True)
    plt.show()
    

if __name__ == "__main__":
    main()

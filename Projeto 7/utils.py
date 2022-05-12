import sys
import numpy as np

from scipy import signal as window
from scipy import fftpack


def calculate_fft(signal, fs):
    # https://docs.scipy.org/doc/scipy/reference/tutorial/fftpack.html
    N  = len(signal)
    W = window.hamming(N)
    T  = 1/fs
    xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
    yf = fftpack.fft(signal * W)
    return(xf, np.abs(yf[0:N//2]))


def to_dB(array):
    ''' Converte para dB '''
    return 10 * np.log10(array)


def build_sine(frequency, amplitude, time, sample_rate):
    ''' Construtor de seno '''

    time_array = np.linspace(0, time, time * sample_rate)
    sine_array = amplitude * np.sin(frequency * 2 * np.pi * time_array)

    return (time_array, sine_array)


def build_tone(frequencies, amplitude, time, sample_rate):
    ''' Construtor de tom '''

    tone_array = [0] * sample_rate * time

    for frequency in frequencies:
        time_array, sine_array = build_sine(frequency, amplitude, time, sample_rate)
        tone_array += sine_array

    # atenua para amplitude = 1
    max_value = max(tone_array)
    tone_array = tone_array / max_value

    return time_array, tone_array
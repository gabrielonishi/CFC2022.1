import sys
import numpy as np
import math
import matplotlib.pyplot as plt

from scipy import signal as window
from scipy import fftpack
from scipy import signal as sg
from scipy.fftpack import fft



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

    time_array = np.linspace(0, time, math.ceil(time * sample_rate))
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

def filtro(y, samplerate, cutoff_hz):
# https://scipy.github.io/old-wiki/pages/Cookbook/FIRFilter.html
    nyq_rate = samplerate/2
    width = 5.0/nyq_rate
    ripple_db = 60.0 #dB
    N , beta = sg.kaiserord(ripple_db, width)
    taps = sg.firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))
    yFiltrado = sg.lfilter(taps, 1.0, y)
    return yFiltrado

def generateY(freq, time_array, amplitude=1):
    Y = amplitude*np.sin(freq*time_array*2*np.pi)
    return Y

def calcFFT(signal, fs):
    """
    Calcula a fast-fourier-function para um sinal

    Parâmetros;
        - signal: sinal recebido
        - fs: taxa de amostragem (Hz)
    """
    # https://docs.scipy.org/doc/scipy/reference/tutorial/fftpack.html
    N  = len(signal)
    W = window.hamming(N)
    T  = 1/fs
    xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
    yf = fft(signal*W)
    return(xf, np.abs(yf[0:N//2]))

def plotFFT(signal, fs):
    x,y = calcFFT(signal, fs)
    plt.figure()
    plt.plot(x, np.abs(y))
    plt.title('Fourier')

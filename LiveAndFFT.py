__author__ = 'ericpark'


import numpy as np
from matplotlib import pyplot as plt
import pyaudio
import math


#Configuration

plt.ion()
chunk = 2048
FORMAT = pyaudio.paInt16
CHANNELS = 1

RATE = 16000
RECORD_SECONDS = 60


p = pyaudio.PyAudio()
signal = np.zeros([1,2048])[0]

f, ax = plt.subplots(3, sharex=False)

line, = ax[0].plot(signal)
fftline, = ax[1].plot(signal)

ax[0].axis(ymin=-16000,ymax= 16000)
ax[1].axis(ymin=0,ymax= 1500)
ax[1].axis(xmin=0,xmax= 8000)


x = []
y = []
z = []

fftSpec = []

def amp(X):
    return [abs(x)/1500 for x in X]

def realFFT(X):
    return [abs(x)/(len(X)/2.0) for x in np.fft.rfft(X)]

def iArray(i, arrLength):
    arr = []
    for x in range(len(arrLength)):
        arr.append(i)
    return arr

cm = plt.get_cmap('gist_rainbow')

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=chunk)

for i in range(0, 44100 / chunk * 8 * RECORD_SECONDS):
    dataSpec = stream.read(chunk * 4)
    data = stream.read(chunk)
    data += data
    data += data
    data += data

    signal = np.fromstring(data,'Int16')
    signalSpec = np.fromstring(dataSpec,'Int16')

    FFT = realFFT(signal)
    FFTSpec = realFFT(signalSpec)

    line.set_xdata(np.arange(len(signal)))
    line.set_ydata(signal)

    fftline.set_xdata(np.arange(len(FFT)))
    fftline.set_ydata(FFT)

    ax[2].specgram(FFTSpec, Fs = chunk, cmap=cm)

    plt.draw()


stream.stop_stream()
stream.close()
p.terminate()

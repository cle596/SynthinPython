import math
import numpy
import pyaudio

def sine(frequency, length, rate):
    length = int(length * rate)
    factor = float(frequency) * (math.pi * 2) / rate
    return numpy.sin(numpy.arange(length) * factor)

def empty(length, rate):
    length = int(length * rate)
    return numpy.zeros(length)

def env(type,length,rate):
    env = []
    length = int(length*rate)
    sixteenth = int(length/16)
    eighth = int(length/8)
    half = int(length/2)
    for x in range(0,sixteenth):
        env.append(1/sixteenth*x)
    for x in range(sixteenth,eighth):
        env.append((-.8/sixteenth)*x+1.8)
    for x in range(eighth,half):
        env.append(env[eighth-1])
    for x in range(half,length):
        env.append(-.2/half*x+.4)
    return env

def create_tone(frequency=440, length=1, rate=44100):
    e = env("piano",length,rate)
    chunks = []
    chunks.append(sine(frequency, length, rate))
    chunk = numpy.concatenate(chunks)
    for x in range(0,len(e)):
        chunk[x] *= .8*e[x]
    return chunk.astype(numpy.float32)

def create_empty_tone(length=1,rate=44100):
    chunks = []
    chunks.append(empty(length, rate))
    chunk = numpy.concatenate(chunks)
    return chunk.astype(numpy.float32)

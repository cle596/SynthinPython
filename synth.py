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
    quarter = int(length/4)
    half = int(length/2)
    for x in range(0,quarter):
        env.append(1/quarter*x)
    for x in range(quarter,half):
        env.append((-.5/quarter)*x+1.5)
    for x in range(half,half+quarter):
        env.append(env[half-1])
    for x in range(half+quarter,length):
        env.append(-.5/quarter*x+2)
    return env

def create_tone(freq=[440], length=1, rate=44100):
    e = env("piano",length,rate)
    wavs=[]
    for x in freq:
        wavs.append(1/len(freq)*sine(x,length,rate))
    chunk=sum(wavs)
    """
    for x in range(0,len(e)):
        chunk[x] *= .8*e[x]
    """
    return chunk.astype(numpy.float32)

def create_empty_tone(length=1,rate=44100):
    chunk=empty(length, rate)
    return chunk.astype(numpy.float32)

def create_env(env,domain,equation):
    pass

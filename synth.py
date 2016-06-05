import math
import numpy
import pyaudio

def sine(frequency, length, rate):
    length = int(length * rate)
    factor = float(frequency) * (math.pi * 2) / rate
    return numpy.sin(numpy.arange(length) * factor)

def env(type,length,rate):
    env = []
    length = int(length*rate)
    for x in range(0,int(length/4)):
        env.append(1)
    for x in range(int(length/4),int(length/2)):
        env.append((-.8/int(length/4))*x+1.8)
    for x in range(int(length/2),int(3*length/4)):
        env.append(env[int(length/2)-1])
    for x in range(int(3*length/4),length):
        env.append((-.2/int(length/4))*x+.8)
    return env

def play_tone(stream, frequency=523.251/2, length=1, rate=44100):
    e = env("piano",length,rate)
    chunks = []
    chunks.append(sine(frequency, length, rate)\
        +.1*sine(frequency*2,length,rate)\
        +.1*sine(frequency*5,length,rate)\
        +.05*sine(frequency*7,length,rate)\
    )
    chunk = numpy.concatenate(chunks) * 0.2
    for x in range(0,len(e)):
        chunk[x] *= e[x]
    stream.write(chunk.astype(numpy.float32).tostring())

C5 = 523.251

if __name__ == '__main__':
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1, rate=44100, output=1)

    play_tone(
        stream,
        frequency=C5,
        length=1,
        rate=44100
    )

    stream.close()
    p.terminate()

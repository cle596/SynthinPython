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
    for x in range(0,int(length/16)):
        env.append(1/int(length/16)*x)
    for x in range(int(length/16),int(length/8)):
        env.append((-.8/int(length/16))*x+1.8)
    for x in range(int(length/8),int(length/2)):
        env.append(env[int(length/8)-1])
    for x in range(int(length/2),length):
        env.append(-.2/int(length/2)*x+.4)
    return env

def play_tone(frequency=440, length=1, rate=44100):
    e = env("piano",length,rate)
    chunks = []
    chunks.append(sine(frequency, length, rate))
    chunk = numpy.concatenate(chunks)
    for x in range(0,len(e)):
        chunk[x] *= .8*e[x]
    #stream.write(chunk.astype(numpy.float32).tostring())
    return chunk.astype(numpy.float32)





C5 = 523.251

if __name__ == '__main__':
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1, rate=44100, input=True,output=True,stream_callback=callback)

    play_tone(
        stream,
        frequency=C5,
        length=1,
        rate=44100
    )

    stream.close()
    p.terminate()

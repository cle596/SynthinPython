import sys
import time

from colorama import init
init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
from termcolor import cprint
from pyfiglet import figlet_format

from synth import *
import threading
from queue import Queue
from msvcrt import getch
from time import time,sleep

cprint(figlet_format('twang', font='univers'),'green',attrs=['bold'])
cprint("your favorite synth looper!",'green',attrs=['bold'])
print()

count=0
top=0
samplerate=2*44100
def callback(in_data,frame_count,time_info,status):
    global mytone,count,top
    data = mytone[count:count+frame_count]
    count += frame_count
    data = data.tostring()
    return (data,pyaudio.paContinue)

while True:
    p = pyaudio.PyAudio()

    mytone = create_tone(400,.1,samplerate)

    i=input("twang>")
    if i=="play":
        cprint("press space to play, enter to go back",'green',attrs=['bold'])
        while True:
            key = ord(getch())
            #time1 = time()
            if key == 32: #space

                #time2 = time()
                #print((time2-time1)*1000.0)

                count=0
                try:
                    stream
                except NameError:
                    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=samplerate, output=True,stream_callback=callback,start=False)
                    stream.start_stream()
                else:
                    if stream.is_active():
                        stream.stop_stream()
                        stream = p.open(format=pyaudio.paFloat32, channels=1, rate=samplerate, output=True,stream_callback=callback,start=False)
                        stream.start_stream()
                    else:
                        stream = p.open(format=pyaudio.paFloat32, channels=1, rate=samplerate, output=True,stream_callback=callback,start=False)
                        stream.start_stream()

            if key == 13: #enter
                break

    elif i=="loop":
        t = threading.Thread(target=playloop)
        t.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
        t.start()

    elif i=="quit":
        try:
            stream
        except NameError:
            pass
        else:
            stream.close()
        try:
            p
        except NameError:
            pass
        else:
            p.terminate()
        cprint("ciao!",'green',attrs=['bold'])
        break

    else:
        cprint("option doesn't exist",'green',attrs=['bold'])

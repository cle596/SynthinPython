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
from time import time

cprint(figlet_format('twang', font='univers'),'green',attrs=['bold'])
cprint("your favorite synth looper!",'green',attrs=['bold'])
print()

def playloop():
    pass

while True:
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=1)
    i=input("twang>")
    if i=="play":
        cprint("press space to play, enter to go back",'green',attrs=['bold'])
        while True:
            key = ord(getch())
            time1 = time()
            if key == 32: #space
                time2 = time()
                print((time2-time1)*1000.0)
                play_tone(stream,125,.5,44100)
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

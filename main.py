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
    x=0
    while x<8:
        play_tone(
            stream,
            frequency=C5/3,
            length=.25,
            rate=44100
        )
        time.sleep(.25)
        x+=1

def playloop():
    while True:
        key = ord(getch())
        time1 = time()
        if key == 32: #space
            time2 = time()
            print((time2-time1)*1000.0)
            t = threading.Thread(target=play_tone,args=(stream,C5,.5,44100))
            t.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
            t.start()
        if key == 13: #enter
            break

while True:
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=1)
    i=input("twang>")
    if i=="play":
        cprint("press space to play, enter to go back",'green',attrs=['bold'])
        try:
            t
        except NameError:
            playloop()
        else:
            pass
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

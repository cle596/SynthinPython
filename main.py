import sys
import time

from colorama import init
init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
from termcolor import cprint
from pyfiglet import figlet_format

cprint(figlet_format('twang', font='univers'),'green',attrs=['bold'])
cprint("your favorite synth looper!",'green',attrs=['bold'])

from synth import *

while True:
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=1)
    i=input("twang>")
    if i=="play":
        play_tone(
            stream,
            frequency=C5,
            length=1,
            rate=44100
        )
    if i=="loop":
        x=0
        while x<8:
            play_tone(
                stream,
                frequency=C5,
                length=1,
                rate=44100
            )
            time.sleep(1)
            x+=1

    if i=="quit":
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

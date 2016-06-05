import sys

from colorama import init
init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
from termcolor import cprint
from pyfiglet import figlet_format

cprint(figlet_format('twang', font='univers'),'green',attrs=['bold'])
cprint("your favorite synth looper!",'green',attrs=['bold'])

from synth import *

while True:
    i=input("twang>")
    if i=="play":
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

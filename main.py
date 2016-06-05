import sys
import time

from colorama import init
init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
from termcolor import cprint
from pyfiglet import figlet_format

import threading

from msvcrt import getch
from time import time,sleep

from synth import *

cprint(figlet_format('twang', font='univers'),'green',attrs=['bold'])
cprint("your favorite synth looper!",'green',attrs=['bold'])
print()

count=0
ecount=0
samplerate=44100
def callback(in_data,frame_count,time_info,status):
    global down
    global count, ecount
    global mytone, emptytone
    if down:
        data = mytone[count:count+frame_count]
        if count+frame_count >= .1*samplerate:
            down = False
            count = 0
        else:
            count += frame_count
        data = data.tostring()
    if not down:
        data = emptytone[ecount:ecount+frame_count]
        ecount += frame_count
        data = data.tostring()
    return (data,pyaudio.paContinue)

while True:
    p = pyaudio.PyAudio()
    emptytone = create_empty_tone(8,samplerate)
    mytone = create_tone(800,.1,samplerate)
    down=False

    i=input("twang> ")
    if i=="play":
        cprint("press space to play, enter to go back",'green',attrs=['bold'])
        stream = p.open(
            format=pyaudio.paFloat32, channels=1,
            rate=samplerate, output=True,
            stream_callback=callback,start=False
        )
        stream.start_stream()
        while True:
            key = ord(getch())
            if key == 32: #space
                down = True
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

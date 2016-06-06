import sys
import time

from colorama import init
init(strip=not sys.stdout.isatty())  # strip colors if stdout is redirected
from termcolor import cprint
from pyfiglet import figlet_format

import threading

from msvcrt import getch
from time import time, sleep

from synth import *
from notes import *

import pickle

cprint(figlet_format('twang', font='univers'), 'green', attrs=['bold'])
cprint("your favorite synth looper!", 'green', attrs=['bold'])
print()

count = 0
ecount = 0
samplerate = 44100
notelength = 2


def callback(in_data, frame_count, time_info, status):
    global down
    global count, ecount
    global mytone, emptytone
    global notelength
    if down:
        data = mytone[count:count + frame_count]
        if count + frame_count >= notelength * samplerate:
            down = False
            count = 0
        else:
            count += frame_count
        data = data.tostring()
    if not down:
        data = emptytone[ecount:ecount + frame_count]
        ecount += frame_count
        data = data.tostring()
    return (data, pyaudio.paContinue)

tones = {}
envs = {}
while True:
    p = pyaudio.PyAudio()
    down = False

    i = input("twang>> ")
    if i == "help":
        msg = \
            " tone - synthesize tone\n" +\
            " env - make a new envelope\n" +\
            " play - live synth playback\n" +\
            " loop - put buffer on loop\n" +\
            " quit"
        print(msg)
    elif i == "mem":
        tone_keys = ""
        for x in tones.keys():
            tone_keys += x + '\t' + tones[x]["id"] + '\n'
        print("tones")
        print(tone_keys)
    elif i == "save":
        with open("mem.txt", 'wb') as f:
            pickle.dump(tones, f)
        f.close()
    elif i == "set":
        tone_select = input("select tone: ")
        if tone_select in tones.keys():
            emptytone = create_empty_tone(8, samplerate)
            mytone = tones[tone_select]
        else:
            print("tone doesn't exist in memory.")
    elif i == "tone":
        args = []
        tone_id = input("id: ")
        tone_freq = input("freq: ")
        tone_freq = tone_freq.split(",")
        tone_freq = [notes[x] for x in tone_freq]
        tone_length = int(input("length: "))
        tone_adsr = input("adsr: ")
        tones['t' + str(len(tones))] = {
            'data': create_tone(tone_freq, tone_length),
            'id': tone_id}
    elif i == "env":
        args = []
        env_domain = input("domain: ")
        env_eq = input("equation: ")
        envs.append((env_domain, env_eq))
    elif i == "play":
        cprint("press space to play, enter to go back",
               'green', attrs=['bold'])
        stream = p.open(
            format=pyaudio.paFloat32, channels=1,
            rate=samplerate, output=True,
            stream_callback=callback, start=False
        )
        stream.start_stream()
        while True:
            key = ord(getch())
            if key == 32:  # space
                if down:
                    count = 0
                else:
                    down = True
            if key == 13:  # enter
                break

    elif i == "loop":
        t = threading.Thread(target=playloop)
        # thread dies when main thread (only non-daemon thread) exits.
        t.daemon = True
        t.start()

    elif i == "quit":
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
        cprint("ciao!", 'green', attrs=['bold'])
        break

    else:
        cprint("option doesn't exist", 'green', attrs=['bold'])

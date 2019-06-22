"""Drumbot Play!
Utilizes Python Sonic and Sonic Pi
Check it out at:
https://github.com/gkvoelkl/python-sonic
"""
from psonic import *
import random
from .drumbot import DrumBot

# Initialize DrumBot!
drumbot = DrumBot()
print(drumbot)



def main():
    continue_loop = True
    choice = "Y"
    while continue_loop and choice:
        syncsound()
        cuesound()
        input("Enter to continue")

# Sync and Cue threading on Play
tick = Message()

@in_thread
def syncsound():
    tick.sync()
    while True:
        for i in range(drumbot.step_count):
            for j, track in enumerate(drumbot.tracks):
                if j == -1:
                    s = ''
                else:
                    s = track.name * track.beat[i]
                    s = '' if s == 0 else s
                sample(s)
            sleep(0.25)


@in_thread
def cuesound():
    tick.cue()
    while True:
        for i in range(drumbot.step_count):
            for j, track in enumerate(drumbot.tracks):
                if j == -1:
                    s = track.name * track.beat[i]
                    s = '' if s == 0 else s
                else:
                    s = ''
                sample(s)
            sleep(0.25)


def initialize_drumbot(drumbot):
    # Gather name globals for Sonic Pi
    samples = []
    for key in [key for key in globals().keys()]:
        if "BD" in key:
            samples.append(key)
    # Normalise naming
    for track in drumbot.tracks:
        name = str(track.name.upper())
        # Iterate, randomize choice
        similar = [s for s in samples if name in s]
        if not similar:
            track.name = random.choice(samples)
        else:
            track.name = random.choice(similar)


initialize_drumbot(drumbot)

main()

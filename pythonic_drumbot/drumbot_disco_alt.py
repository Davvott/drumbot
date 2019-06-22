"""Drumbot Play!
Utilizes Python Sonic and Sonic Pi
Check it out at:
https://github.com/gkvoelkl/python-sonic
"""
from psonic import *
import random
from drumbot.pythonic_drumbot.drumbot_py import DrumBot
from threading import Thread, Condition, Event

# Initialize DrumBot!
# tick = Message()  # tick.sync(),tick.cue() inside @in_thread


def main():
    drumbot = DrumBot()
    initialize_drumbot(drumbot)

    condition = Condition()
    stop_event = Event()
    choice = ""
    while not choice:
        print(drumbot)

        thread1 = Thread(name='prod', target=syncsound, args=(condition, stop_event, drumbot))
        thread2 = Thread(name='consumer', target=cuesound, args=(condition, stop_event, drumbot))
        thread1.start()
        thread2.start()

        choice = input("Enter to change drumBot: \n")
        if not choice:
            stop_event.set()

            while stop_event.is_set():
                next_bot = DrumBot()
                initialize_drumbot(next_bot)

            drumbot = next_bot


# Sync and Cue threading on Play
# TODO: Lag in stop_event signal, perhaps implement another stop_event in functions?
def syncsound(condition, stop_event, bot):
    # IF tick or condition inside while loop, looping suffers possibly due to for loops

    with condition:
        condition.wait()
    while not stop_event.is_set():

        for i in range(bot.step_count):
            for j, track in enumerate(bot.tracks):
                if j != -1 and track.beat[i] == 1:
                    sample(track.name)
            sleep(bot.sleep_time)
    stop_event.clear()


def cuesound(condition, stop_event, bot):

    with condition:
        condition.notifyAll()

    while not stop_event.is_set():

        for i in range(bot.step_count):
            for j, track in enumerate(bot.tracks):
                if j == -1 and track.beat[i] == 1:
                    sample(track.name)
            sleep(bot.sleep_time)


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


main()

# samples = [BD_808,
# BD_ADA,
# BD_BOOM,
# BD_FAT,
# BD_GAS,
# BD_HAUS,
# BD_KLUB,
# BD_PURE,
# BD_SONE,
# BD_TEK,
# BD_ZOME,
# BD_ZUM,]
# while True:
#     for s in samples:
#         sample(s)
#         sleep(0.25)
import time

from Printer import Printer
from Keyboard import Keyboard
from Globals import *


def main():
    p = Printer('/dev/ttyUSB0', 250000)
    k = Keyboard()

    last_loop_time = time.time()
    start_time = time.time()
    playing_note = None
    while (1):
        data = k.read()
        for msg in data:
            if msg.command == 144:
                playing_note = msg.note
            elif msg.command == 128 and msg.note == playing_note:
                playing_note = None
        if playing_note:
            p.play_note(playing_note[:-1])
            # p.tune(playing_note[:-1])
            # playing_note = None

        # Loop handling
        delta = time.time() - last_loop_time
        if delta < .25:
            time.sleep(.25 - delta)
        last_loop_time = time.time()


if __name__ == '__main__':
    main()

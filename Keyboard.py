import pygame.midi


class Command(object):
    def __init__(self, midi_msg):
        self.note = pygame.midi.midi_to_ansi_note(midi_msg[0][1])
        self.command = midi_msg[0][0]
        self.timestamp = midi_msg[1]

    def __repr__(self):
        return f"{self.timestamp}: {self.command}: {self.note}"


class Keyboard(object):
    """
    Note Off	128    	0-127 Pitch	     0-127 Velocity
    Note On	    144 	0-127 Pitch	     0-127 Velocity
    """
    def __init__(self):
        pygame.midi.init()
        for i in range(pygame.midi.get_count()):
            print(i, pygame.midi.get_device_info(i))
        self.input = pygame.midi.Input(3)

    def __del__(self):
        if pygame.midi.get_init():
            self.input.close()
        pygame.midi.quit()

    def read(self):
        res = []
        if self.input.poll():
            data = self.input.read(1000)
            for msg in data:
                if msg[0][0] != 248:
                    res.append(Command(msg))
        return res

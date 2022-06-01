class Move(object):
    """ X = head, Y = bed, Z = height """
    def __init__(self, x, y, z, speed=-1):
        self.x = x
        self.y = y
        self.z = z
        self.speed = speed

    def __repr__(self):
        return f"{self.x:.2f}/{self.y:.2f}/{self.z:.2f} - {self.speed}"

    def is_valid(self, bounds):
        if self.x < 0 or self.x > bounds.x or self.y < 0 or self.y > bounds.y or self.z < 0 or self.z > bounds.z:
            return False
        return True


# Approximative, needs to be fine tuned
NOTES_TO_SPEED = {
    "C": 3150,
    "C#": 3340,
    "D": 3535,
    "D#": 3740,
    "E": 3960,
    "F": 4210,
    "F#": 4440,
    "G": 4720,
    "G#": 4997,
    "A": 5285,
    "A#": 5600,
    "B": 5960,
}

NOTE_CHUNK_DURATION_SECS = 0.25

# 0, 0, 0 = Printer left, front, bottom
PRINTER_SIZE = Move(200, 200, 200)
PRINTER_HOME = Move(100, 100, 0, 6000)
PRINTER_CENTER = Move(100, 100, 10, 6000)

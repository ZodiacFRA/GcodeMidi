import serial
import time
import copy
from pprint import pprint

from Globals import *


class Printer(object):
    def __init__(self, port, baud):
        # 100 = slow AF, 1000 = slow, 5000 = normal, 10000 = semi fast, 20000
        # speed in mm/min
        self.port = port
        self.baud = baud
        self.moves = []

        self.ser = serial.Serial(self.port, self.baud)
        time.sleep(2)
        self.send_command("G21\r\n")  # Set distances to mm
        self.send_command("G28\r\n")  # Homing
        self.moves.append(PRINTER_HOME)  # Add homing movement
        self.send_command("G90\r\n")  # Set to Absolute Positioning
        self.send_move(PRINTER_CENTER)
        time.sleep(4)
        print(f"\n\n{'='*50}\n[+] - Starting...")

        self.notes_to_speed = NOTES_TO_SPEED

    def __del__(self):
        self.ser.close()

    def tune(self, note):
        if note not in self.notes_to_speed:
            print("[-] - Invalid note:", note)
            return
        print("Tuning", note)
        cmd = None
        while 1:
            print("-----")
            start_time = time.time()
            while time.time() - start_time < 5:
                self.play_note(note)
            ok_command_flag = False
            while not ok_command_flag:
                try:
                    cmd = input("Exit (e)\nPrint values (p)\n+{int} add int to note speed\n-{int} remove int to note speed\n->")
                    if cmd[0] == "+":
                        v = int(cmd[1:])
                        self.notes_to_speed[note] += v
                        print(f"Added {v} to {note}, now {self.notes_to_speed[note]}")
                    elif cmd[0] == "-":
                        v = int(cmd[1:])
                        self.notes_to_speed[note] -= v
                        print(f"Removed {v} to {note}, now {self.notes_to_speed[note]}")
                    elif cmd[0] == "p":
                        pprint(self.notes_to_speed)
                    elif cmd[0] == "e":
                        print("Play next note now")
                        return
                except:
                    print("Invalid command")
                else:
                    ok_command_flag = True

    def play_note(self, note):
        if note not in self.notes_to_speed:
            print("[-] - Invalid note:", note)
            return
        speed = self.notes_to_speed[note]
        distance = self.get_movement_distance(speed)
        move = copy.copy(self.moves[-1])
        move.speed = speed
        # Try to go in the same direction if possible
        was_going_positive = self.moves[-1].x > self.moves[-2].x
        if was_going_positive:
            # We do have the clearance, go for it
            if move.x + distance < PRINTER_SIZE.x:
                move.x += distance
                self.send_move(move)
            # Impossible single movement for the note, split it into two moves
            else:
                done_distance = PRINTER_SIZE.x - move.x
                move.x = PRINTER_SIZE.x
                self.send_move(move)
                move = copy.copy(move)
                move.x = PRINTER_SIZE.x - (distance - done_distance)
                self.send_move(move)
        else:
            # We do have the clearance, go for it
            if move.x - distance > 0:
                move.x -= distance
                self.send_move(move)
            # Impossible single movement for the note, split it into two moves
            else:
                done_distance = move.x
                move.x = 0
                self.send_move(move)
                move = copy.copy(move)
                move.x = distance - done_distance
                self.send_move(move)

    def send_command(self, command):
        # print("Sending:", command, end='')
        self.ser.write(str.encode(command))
        while True:
            line = self.ser.readline()
            if line == b'ok\n':
                return
            else:
                print(line.decode(), end='')

    def send_move(self, move):
        if not move.is_valid(PRINTER_SIZE):
            print("[-] - Invalid move:", move)
            return
        self.moves.append(move)
        self.send_command(f"G1 X{move.x} Y{move.y} Z{move.z} E0 F{move.speed}\r\n")

    def get_movement_distance(self, speed):
        """
        in: speed (mm/min)
        out: length (mm)
        """
        return (speed / 60) * NOTE_CHUNK_DURATION_SECS

    def get_movement_duration(self, move):
        """
        in: move (mm), speed (mm/min)
        out: time (s)
        """
        distance = abs(self.moves[1].x - move.x)
        return distance / (move.speed / 60)

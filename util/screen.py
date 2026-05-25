import os
import sys

class Screen:
    def __init__(self):
        self.width, self.height = os.get_terminal_size()

    def resize(self):
        self.width, self.height = os.get_terminal_size()

    def clear(self):
        sys.stdout.write("\x1b[2J")

    def check_resize():
        new_w, new_h = os.get_terminal_size()
        return new_w != self.width or new_h != self.height


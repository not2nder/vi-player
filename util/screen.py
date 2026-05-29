import os
import sys

class Screen:
    def __init__(self):
        self.width, self.height = os.get_terminal_size()
    
        self.previous = {}
        self.current = {}

    def draw(self, y, text):
        self.current[y] = text

    def resize(self):
        self.width, self.height = os.get_terminal_size()
        self.previous.clear()

    def clear(self):
        sys.stdout.write("\x1b[2J")
        sys.stdout.write("\x1b[H")
        sys.stdout.flush()

    def render(self):
        for y, text in self.current.items():
            if text != self.previous.get(y):
                sys.stdout.write(move_cursor(y,1)+text)
        
        sys.stdout.flush()
        self.previous = self.current.copy()
        self.current.clear()

def move_cursor(x,y):
    return f"\x1b[{x};{y}H"

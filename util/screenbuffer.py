import sys

class ScreenBuffer:
    def __init__(self):
        self.parts = []

    def add(self, text):
        self.parts.append(text)

    def render(self):
        sys.stdout.write("".join(self.parts))
        sys.stdout.flush()
        self.parts.clear()

class CommandBuffer:
    def __init__(self):
        self.text = ""
        self.cursor = 1

        self.buffer = []
        self.index = 0

    def add(self, value):
        if not value:
            return

        self.buffer.insert(0, value)

    def next(self):
        self.text = self.buffer[self.index]
        
        if self.index < len(self.buffer) - 1:
            self.index += 1
        
        self.cursor = len(self.text)
    
    def prev(self):
        if self.index == 0:
            self.text = ":"
            self.cursor = len(self.text)
            return
        
        if not self.index < 0:
            self.index -= 1

        self.text = self.buffer[self.index]
        self.cursor = len(self.text)
    
    def feed(self, key):
        self.text = self.text[:self.cursor] + key + self.text[self.cursor:]
        self.cursor += len(key)

    def backspace(self):
        if self.cursor > 1:
            self.text = self.text[:self.cursor-1] + self.text[self.cursor:]
            self.cursor -= 1

    def left(self):
        if self.cursor > 1:
            self.cursor -= 1

    def right(self):
        if self.cursor < len(self.text):
            self.cursor += 1

    def clear(self):
        self.text = ""
        self.cursor = 1

    def value(self):
        return self.text

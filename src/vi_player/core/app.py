import signal

from vi_player.core.player import Player

from vi_player.normal.dispatch import InputBuffer, PendingOperator
from vi_player.normal.dispatch import handle_key as normal_handler
from vi_player.command.dispatch import handle_key as command_handler

from vi_player.util.screen import Screen
from vi_player.util import ui

from vi_player.ui.statusline.draw import render as draw_statusline
from vi_player.ui.playlist.draw import render as draw_playlist
from vi_player.ui.commandline.draw import render as draw_commandline
from vi_player.ui.home.draw import render as draw_home

from vi_player.input.keyboard import getch, enter_raw_mode, restore_terminal 
from vi_player.input.mouse import handle_event as mouse_handler, MouseEvent

from vi_player.core.config import load_config, get_config
from vi_player.core.theme import set_theme

from vi_player.core.enums import Mode

class TextInput:
    def __init__(self):
        self.text   = ""
        self.cursor = 1

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

class App:
    def __init__(self):
        self.mpv = Player()
        self.screen = Screen()
        self.dirty = True

        self.mode = Mode.NORMAL

        self.cursor = 0
        self.input = InputBuffer()
        self.pending = PendingOperator()

        self.command = TextInput()
        
        self.message = ""
        
        self.command_buffer = []
        self.hitboxes = {} 

        self.buffer_index = 0

        self.running = True

        load_config()
        self.config = get_config()

        try:
            set_theme(self.config.general["theme"])
        except Exception as e:
            self.message = e

    def run(self):
        ui.initscreen(self.screen)
        signal.signal(signal.SIGWINCH, self.handle_resize)

        fd, old = enter_raw_mode()
        try:
            while self.running:
                if self.dirty:
                    self.draw()

                key = getch(fd)
                if key is None:
                    continue

                self.handle_key(key)
        finally:
            restore_terminal(fd, old)
            ui.exitscreen()

    def handle_resize(self, signum, frame):
        self.screen.resize()
        self.dirty = True
        self.draw()

    def handle_key(self, key):
        if isinstance(key, MouseEvent):
            mouse_handler(self, key)

        match self.mode:
            case Mode.NORMAL:
                normal_handler(self, key)
            case Mode.COMMAND:
                command_handler(self, key)

        self.dirty = True

    def draw(self):
        ui.draw_background(self.screen)
        draw_statusline(self.screen, self)
        
        if self.mpv.isempty:
            draw_home(self.screen, self)
        else:
            draw_playlist(self.screen, self)

        draw_commandline(
            self.screen,
            self.command,
            self.input.display,
            self.message, 
            self.mode
        )

        self.screen.render()
        self.dirty = False 
    
    def buffer_add(self, command:str):
        if command:
            self.command_buffer.insert(0, command)

    def buffer_next(self):
        if self.buffer_index < len(self.command_buffer) - 1:
            self.buffer_index += 1

    def buffer_prev(self):
        if not self.buffer_index < 1:
            self.buffer_index -= 1

    def exit(self):
        self.mpv.exit()
        self.running = False

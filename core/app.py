import signal

from core.player import Player
import util.motions as motions
import util.commands as commands
from util.motions import InputBuffer, PendingOperator

from util.screen import Screen
from util import ui

from ui import statusline, commandline, homescreen, playlist

from util.keyboard import enter_raw_mode, restore_terminal, getch 

from core.config import load_config, get_config
from core.theme import Theme, set_theme

from core.enums import Mode

from core.plugins import PluginHost

class CommandLine:
    def __init__(self):
        self.text = ""
        self.cursor = 1

    def insert(self, char):
        self.text = self.text[:self.cursor] + char + self.text[self.cursor:]
        self.cursor += len(char)

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

        self.commandline = CommandLine()
        self.command_buffer = []

        self.operator = None 
        self.motion   = ""
        
        self.message = ""

        self.buffer_index = 0

        self.running = True
        self.luahost = PluginHost(self)

        self.luahost.load_plugin("luatheme","lua/luatheme.lua")

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
        match self.mode:
            case Mode.NORMAL:
                motions.handle_key(self, key)
            case Mode.COMMAND:
                commands.handle(self, key)

        self.dirty = True

    def draw(self):
        ui.draw_background(self.screen)
        statusline.draw(self.screen, self)
        
        if self.mpv.isempty:
            homescreen.draw(self.screen, self)
        else:
            playlist.draw(self.screen, self)

        commandline.draw(
            self.screen,
            self.commandline,
            self.input.display,
            self.motion,
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

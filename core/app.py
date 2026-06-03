import signal

from core.player import Player
import util.motions as motions
import util.commands as commands

from util.screen import Screen
from util import ui
from ui import statusline

from util.keyboard import getch 

from core.config import load_config, get_config
from core.theme import set_theme

from core.enums import Mode

class App:
    def __init__(self):
        self.mpv = Player()
        self.screen = Screen()
        self.dirty = True

        self.mode = Mode.NORMAL

        self.command = ""
        self.motion = ""
        self.command_buffer = []

        self.cursor = 0
        self.buffer_index = 0

        self.running = True

        load_config()
        self.config = get_config()

        set_theme(self.config.general["theme"])

    def run(self):
        ui.initscreen(self.screen)
        
        signal.signal(signal.SIGWINCH, self.handle_resize)

        try:
            while self.running:
                if self.dirty:
                    self.draw()

                key = getch()
                self.handle_key(key)
        finally:
            ui.exitscreen()

    def handle_resize(self, signum, frame):
        self.screen.resize()
        self.dirty = True
        self.draw()

    def handle_key(self, key):
        if self.mode == Mode.NORMAL:
            motions.handle_key(self, key)
        elif self.mode == Mode.COMMAND:
            commands.handle(self, key)

        self.dirty = True

    def draw(self):
        ui.draw_background(self.screen)
        statusline.draw(self.screen, self)
        
        if self.mpv.isempty:
            ui.draw_home(self.screen, self.config)
        else:
            ui.draw_songs(
                self.screen,
                self.mpv.playlist,
                self.cursor,
                self.config.player["relativenumber"]
            )

        ui.draw_warning(self.screen, self.mpv.state)
        ui.draw_commandline(self.screen, self.command, self.motion, self.mode)

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

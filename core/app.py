import signal

from core.player import Player
import util.motions as motions
import util.commands as commands
from util.screen import Screen
from util import ui
from util.keyboard import getch 
from core.config import *
from core.theme import set_theme

class App:
    def __init__(self):
        self.player = Player()
        self.screen = Screen()
        self.dirty = True

        self.mode = "NORMAL"
        self.command = ""
        self.motion = ""

        self.cursor = 0

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
        self.screen.clear()
        self.screen.resize()
        self.draw()

    def handle_key(self, key):
        if self.mode == "NORMAL":
            motions.handle(self, key)
        elif self.mode == "COMMAND":
            commands.handle(self, key)

    def draw(self):
        ui.draw_background(self.screen)
        ui.draw_header(self.screen)
        ui.draw_songs(self.screen, self.player.get_playlist(), self.cursor, self.config.player["relativenumber"])
        ui.draw_warning(self.screen, self.player.state)
        ui.draw_statusbar(self.screen, self.mode, self.cursor+1, len(self.player.get_playlist()))
        ui.draw_commandline(self.screen, self.command)

        self.screen.render()
        self.dirty = True

    def exit(self):
        self.player.exit()
        ui.exitscreen()
        self.running = False

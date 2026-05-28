from core.player import Player
import util.motions as motions
import util.commands as commands
from util.screen import Screen
from util import ui
from core.config import *
from core.theme import set_theme

class App:
    def __init__(self):
        self.player = Player()
        self.screen = Screen()

        self.mode = "NORMAL"
        self.command = ""
        self.motion = ""

        self.cursor = 0

        self.running = True

        load_config()
        self.config = get_config()
        set_theme(self.config.general["theme"])

        ui.initscreen(self.screen)

    def handle_key(self, key):
        if self.mode == "NORMAL":
            motions.handle(self, key)
        elif self.mode == "COMMAND":
            commands.handle(self, key)

    def draw(self):
        ui.draw_background(self.screen)
        ui.draw_header(self.screen)
        ui.draw_songs(self.screen, self.player.playlist, self.cursor)
        ui.draw_warning(self.screen, self.player.state)
        ui.draw_statusbar(self.screen, self.mode, self.cursor+1, len(self.player.playlist))
        ui.draw_commandline(self.screen, self.command)

        self.screen.render()

    def exit(self):
        self.player.exit()
        self.running = False

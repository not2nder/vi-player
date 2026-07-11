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
from vi_player.core.buffers.cmd import CommandBuffer

class App:
    def __init__(self):
        self.mpv = Player()
        self.screen = Screen()
        self.dirty = True

        self.mode = Mode.NORMAL

        self.cursor = 0

        self.input = InputBuffer()
        self.pending = PendingOperator()

        self.command = CommandBuffer()
        
        self.message = ""
        
        self.hitboxes = {} 

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
    
    def exit(self):
        self.mpv.exit()
        self.running = False

import sys, tty, termios
import shlex

from util import ui
from util.theme import set_theme
from util.config import load_config, get_config, save
from util.screen import Screen
from util.player import Player

import signal

player = Player()

if len(sys.argv) > 1:
    path = sys.argv[1]
    player.load_songs(path)
    songs = player.playlist

load_config()
config = get_config()
set_theme(config.general["theme"])

screen = Screen()

def handle_resize(sigun, frame):
    screen.resize()
    draw()

signal.signal(signal.SIGWINCH, handle_resize)

def getch():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        if ch == "\x1b":
            ch += sys.stdin.read(2)
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

def draw():
    ui.draw_background(screen)
    ui.draw_header(path, screen=screen)
    ui.draw_songs(songs, indicator, screen=screen)
    ui.draw_warning(player.state, screen=screen)
    ui.draw_statusbar(mode, indicator+1, len(songs), screen=screen)
    ui.draw_commandline(command, screen=screen)

    screen.render()
   
ui.initscreen(screen)

command = ""
mode = "NORMAL"
motion = ""

indicator = 0

while True:

    if screen.check_resize:
        screen.resize()

    draw()

    key = getch()

    if mode == "NORMAL":
        if key.isdigit():
            motion+= key
        elif (key == "j" or key == "k") and len(motion) >= 1:
            num = int(motion)
            if key == "j":
                indicator = (indicator+num) % len(songs)
            elif key == "k":
                indicator = (indicator-num) % len(songs)
            motion = ""
            key = ""

        match key:
            case ":":
                mode = "COMANDO"
                command = ":"
            case "h":
                indicator = 0
            case "l":
                if len(songs) > 1:
                    indicator = len(songs) - 1
            case "j":
                if len(songs) > 1:
                    indicator = (indicator+1) % len(songs)
            case "k":
                if len(songs) > 1:
                    indicator = (indicator-1) % len(songs)
            case "q":
                player.exit()
                break

    elif mode == "COMANDO":
        if key == "\r":
            args = shlex.split(command)
            
            if not args:
                mode = "NORMAL"
                command = ""
                continue

            cmd = args[0]

            match cmd:
                case ":p":
                    player.set_current(indicator)
                    player.play()
                case ":pp":
                    player.pause()
                case ":sk":
                    player.skip(int(args[1]))
                    indicator = player.get_current()
                case ":n":
                    player.next()
                    indicator = player.get_current()
                case ":pv":
                    player.prev()
                    indicator = player.get_current()
                case ":q":
                    player.exit()
                    break
                case ":o":
                    songs = player.load_songs(str(args[1]))
                    indicator = player.get_current()
                case ":theme":
                    try:
                        set_theme(args[1])
                    except:
                        pass
                case ":set":
                    attr = args[1]
                    val = args[2]

                    config.set_general(attr, val)
                    if attr == "theme":
                        set_theme(val)
                case _:
                    pass

            command = ""
            mode = "NORMAL"

        elif key == "\x7f": 
            command = command[:-1]
        elif key == "\x1b":
            command = ""
            mode = "NORMAL"
        else:
            command += key

ui.exitscreen()

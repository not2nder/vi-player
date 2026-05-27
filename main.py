import sys, tty, termios
import shlex
from pathlib import Path

import mpv

from util import ui
from util.pretty import length
from util.theme import set_theme
from util.config import load_config, get_config 
from util.screen import Screen

import signal

if len(sys.argv) > 1:
    path = Path(sys.argv[1])
    songs = list(path.glob("*.mp3"))
else:
    path = ""
    songs = []

load_config()
config = get_config()
set_theme(config.theme)

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
    ui.draw_warning(warning, screen=screen)
    ui.draw_statusbar(mode, indicator+1, len(songs), screen=screen)
    ui.draw_commandline(command, screen=screen)

    if mode == "COMANDO":
        ui.show_cursor()
        ui.move_cursor(screen.height, length(command)+1)
    else:
        ui.hide_cursor()

    screen.render()

def play_current():
    global warning
    global current
    global indicator

    song = songs[indicator]
    warning = "TOCANDO"
    player.play(str(song))
    current = indicator

def next_song():
    global current
    global indicator

    current = (current+1) % len(songs)
    indicator = current
    play_current()    

def previous_song():
    global current
    global indicator

    current = (current-1) % len(songs)
    indicator = current
    play_current()

def pause():
    global warning

    if player.pause:
        warning = "TOCANDO"
    else:
        warning = "PAUSA"

    player.pause = not player.pause

def skip(to: int = 1):
    global current
    global indicator

    if not 1 <= to <= len(songs):
        return
    
    current = to - 1
    indicator = current

    play_current()

ui.initscreen(screen)

command = ""
mode = "NORMAL"
warning = "AGUARDANDO"

player = mpv.MPV(video=False)

current = 0
indicator = 0

while True:

    if screen.check_resize:
        screen.resize()

    draw()

    key = getch()

    if mode == "NORMAL":
        match key:
            case ":":
                mode = "COMANDO"
                command = ":"
            case "p":
                mode = "PLAYER"
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
                player.terminate()
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
                    play_current()
                case ":pp":
                    pause()
                case ":sk":
                    if len(args) < 2:
                        skip(1)
                        continue
                    skip(int(args[1]))
                case ":nx":
                    next_song()
                case ":pv":
                    previous_song()
                case ":q":
                    player.terminate()
                    break
                case ":o":
                    path = Path(str(args[1])).expanduser()
                    if path.exists():
                        songs = list(path.glob("*.mp3"))
                        indicator = 0
                case ":theme":
                    try:
                        set_theme(args[1])
                        warning = "Tema da sessão atualizado!"
                    except:
                        warning = f"Tema não encontrado: {args[1]}"
                case _:
                    warning = f"Comando desconhecido: <{cmd}>"
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

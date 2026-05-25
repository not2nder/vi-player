import sys, tty, termios
import shlex
from pathlib import Path

import mpv

from util import ui
from util.pretty import length
from util.theme import set_theme

from util.screen import Screen
from util.screenbuffer import ScreenBuffer

import signal

if len(sys.argv) > 1:
    path = Path(sys.argv[1])
    songs = list(path.glob("*.mp3"))
else:
    path = ""
    songs = []

set_theme("ocean")

screen = Screen()

def handle_resize(sigun, frame):
    screen.clear()
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
    buffer = ScreenBuffer()
    buffer.add(ui.draw_background(screen))
    buffer.add(ui.draw_header(path, screen=screen))
    buffer.add(ui.draw_songs(songs, indicator, screen=screen))
    buffer.add(ui.draw_warning(state, screen=screen))
    buffer.add(ui.draw_statusbar(mode, indicator+1, len(songs), screen=screen))
    buffer.add(ui.draw_commandline(command, screen=screen))

    if mode == "COMANDO":
        buffer.add(ui.show_cursor())
        buffer.add(ui.move_cursor(screen.height, length(command)+1))
    else:
        buffer.add(ui.hide_cursor())

    buffer.render()

def play_current():
    global state
    global current
    global indicator

    song = songs[indicator]
    state = "TOCANDO"
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
    global state

    if player.pause:
        state = "TOCANDO"
    else:
        state = "PAUSA"

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
state = "AGUARDANDO"

player = mpv.MPV(video=False)

current = 0
indicator = 0

draw()
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
                        state="Tema da sessão atualizado!"
                    except:
                        state=f"Tema não encontrado: {args[1]}"
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

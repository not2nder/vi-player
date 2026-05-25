import sys, tty, termios
import shlex
from pathlib import Path

import mpv

from util import ui

if len(sys.argv) > 1:
    path = Path(sys.argv[1])

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
    frame = ""
    frame += ui.draw_header(path)
    frame += ui.draw_songs(songs, indicator)
    frame += ui.draw_warning(state)
    frame += ui.draw_statusbar(mode, indicator+1, len(songs))
    frame += ui.draw_commandline(command)

    sys.stdout.write(frame)
    sys.stdout.flush()

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

ui.initscreen()

command = ""
mode = "NORMAL"
state = "AGUARDANDO"

player = mpv.MPV(video=False)
songs = list(path.glob("*.mp3"))

current = 0
indicator = 0

draw()
while True:
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
                case ":P":
                    pause()
                case ":sk":
                    if len(args) < 2:
                        skip(1)
                        continue
                    skip(int(args[1]))
                case ":nx":
                    next_song()
                case ":q":
                    player.terminate()
                    break
                case ":o":
                    path = Path(str(args[1])).expanduser()
                    if path.exists():
                        songs = list(path.glob("*.mp3"))
                        indicator = 0
                        ui.draw_background()
                case _:
                    pass

            command = ""
            mode = "NORMAL"

        elif key == "\x7f":
            command = command[:-1]
        elif key == "\x1b":
            cmd_buffer.append(command)
            command = ""
            mode = "NORMAL"
        else:
            command += key

ui.exitscreen()

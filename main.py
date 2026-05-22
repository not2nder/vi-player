import sys, tty, termios

import os
import shlex
from pathlib import Path

import mpv

from util import pretty as p
from util import ui

cols, lines = os.get_terminal_size()

pending_next = False

if len(sys.argv) > 1:
    path = Path(sys.argv[1])
else:
    path = Path.home()/"vip"

player = mpv.MPV(video=False)
songs = list(path.glob("*.mp3"))
current = 0

print("\x1b[?1049h",end="")
print("\x1b[?25l", end="")

ui.draw_background()
sys.stdout.flush()

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
    ui.draw_statusbar(path)
    ui.draw_songs(songs, current)
    ui.draw_player(player.pause, mode)
    ui.draw_commandline(command)
    sys.stdout.flush()

def play_current():
    song = songs[current]
    
    player.play(str(song))

def next_song():
    global current

    current = (current+1) % len(songs)

    play_current()    

@player.event_callback("end-file")
def on_end(event):
    global pending_next

    if event.data.reason == "eof":
        pending_next = True

def skip(to: int = 1):
    global current

    if not 1 <= to <= len(songs):
        return
    
    current = to - 1

    play_current()

mode = "NORMAL"
command = ""

draw()
while True:
    if pending_next:
        next_song()
        pending_next = False
    
    draw()

    key = getch()

    if mode == "NORMAL":
        match key:
            case ":":
                mode = "COMMAND"
                command = ":"
            case "h":
                current = 0
            case "l":
                current = len(songs) - 1
            case "j":
                current = (current+1) % len(songs)
            case "k":
                current = (current-1) % len(songs)
            case " ":
                player.pause = not player.pause
            case "q":
                player.terminate()
                break

    elif mode == "COMMAND":
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
                    player.pause = not player.pause
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

print("\x1b[?1049l", end="")

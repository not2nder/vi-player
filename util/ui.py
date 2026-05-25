from pathlib import Path
import mutagen

from util.pretty import *
from util import lexer
from util.theme import get_theme 
from util.screen import Screen

def initscreen(screen: object):
    sys.stdout.write("\x1b[?1049h")
    sys.stdout.write(hide_cursor())
    sys.stdout.write("\x1b[H")
    draw_background(screen)
    sys.stdout.flush()

def exitscreen():
    sys.stdout.write("\x1b[0m")
    sys.stdout.write(show_cursor())
    sys.stdout.write("\x1b[?1049l")
    sys.stdout.flush()

def move_cursor(x,y):
    return f"\x1b[{x};{y}H"

def show_cursor():
    return "\x1b[?25h"

def hide_cursor():
    return "\x1b[?25l"

def draw_background(screen: object):
    theme = get_theme()
    frame = ""
    line = bg(theme.bg)+(" "*screen.width)+RESET

    for y in range(screen.height):
        frame += f"\x1b[{y+1};1H{line}"

    return frame

def draw_header(path: str, screen: object):
    theme = get_theme()
    text = center(f"vi-player {path}", width=screen.width)
    
    line = paint(fill(text, width=screen.width), theme.secondary_fg, theme.secondary_bg) + RESET

    return printf(line, pos="start", screen=screen)

def get_time(song):
    duration = mutagen.File(song).info.length
    mins = int(duration//60)
    secs = int(duration%60)

    return f"{mins}:{str(secs).rjust(2,'0')}" 

def draw_songs(songs: list, current: int, screen: object):
    theme = get_theme()
    frame = ""
    digits = max(2, len(str(len(songs))))
    # frame += draw_background(screen=screen)

    for i, song in enumerate(songs):
        index = str(i+1).rjust(digits)
        songname = Path(song.name).stem
        duration = get_time(song)

        text = f"{justify(songname, padding(duration), width=screen.width-4)}"

        if i == current:
            line = f"{paint(bold(index), theme.inum_fg, theme.inum_bg)} {paint(bold(text), theme.iline_fg, theme.iline_bg)}"
        else:
            line = fill(f"{paint(index, theme.index_fg, theme.index_bg)} {paint(text, theme.fg, theme.bg)}", width=screen.width)
        line += RESET

        frame += printf(line, pos="start", offset=i+2, screen=screen)

    return frame

def draw_statusbar(mode: str, current: int, qtd: int, screen: object):
    theme = get_theme()
    state = f"{current} de {qtd}"
    left = paint(padding(bold(mode)), theme.status_fg, theme.status_bg) 
    right = paint(padding(bold(state)), theme.secondary_fg, theme.secondary_bg)

    line = justify(left, right, width=screen.width)

    return printf(line, pos="end", offset = -1, screen=screen)

def draw_warning(state: str, screen: object):
    theme = get_theme()
    line = paint(padding(bold(state)), theme.warning_fg, theme.warning_bg)
    tail = paint('', theme.fg, theme.bg)
    line = fill(line+tail, width=screen.width)+RESET
    return printf(line, pos="end", offset = -2, screen=screen)

def highlight(text: str): 
    TOKEN_STYLES = {
        "COMMAND": lambda x: x,
        "PATH": lambda x: underline(x),
        "SPACE": lambda x: x,
        "DIGIT": lambda x: x,
        "TEXT": lambda x: x
    }
    result = ""
    for token in lexer.tokenize(text):
        result += TOKEN_STYLES[token.tipo](token.texto)
    return result

def draw_commandline(command: str, screen: object):
    theme = get_theme()
    text = highlight(command)
    line = paint(fill(text, width=screen.width), theme.fg, theme.bg) + RESET
    return printf(line, pos="end", screen=screen)


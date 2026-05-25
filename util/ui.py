from pathlib import Path
import mutagen

from util.pretty import *
from util import lexer
from util.theme import get_current_theme

theme = get_current_theme()

def initscreen():
    sys.stdout.write("\x1b[?1049h")
    sys.stdout.write(hide_cursor())
    sys.stdout.write("\x1b[H")
    draw_background()
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

def draw_background():
    line = bg(theme.bg)+(" "*cols)+RESET

    for y in range(lines):
        sys.stdout.write(f"\x1b[{y+1};1H{line}")

def draw_header(path: str):
    text = center(f"vi-player {path}")
    
    line = paint(fill(text), theme.secondary_fg, theme.secondary_bg) + RESET

    return printf(line, pos="start")

def get_time(song):
    duration = mutagen.File(song).info.length
    mins = int(duration//60)
    secs = int(duration%60)

    return f"{mins}:{str(secs).rjust(2,'0')}" 

def draw_songs(songs: list, current: int):
    frame = ""
    digits = max(2, len(str(len(songs))))
    
    for i, song in enumerate(songs):
        index = str(i+1).rjust(digits)
        songname = Path(song.name).stem
        duration = get_time(song)

        text = f"{songname} {duration}"

        if i == current:
            line = f"{paint(bold(index), theme.index_fg, theme.index_bg)} "+paint(padding(bold(text)), theme.hg_fg, theme.hg_bg)
        else:
            line = paint(fill(f"{index} {text}"), theme.fg, theme.bg)

        line += RESET

        frame += printf(line, pos="start", offset=i+2)

    return frame

def draw_statusbar(mode: str, current: int, qtd: int):
    state = f"{current} de {qtd}"
    left = paint(padding(bold(mode)), theme.statusline_fg, theme.statusline_bg) 
    right = paint(padding(bold(state)), theme.hg_fg, theme.hg_bg)

    line = justify(left, right)

    return printf(line, pos="end", offset = -1)

def draw_warning(state: str):
    line = paint(padding(bold(state)), theme.hg_fg, theme.hg_bg)
    tail = paint('', theme.fg, theme.bg)
    line = fill(line+tail)+RESET
    return printf(line, pos="end", offset = -2)

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

def draw_commandline(command: str):
    text = highlight(command)
    line = paint(fill(text), theme.fg, theme.bg) + RESET
    return printf(line, pos="end")


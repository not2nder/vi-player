from pathlib import Path
import mutagen

from util.pretty import *
from util import Lexer

import tomllib

config_path = Path.home()/".config"/"vi-player"

config_file = config_path/"config.toml"

with open(config_file, "rb") as f:
    config = tomllib.load(f)

default_theme = config["general"]["theme"]

theme_path = config_path/"themes"/f"{default_theme}.toml"

with open(theme_path, "rb") as f:
    theme = tomllib.load(f)

theme_colors= theme["colors"]
PLAYER_BG = theme_colors["bg"]
PLAYER_FG = theme_colors["fg"]

SCD_BG = theme_colors.get("secondary_bg", PLAYER_BG)
SCD_FG = theme_colors.get("secondary_fg", PLAYER_FG)

STATUS_BG = theme_colors.get("statusline_bg", SCD_BG)
STATUS_FG = theme_colors.get("statusline_fg", SCD_FG)

HG_BG = theme_colors.get("highlight_bg", SCD_BG)
HG_FG = theme_colors.get("highlight_fg", SCD_FG)

INDEX_BG = theme_colors.get("index_bg", SCD_BG)
INDEX_FG = theme_colors.get("index_fg", SCD_FG)

COMMAND_BG = theme_colors.get("command_bg", PLAYER_BG)
ARGS_FG = theme_colors.get("args_fg", PLAYER_FG)

def initscreen():
    print("\x1b[?1049h", end="")
    print("\x1b[?125l", end="")
    draw_background()
    sys.stdout.flush()

def exitscreen():
    print("\x1b[?1049l", end="")

def draw_background():
    line = bg(PLAYER_BG)+(" "*cols)+RESET

    for y in range(lines):
        sys.stdout.write(f"\x1b[{y+1};1H{line}")

def draw_header(path: str):
    text = center(f"vi-player {path}")
    
    line = paint(fill(text), SCD_FG, SCD_BG) + RESET

    printf(line, pos="start")

def get_time(song):
    duration = mutagen.File(song).info.length
    mins = int(duration//60)
    secs = int(duration%60)

    return f"{mins}:{str(secs).rjust(2,'0')}" 

def draw_songs(songs: list, current: int):
    digits = max(2, len(str(len(songs))))
    
    for i, song in enumerate(songs):
        index = str(i+1).rjust(digits)
        songname = Path(song.name).stem
        duration = get_time(song)

        text = f"{songname} {duration}"

        if i == current:
            line = f"{paint(bold(index), INDEX_FG, INDEX_BG)} "+paint(padding(bold(text)), HG_FG, HG_BG)
        else:
            line = paint(fill(f"{index} {text}"), PLAYER_FG, PLAYER_BG)

        line += RESET

        printf(line, pos="start", offset=i+2)

def draw_statusbar(mode: str, current: int, qtd: int):
    state = f"{current} de {qtd}"
    left = paint(padding(bold(mode)), STATUS_FG, STATUS_BG) 
    right = paint(padding(bold(state)), HG_FG, HG_BG)

    line = justify(left, right)

    printf(line, pos="end", offset = -1)

def draw_warning(state: str):
    line = paint(padding(bold(state)), HG_FG, HG_BG)
    tail = paint('', HG_BG, HG_FG)
    line = fill(line + tail) + RESET
    printf(line, pos="end", offset = -2)

def highlight(text: str): 
    TOKEN_STYLES = {
        "COMMAND": lambda x: x,
        "PATH": lambda x: underline(x),
        "SPACE": lambda x: x,
        "DIGIT": lambda x: paint(x, ARGS_FG, PLAYER_BG),
        "TEXT": lambda x: x
    }
    result = ""
    for token in Lexer.tokenize(text):
        result += TOKEN_STYLES[token.tipo](token.texto)
    return result

def draw_commandline(command: str):
    text = highlight(command)

    line = paint(fill(text), PLAYER_FG, COMMAND_BG) + RESET
    printf(line, pos="end")


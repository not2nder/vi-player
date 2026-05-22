import os
from pathlib import Path
import mutagen
import shutil

from util.pretty import *

import tomllib

config_path = Path.home()/".config"/"vi-player"

def setup():
    config_path.mkdir(parents=True, exist_ok=True)
    assets = Path(__file__).parent.parent/"assets"
    shutil.copytree(assets, config_path, dirs_exist_ok=True)

config_file = config_path/"config.toml"

setup()

with open(config_file, "rb") as f:
    config = tomllib.load(f)

default_theme = config["general"]["theme"]

theme_path = (Path.home()/".config"/"vi-player"/"themes"/f"{default_theme}.toml")

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

def draw_background():
    line = bg(PLAYER_BG)+(" "*cols)+RESET

    for y in range(lines):
        sys.stdout.write(f"\x1b[{y+1};1H{line}")

def draw_statusbar(path: str):
    text = center(bold(f"vi-player {path}"))
    
    line = paint(
        fill(text),
        SCD_FG,
        SCD_BG
    ) + RESET

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
            line = paint(fill(f"{index} {padding(text)}"), PLAYER_FG, PLAYER_BG)

        line += RESET

        printf(line, pos="start", offset=i+2)

def draw_player(paused: bool, mode: str):
    state = "PAUSA" if paused else "TOCANDO"
    
    left = paint(padding(bold(mode)), STATUS_FG, STATUS_BG)
    right = paint(padding(state), PLAYER_FG, PLAYER_BG)

    line = left+right+RESET

    printf(line, pos="end", offset=-1)

def draw_commandline(command: str):
    line = paint(fill(command), PLAYER_FG, PLAYER_BG) + RESET
    printf(line, pos="end")


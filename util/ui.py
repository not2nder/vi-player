import os
from pathlib import Path
import mutagen

from util.pretty import *

GREEN = "#20c20e"
BLACK = "#000000"
PRIMARY = "#24252d"
TEXT = "#bebebe"
SECONDARY = "#7b99b9"

def draw_statusbar():
    printf(bg(center("vi-player"), GREEN), pos="start")

def get_time(song):
    duration = mutagen.File(song).info.length
    mins = int(duration//60)
    secs = int(duration%60)

    return f"{mins}:{str(secs).rjust(2,'0')}" 

def draw_songs(songs: list, current):
    digits = max(2, len(str(len(songs))))
    
    for i, song in enumerate(songs):
        index = f"{str(i+1).rjust(digits)}"
        songname = Path(song.name).stem
        
        duration = get_time(song)

        text = f"{songname} {duration}"

        if i == current:
            line = f"{fg(bold(index), GREEN)} {bg(padding(bold(text)), GREEN)}"
        else:
            line = f"{index} {text}"

        printf(line, pos="start", offset=i+2)

def draw_player(paused: bool, mode: str):
    state = "PAUSA" if paused else "TOCANDO"
    
    line = bg(padding(mode), GREEN)+fg('', GREEN)

    printf(line, pos="end", offset=-1)

def draw_commandline(command: str):
    printf(f"{command}", pos="end")


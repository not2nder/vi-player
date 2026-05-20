import os

from util.pretty import *

PRIMARY = "#24252d"
TEXT = "#bebebe"
SECONDARY = "#7b99b9"

def draw_statusbar(current: str):
    printf(center(f"{current}"), pos="start")
    printf("─"*cols, pos="start", offset=1)

def draw_songs(songs: list, current):
    digits = max(2, len(str(len(songs))))
    for i, song in enumerate(songs):
        index = f"{str(i+1).rjust(digits)}"

        if i == current:
            text = f"{fg(bold(index), SECONDARY)} {bg(bold(padding(song.name)), SECONDARY)}"
        else:
            text = f"{index} {song.name}"

        line = fill(text)

        printf(line, pos="start", offset=i+2)

def draw_player(paused: bool, mode: str):
    state = "PAUSA" if paused else "TOCANDO"
    
    line = justify(f" {mode}", state)

    printf(bg(line, SECONDARY), pos="end", offset=-1)

def draw_commandline(command: str):
    printf(f">{command}", pos="end")


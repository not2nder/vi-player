import os

from util import pretty as p

MAIN_BACKGROUND = "#24252d"
MAIN_TEXT = "#bebebe"
MAIN_SECONDARY = "#7b99b9"

def draw_statusbar(current: str):
    p.printf(p.center(f"{current}"), pos="start")

    p.printf("-"*p.cols, pos="start", offset=1)

def draw_songs(songs: list, current):
    for i, song in enumerate(songs):
        text = f"{i+1}. {song.name}"
 
        if i == current:
            text = p.reverse(text)

        line = p.fill(text)

        p.printf(line, pos="start", offset=i+2)

def draw_player(paused: bool, mode: str):
    state = "PAUSA" if paused else "TOCANDO"
    text = p.justify(state, f"[{mode} MODE]")

    p.printf(p.colorize(text, MAIN_BACKGROUND), pos="end", offset=-1)

def draw_commandline(command: str):
    p.printf(f"MUSIC>{command}", pos="end")

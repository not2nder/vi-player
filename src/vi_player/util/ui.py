from vi_player.util.pretty import *
from vi_player.core.theme import get_theme 

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

def show_cursor():
    return "\x1b[?25h"

def hide_cursor():
    return "\x1b[?25l"

def draw_background(screen: object):
    theme = get_theme()
    normal = theme.style("Normal")

    line = bg(normal["bg"]) + (" "*screen.width) + RESET

    for y in range(screen.height):
        screen.draw(y+1,line)

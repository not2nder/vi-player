from vi_player.util.pretty import *
from vi_player.core.theme import get_theme 

def initscreen(screen: object):
    sys.stdout.write("\x1b[?1049h") # alternate screen
    sys.stdout.write("\x1b[?25h")   # hide text cursor
    sys.stdout.write("\x1b[?1000h") # activate mouse reporting
    sys.stdout.write("\x1b[?1006h") # sgr mouse mode
    draw_background(screen)
    sys.stdout.flush()

def exitscreen():
    sys.stdout.write("\x1b[0m")
    sys.stdout.write("\x1b[?25h")
    sys.stdout.write("\x1b[?1049l")
    sys.stdout.write("\x1b[?1000l")
    sys.stdout.write("\x1b[?1006l")
    sys.stdout.flush()

def draw_background(screen: object):
    theme = get_theme()
    normal = theme.style("Normal")

    line = bg(normal["bg"]) + (" "*screen.width) + RESET

    for y in range(screen.height):
        screen.draw(y + 1,line)

from vi_player.util.pretty import *
from vi_player.core.theme import get_theme 

def initscreen(screen: object):
    sys.stdout.write("\x1b[?1049h") # alternate screen
    sys.stdout.write("\x1b[?25l")   # hide text cursor
    sys.stdout.write("\x1b[?1000h") # activate mouse reporting
    sys.stdout.write("\x1b[?1006h") # sgr mouse mode
    draw_background(screen)
    sys.stdout.flush()

def exitscreen():
    sys.stdout.write("\x1b[0m")
    sys.stdout.write("\x1b[?25h")   # show text cursor
    sys.stdout.write("\x1b[?1049l") # exit alternate screem
    sys.stdout.write("\x1b[?1000l") # disable mouse reporting
    sys.stdout.write("\x1b[?1006l") # disable sgr mouse mode
    sys.stdout.flush()

def show_cursor():
    sys.stdout.write("\x1b[?25h")   # show text cursor

def hide_cursor():
    sys.stdout.write("\x1b[?25l")   # show text cursor

def set_cursor(value):
    sys.stdout.write(f"\x1b[{value} q")

def draw_background(screen: object):
    theme = get_theme()
    normal = theme.style("Normal")

    line = bg(normal["bg"]) + (" "*screen.width) + RESET

    for y in range(screen.height):
        screen.draw(y + 1,line)

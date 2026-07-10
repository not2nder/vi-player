from vi_player.util.pretty import *
from vi_player.core.theme import get_theme
from vi_player.core.enums import Mode
from vi_player.util.ui import show_cursor, hide_cursor, set_cursor

def render(screen, command, motion, message, mode):
    theme = get_theme()
    style = theme.style("Normal")

    if mode == Mode.COMMAND:
        show_cursor()

        cursor_y = screen.height
        cursor_x = command.cursor

        set_cursor(2 if cursor_x >= len(command.text) else 5)

        line = paint(
            fill(command.text, width=screen.width),
            style
        ) + RESET + move_cursor(cursor_y, cursor_x)
        
    elif mode == Mode.NORMAL:
        hide_cursor()
        freespace = screen.width - len(motion) - 1
        text = justify(truncate(message, freespace), motion, width=screen.width-1)
    
        line = paint(
            fill(text, width=screen.width),
            style
        ) + RESET
        
    screen.draw(screen.height, line)

def move_cursor(line, col):
    return f"\x1b[{line};{col + 1}H"


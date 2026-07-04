from vi_player.util.pretty import *
from vi_player.core.theme import get_theme
from vi_player.ui import ascii as art

def draw(screen, app):
    theme = get_theme()
    title = [
        "VI-PLAYER v0.0.1",
        "",
        "A Vim-like music player for the terminal",
        "https://github.com/not2nder",
    ]

    commands = [
        (f":o <dir>", "Open a directory"),
        (f":q", "Quit"),
    ]

    navigation = [
        ("j / k", "Move cursor"),
        ("gg / G", "First / Last song"),
        ("h / l", "Seek backward / forward"),
    ]

    WIDTH = max(len(t) for t in title)

    total_lines = (len(title)
        +len(commands)
        +len(navigation)
        +2
    )

    start_y = (screen.height-total_lines)//2

    start_y = build_text(screen, title, start_y, WIDTH)
    start_y = build_hr(screen, start_y, WIDTH)
    start_y = build_table(screen, commands, start_y, WIDTH)
    start_y = build_hr(screen, start_y, WIDTH)
    start_y = build_table(screen, navigation, start_y, WIDTH)

def build_text(screen, lines, start, max_width):
    theme = get_theme()
    style = theme.style("Normal")

    for line in lines:
        text = paint(
            center(line, width=screen.width),
            style
        )
        screen.draw(start, text)
        start += 1

    return start

def build_table(screen, lines, start, max_width):
    theme = get_theme()

    for cmd, desc in lines:
        row = cmd + desc.rjust(max_width-length(cmd))

        text = paint(
            center(row, width=screen.width),
            theme.style("Normal")
        )

        screen.draw(start, text)
        start += 1
    
    return start

def build_hr(screen, start, max_width, char="─"):
    theme = get_theme()
    
    hr = char*max_width 
    screen.draw(
        start,
        paint(center(hr, width=screen.width),
            theme.style("Muted")
        )
    )
    return start+1

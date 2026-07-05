from vi_player.util.pretty import *
from vi_player.core.theme import get_theme
from vi_player import __version__

def render(screen, app):
    theme = get_theme()

    normal_style = theme.style("Normal")
    muted_style  = theme.style("Muted")

    title = [
        f"VI-PLAYER {__version__}",
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
        + len(commands)
        + len(navigation)
        + 3
    )

    start_y = (screen.height-total_lines)//2

    start_y = build_text(screen, title, start_y, normal_style)
    start_y = build_hr(screen, start_y, WIDTH, muted_style)
    start_y = build_table(screen, commands, start_y, WIDTH, normal_style)
    start_y = build_hr(screen, start_y, WIDTH, muted_style)
    start_y = build_table(screen, navigation, start_y, WIDTH, normal_style)
    start_y = build_hr(screen, start_y, WIDTH, muted_style)

def build_text(screen, lines, start, style):
    for line in lines:
        text = paint(
            center(line, width=screen.width),
            style
        )
        screen.draw(start, text)
        start += 1

    return start

def build_table(screen, lines, start, max_width, style):
    for cmd, desc in lines:
        row = cmd + desc.rjust(max_width - length(cmd))

        text = paint(
            center(row, width=screen.width),
            style
        )

        screen.draw(start, text)
        start += 1
    
    return start

def build_hr(screen, start, max_width, style):
    hr = "─" * max_width 
    screen.draw(
        start,
        paint(
            center(hr, width=screen.width),
            style
        )
    )
    return start+1

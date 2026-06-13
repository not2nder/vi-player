from util.pretty import *
from core.theme import get_theme
import ui.ascii as art

def draw(screen, app):
    theme = get_theme()
    
    logo = ["VI-PLAYER", "v0.1.0"] if screen.width <= len(art.logo[1])-2 else art.logo

    descricao = [
        "Um player de músicas inspirado no Vim",
        "https://github.com/not2nder"
    ]
    commands = [
        (f"digite  :help<Enter>", "para ajuda"),
        (f"digite  :e<Enter>", "abrir playlist"),
        (f"digite  :q<Enter>", "para sair"),
    ]

    WIDTH = 40

    total_lines = len(logo)+len(descricao)+len(commands)

    start_y = (screen.height-total_lines)//2
    start_y = build_text(screen, logo, start_y, WIDTH)
    start_y = build_hr(screen, start_y, WIDTH)
    start_y = build_text(screen, descricao, start_y, WIDTH)
    start_y = build_hr(screen, start_y, WIDTH)
    start_y = build_table(screen, commands, start_y, WIDTH)
    start_y = build_hr(screen, start_y, WIDTH)

def build_text(screen, lines, start, max_width):
    theme = get_theme()
    style = theme.style("normal")

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
            theme.style("normal")
        )

        screen.draw(start, text)
        start += 1
    
    return start

def build_hr(screen, start, max_width):
    theme = get_theme()
    
    hr = "─"*max_width 
    screen.draw(
        start,
        paint(center(hr, width=screen.width),
            theme.style("muted")
        )
    )
    return start+1

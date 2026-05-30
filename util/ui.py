from util.pretty import *
from util import lexer
from core.theme import get_theme 

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
    line = bg(theme.bg)+(" "*screen.width)+RESET

    for y in range(screen.height):
        screen.draw(y+1,line)

def draw_home(screen: object, config: object):

    titulo = [
        "vi-player v0.0.1",
        "Um player de música inspirado no Vim",
    ]

    motions = [
        ("j/k:", "baixo e cima"),
        ("gg/G:", "início e fim"),
        ("50%:", "meio da playlist"),
    ]

    commands = [
        ('digite  '+bold(':help'), "para mostrar ajuda"),
        ('digite  '+bold(':q'), "para sair"),
        ('digite  '+bold(':theme'), "para mudar tema")
    ]

    total_lines = len(titulo)+len(motions)+len(commands)+2
    start_y = (screen.height-total_lines)//2
    
    max_width = max(length(cmd+desc) for cmd, desc in commands)
    
    start_y = draw_centered_lines(screen, titulo, start_y)+1
    start_y = draw_centered_table(screen, motions, start_y, max_width)+1
    start_y = draw_centered_table(screen, commands, start_y, max_width)+1
    draw_centered_lines(screen, [f"Tema: {config.general['theme']}"], start_y)

def draw_centered_lines(screen, lines, start):
    theme = get_theme()
    
    for line in lines:
        text = center(line, width=screen.width)
        text = paint(text, theme.fg, theme.bg)
        screen.draw(start, text)
        start += 1

    return start

def draw_centered_table(screen, lines, start, max_width):
    theme = get_theme()

    for cmd, desc in lines:
        row = justify(cmd, desc, width=max_width)
        text = center(row, width=screen.width)
        text = paint(text, theme.fg, theme.bg)

        screen.draw(start, text)
        start += 1

    return start

def draw_header(screen: object):
    theme = get_theme()
    text = center("vi-player", screen.width)
    
    line = paint(fill(text, width=screen.width), theme.secondary_fg, theme.secondary_bg) + RESET

    screen.draw(1, line)

def draw_songs(screen: object, songs: list, cursor: int, relative: bool):

    theme = get_theme()
    digits = max(2, len(str(len(songs))))

    for i, song in enumerate(songs):

        if relative and i != cursor:
            display_number = str(abs(i - cursor)).rjust(digits)
        elif not relative:
            display_number = str(i+1).rjust(digits)
        else:
            display_number = str(i+1).ljust(digits)

        index = padding(display_number)
        duration = padding(song.get_time())

        freespace = screen.width - length(index) - length(duration)

        text = f"{justify(truncate(song.title, freespace-1), duration, width=screen.width-4)}"

        if i == cursor:
            line = f"{paint(bold(index), theme.inum_fg, theme.inum_bg)}{paint(bold(text), theme.iline_fg, theme.iline_bg)}"
        else:
            line = fill(f"{paint(index, theme.index_fg, theme.index_bg)}{paint(text, theme.fg, theme.bg)}", width=screen.width)
        line += RESET
        
        screen.draw(i+3, line)
       
def draw_statusbar(screen: object, app: object):
    theme = get_theme()
    right = ""

    if app.player.playlist:
        right = paint(
            padding(bold(f"{app.cursor+1}/{app.player.count}")),
            theme.secondary_fg,
            theme.secondary_bg)

    song = app.player.get_current_song()
    text = app.mode.value+f" | {song.get_name() if song else 'Sem Música'}"
    
    left = paint(padding(bold(text)), theme.status_fg, theme.status_bg) 

    line = justify(left, right, width=screen.width)
    screen.draw(screen.height-1, line)

def draw_warning(screen: object, state: str):
    if state is None:
        return

    theme = get_theme()
    line = paint(padding(bold(state.value)), theme.warning_fg, theme.warning_bg)
    tail = paint('', theme.fg, theme.bg)
    line = fill(line+tail, screen.width)

    screen.draw(screen.height-2, line)

def highlight(text: str): 
    TOKEN_STYLES = {
        "COMMAND": lambda x: x,
        "PATH": lambda x: underline(x),
        "SPACE": lambda x: x,
        "DIGIT": lambda x: bold(x),
        "TEXT": lambda x: x
    }
    result = ""
    for token in lexer.tokenize(text):
        result += TOKEN_STYLES[token.tipo](token.texto)
    return result

def draw_commandline(screen: object, command: str):
    theme = get_theme()
    text = highlight(command)
    line = paint(fill(text, width=screen.width), theme.fg, theme.bg) + RESET
    
    screen.draw(screen.height, line)


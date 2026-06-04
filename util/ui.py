from util.pretty import *
from util import lexer
from core.theme import get_theme 
from core.enums import Mode

TOP_MARGIN = 2
WARNING_Y= 1
STATUS_Y = 1
COMMAND_Y = 1

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

def draw_songs(screen: object, songs: list, cursor: int, relative: bool):

    theme = get_theme()
    digits = max(2, len(str(len(songs))))
    
    visible_lines = (
        screen.height
        -TOP_MARGIN
        -WARNING_Y
        -STATUS_Y
        -COMMAND_Y
    )

    scroll = max(0, cursor-visible_lines//2)
    max_scroll = max(0, len(songs), visible_lines)
    scroll = min(scroll, max_scroll)

    visible_songs = songs[scroll:scroll+visible_lines]

    for i, song in enumerate(visible_songs):
        real_index = scroll+i

        if relative and real_index != cursor:
            display_number = str(abs(real_index - cursor)).rjust(digits)
        elif not relative:
            display_number = str(real_index+1).rjust(digits)
        else:
            display_number = str(real_index+1).ljust(digits)

        index = padding(display_number)
        duration = padding(song.time)

        freespace = screen.width - length(index) - length(duration)

        text = f"{justify(truncate(song.title, freespace-1), duration, width=screen.width-4)}"

        if real_index == cursor:
            line = f"{paint(bold(index), theme.inum_fg, theme.inum_bg)}{paint(bold(text), theme.iline_fg, theme.iline_bg)}"
        else:
            line = fill(f"{paint(index, theme.index_fg, theme.index_bg)}{paint(text, theme.fg, theme.bg)}", width=screen.width)
        line += RESET
        
        screen.draw(TOP_MARGIN+i, line)

    for i in range(visible_lines):
        if i >= len(visible_songs):
            text = bold("~ ")
            line = paint(fill(text, width=screen.width), theme.index_fg, theme.bg)
            screen.draw(TOP_MARGIN+i, line)

def draw_statusbar(screen: object, app: object):
    theme = get_theme()
    mode = app.mode.value
    musica = app.mpv.playing_song.name

    left = [
        mode,
        musica
    ]
    right = ["6/7"]

    line = build_statusline(left, right, width=screen.width)
        
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
        result += TOKEN_STYLES[token.token_type](token.text)
    return result

def draw_commandline(screen, command, motion, mode):
    theme = get_theme()
    if mode == Mode.COMMAND:
        text = highlight(command)
    elif mode == Mode.NORMAL:
        text = motion.rjust(screen.width-2)
    
    line = paint(fill(text, width=screen.width), theme.fg, theme.bg) + RESET
    
    screen.draw(screen.height, line)


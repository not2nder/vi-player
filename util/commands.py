import shlex
from core.theme import set_theme, get_theme
import core.config as config
from core.enums import Mode, Key
from util.pretty import paint 

def error(text):
    theme = get_theme()

    return paint(
        text,
        theme.style("Error")
    )

def warning(text):
    theme = get_theme()

    return paint(
        str(text),
        theme.style("Warning")
    )

def skip(app, args):
    if app.mpv.isempty:
        return

    app.mpv.skip(int(args[1]))
    app.cursor = app.mpv.current

def quit(app, args):
    app.exit()

def open_dir(app, args):
    if len(args) < 2:
        app.message = warning("Nenhum nome de diretório")
        return
    
    app.mpv.playlist.load_directory(args[1])
    app.message = f"Mostrando músicas de: {args[1]}"
    app.cursor = 0

def add_dir(app, args):
    if len(args) < 2:
        app.message = warning("Nenhum nome de diretório")
        return

    count = app.mpv.playlist.add_dir(args[1])

    if count:
        app.message = f'{count} Música(s) adicionada(s)'
    else:
        app.message = warning('Diretório vazio ou inexistente')

def add_song(app, args):
    if len(args) < 2:
        return

    app.mpv.playlist.add(Song(args[1]))
    app.message = "Música adicionada!"

def set_rnu(app, args):
    app.config.set_relativenumber()

def disable_rnu(app, args):
    app.config.set_relativenumber(False)

def set_colorscheme(app, args):
    if len(args) < 2:
        app.message = f"tema: '{get_theme().meta['name']}' de {get_theme().meta['author']}"
        return

    try:
        set_theme(args[1])
    except Exception as e:
        app.message = warning(e)

COMMANDS = {
    ":sk": skip,
    ":e": open_dir,
    ":add": add_dir,
    ":addsong": add_song,
    ":rnu": set_rnu,
    ":relativenumber": set_rnu,
    ":nornu": disable_rnu,
    ":norelativenumber": disable_rnu,
    ":colorscheme": set_colorscheme,
    ":q": quit
}

def handle(app, key):
    if key == Key.ENTER:
        args = shlex.split(app.command.value())
        cmd = args[0]

        command = COMMANDS.get(cmd)
        
        if command:
            command(app, args)
            app.buffer_add(app.command.value())
        else:
            app.message = warning(f"Não é um comando do player: {cmd.strip(':')}")

        app.command.clear()
        app.mode = Mode.NORMAL

    elif key == Key.ESC:
        app.command.clear()
        app.mode = Mode.NORMAL
        return

    elif key == Key.DEL:
        if app.command.value() != ":":
            app.command.backspace()
        else:
            app.command.clear()
            app.mode = Mode.NORMAL 

    elif key == Key.UP and len(app.command_buffer) > 0:
        app.command.text = app.command_buffer[app.buffer_index]
        app.buffer_next()
        app.command.cursor = len(app.command.text)

    elif key == Key.DOWN and len(app.command_buffer) > 0:
        if app.buffer_index == 0:
            app.command.text = ":"
        else:
            app.buffer_prev()
            app.command.text = app.command_buffer[app.buffer_index]
            app.command.cursor = len(app.command.text)

    elif key == Key.LEFT:
        app.command.left()
    
    elif key == Key.RIGHT:
        app.command.right()

    elif isinstance(key, str):
        app.command.feed(key)

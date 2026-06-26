import shlex
from core.theme import set_theme, get_theme
import core.config as config
from core.enums import Mode, Key
from util.pretty import error

def play(app, args):
    if app.mpv.isempty:
        return

    app.mpv.current = app.cursor
    app.mpv.play()

def pause(app, args):
    if app.mpv.isempty:
        return

    app.mpv.pause()

def next(app, args):
    if app.mpv.isempty:
        return

    app.mpv.next()
    app.cursor = app.mpv.current

def prev(app, args):
    if app.mpv.isempty:
        return

    app.mpv.prev()
    app.cursor = app.mpv.current

def skip(app, args):
    if app.mpv.isempty:
        return

    app.mpv.skip(int(args[1]))
    app.cursor = app.mpv.current

def quit(app, args):
    app.exit()

def open_dir(app, args):
    if len(args) < 2:
        return
    
    app.mpv.playlist.load_directory(args[1])
    app.message = f"Mostrando músicas de: {args[1]}"

def add_dir(app, args):
    if len(args) < 2:
        app.message = error("Nenhum nome de diretório")
        return

    count = app.mpv.playlist.add_dir(args[1])

    if count:
        app.message = f'{count} Música(s) adicionada(s)'
    else:
        app.message = error('Diretório vazio ou inexistente')

def add_song(app, args):
    if len(args) < 2:
        return

    app.mpv.playlist.add(Song(args[1]))
    app.message = "Música adicionada!"

def command_set(app, args):
    if len(args) < 2:
        app.message = "Uso: ':set opção=valor'"
        return

    text = " ".join(args)
    try:
        apply_set(app, text[5:])
        app.message = " ".join(args)
    except Exception as e:
        app.message = error(e)

def apply_set(app, expr):
    if '=' in expr:
        name, value = expr.split("=",1)
    else:
        value = ""
        name = shlex.split(expr)[0]

    name = get_alias(name)

    match name:
        case "playlist":
            app.config.set_playlist_fmt(value)

        case "relativenumber":
            app.config.set_relativenumber(True)
        case "norelativenumber":
            app.config.set_relativenumber(False)
        case "relativenumber!":
            app.config.set_relativenumber()

        case "number":
            app.config.set_number(True)
        case "nonumber":
            app.config.set_number(False)
        case "number!":
            app.config.set_number()

        case "wrap":
            app.config.set_wrap(True)
        case "nowrap":
            app.config.set_wrap(False)
        case "wrap!":
            app.config.set_wrap()

        case _:
            raise Exception(f"Opção desconhecida: {name}")

def get_alias(name):
    aliases = {
        "rnu": "relativenumber",
        "nornu": "norelativenumber",
        "rnu!": "relativenumber!",

        "nu": "number",
        "nonu": "nonumber",
        "nu!": "number!",
    }

    return aliases.get(name, name)

def set_colorscheme(app, args):
    if len(args) < 2:
        app.message = f"tema: '{get_theme().meta['name']}' de {get_theme().meta['author']}"
        return

    try:
        set_theme(args[1])
        app.message = " ".join(args)
    except Exception as e:
        app.message = error(e)

def luatheme(app, args):
    if len(args) < 2:
        app.message = f"Uso: ':lt random | current | grep'"
        return

    match args[1]:
        case "random":
            app.luahost.plugins["luatheme"].random()
        case "current":
            app.luahost.plugins["luatheme"].current()
        case "ls":
            app.luahost.plugins["luatheme"].count()
        case "grep":
            if len(args) < 3:
                app.message = "Uso: ':lt grep texto'"
                return

            app.luahost.plugins["luatheme"].grep(args[2])
        case _:
            app.message = f"LuaTheme: Opção inválida '{args[1]}'"

COMMANDS = {
    ":p": play,
    ":pp": pause,
    ":n": next,
    ":pv": prev,
    ":sk": skip,
    ":e": open_dir,
    ":set": command_set,
    ":add": add_dir,
    ":addsong": add_song,
    ":colorscheme": set_colorscheme,
    ":lt": luatheme,
    ":q": quit
}

#with open("lua/autopairs.lua", "r") as f:
#    autopairs = lua.execute(f.read())
#    api = ViPlayerAPI(app)
#    lua.globals()["viplayer"] = api

#def plugin_handler(app, key):
#    ctx = {
#        "mode": app.mode.name,
#        "text": app.commandline.text,
#        "cursor": app.commandline.cursor
#    }

#    handled = autopairs.on_key(ctx, key)
#    app.commandline.text = ctx["text"]
#    app.commandline.cursor = ctx["cursor"]

#    return handled

def handle(app, key):
    if key == Key.ENTER:
        args = shlex.split(app.commandline.value())
        cmd = args[0]

        command = COMMANDS.get(cmd)
        
        if command:
            command(app, args)
            app.buffer_add(app.commandline.value())
        else:
            app.message = error(f"Não é um comando do player: {cmd.strip(':')}")

        app.commandline.clear()
        app.mode = Mode.NORMAL

    elif key == Key.ESC:
        app.commandline.clear()
        app.mode = Mode.NORMAL
        return

    elif key == Key.DEL:
        if app.commandline.value() != ":":
            app.commandline.backspace()
        else:
            app.commandline.clear()
            app.mode = Mode.NORMAL 

    elif key == Key.UP and len(app.command_buffer) > 0:
        app.commandline.text = app.command_buffer[app.buffer_index]
        app.buffer_next()
        app.commandline.cursor = len(app.commandline.text)

    elif key == Key.DOWN and len(app.command_buffer) > 0:
        if app.buffer_index == 0:
            app.commandline.text = ":"
        else:
            app.buffer_prev()
            app.commandline.text = app.command_buffer[app.buffer_index]
            app.commandline.cursor = len(app.commandline.text)
    
    elif key == Key.LEFT:
        app.commandline.left()
    
    elif key == Key.RIGHT:
        app.commandline.right()

    elif isinstance(key, str):
    #    if plugin_handler(app, key):
    #        return

        app.commandline.insert(key)


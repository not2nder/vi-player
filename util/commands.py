import shlex
from core.theme import set_theme
import core.config as config
from core.enums import Mode, Key

def play(app, args):
    if not app.mpv.playlist:
        return

    app.mpv.current = app.cursor
    app.mpv.play()

def pause(app, args):
    if not app.mpv.playlist:
        return

    app.mpv.pause()

def next(app, args):
    if not app.mpv.playlist:
        return

    app.mpv.next()
    app.cursor = app.mpv.current

def prev(app, args):
    if not app.mpv.playlist:
        return

    app.mpv.prev()
    app.cursor = app.mpv.current
        

def skip(app, args):
    if not app.mpv.playlist:
        return

    app.mpv.skip(int(args[1]))
    app.cursor = app.mpv.current

def quit(app, args):
    app.quit()

def open(app, args):
    if len(args) < 2:
        return
    
    app.mpv.playlist.load_directory(args[1])

def add_dir(app, args):
    if len(args) < 2:
        return

    app.mpv.playlist.add_dir(args[1])

def add_song(app, args):
    if len(args) < 2:
        return

    app.mpv.playlist.add(Song(args[1]))

def set_rnu(app, args):
    app.config.set_relativenumber()

def disable_rnu(app, args):
    app.config.set_relativenumber(False)

def set_theme(app, args):
    if len(args) < 2:
        return

    set_theme(args[1])

COMMANDS = {
    ":p": play,
    ":pp": pause,
    ":n": next,
    ":pv": prev,
    ":sk": skip,
    ":open": open,
    ":add": add_dir,
    ":addsong": add_song,
    ":rnu": set_rnu,
    ":relativenumber": set_rnu,
    ":nornu": disable_rnu,
    ":norelativenumber": disable_rnu,
    ":colorscheme": set_theme,
    ":q": quit
}

def handle_key(app, key):
    if isinstance(key, str) and key == "\r":
        args = shlex.split(app.command)
        cmd = args[0]

        command = COMMANDS.get(cmd)
        
        if command:
            command(app, args)

        app.command = ""
        app.mode = Mode.NORMAL
    
    elif key == Key.DEL:
        if app.command != ":":
            app.command = app.command[:-1]
        else:
            app.command = ""
            app.mode = Mode.NORMAL 

    elif key == Key.UP and len(app.command_buffer) > 0:
        app.command = app.command_buffer[app.buffer_index]
        app.buffer_next()

    elif key == Key.DOWN and len(app.command_buffer) > 0:
        if app.buffer_index == 0:
            app.command = ":"
        else:
            app.buffer_prev()
            app.command = app.command_buffer[app.buffer_index]
    else:
        app.command += key


import shlex
from core.theme import set_theme
import core.config as config
from core.enums import Mode, Key

def handle(app, key):
    if isinstance(key, str) and key == "\r":
        args = shlex.split(app.command)

        if not args:
            app.mode = Mode.NORMAL
            app.command = ""
            return

        cmd = args[0]

        if cmd == ":p":
            app.mpv.current = app.cursor
            app.mpv.play()

        elif cmd == ":pp":
            app.mpv.pause()

        elif cmd == ":n":
            app.mpv.next()
            app.cursor = app.mpv.current

        elif cmd == ":open":
            if len(args) > 1:
                app.mpv.playlist.load_directory(args[1])

        elif cmd == ":add":
            if len(args) > 1:
                app.mpv.playlist.add_dir(args[1])

        elif cmd == ":addsong":
            if len(args) > 1:
                try:
                    app.mpv.playlist.add(Song(args[1]))
                except:
                    pass

        elif cmd == ":pv":
            app.mpv.prev()
            app.cursor = app.mpv.current
        
        elif cmd == ":sk":
            app.mpv.skip(int(args[1]))
            app.cursor = app.mpv.current

        elif cmd[0] == ":" and cmd[1:].isdigit():
            app.cursor = int(cmd[1:]) -1

        elif cmd == ":colorscheme":
            if len(args) > 1:
                try:
                    set_theme(args[1])
                except:
                    pass

        elif cmd in (":rnu", ":relativenumber"):
            app.config.set_relativenumber()

        elif cmd in (":nornu", ":norelativenumber"):
            app.config.set_relativenumber(False)

        elif cmd == ":q":
            app.exit()
            return

        else:
            pass

        if app.command.startswith(":"):
            app.buffer_add(app.command)
        
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

    elif isinstance(key, str):
        app.command += key

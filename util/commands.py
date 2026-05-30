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
            app.player.current = app.cursor
            app.player.play()

        elif cmd == ":pp":
            app.player.pause()

        elif cmd == ":n":
            app.player.next()
            app.cursor = app.player.current

        elif cmd == ":pv":
            app.player.prev()
            app.cursor = app.player.current
        
        elif cmd == ":sk":
            app.player.skip(int(args[1]))
            app.cursor = app.player.current

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

        elif cmd == ":usearrows":
            app.config.set_arrows()

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
        app.command = app.command[:-1]

    elif key == Key.UP and len(app.command_buffer) > 0:
        app.command = app.command_buffer[app.get_buffer_index()]
        app.buffer_next()

    elif key == Key.DOWN and len(app.command_buffer) > 0:
        if app.get_buffer_index() == 0:
            app.command = ":"
        else:
            app.buffer_prev()
            app.command = app.command_buffer[app.get_buffer_index()]

    elif isinstance(key, str):
        app.command += key

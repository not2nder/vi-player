import shlex
from core.theme import set_theme
import core.config as config

def handle(app, key):
    if key == "\r":
        args = shlex.split(app.command)

        if not args:
            app.mode = "NORMAL"
            app.command = ""
            return

        cmd = args[0]

        if cmd == ":p":
            app.player.set_current(app.cursor)
            app.player.play()

        elif cmd == ":pp":
            app.player.pause()

        elif cmd == ":n":
            app.player.next()
            app.cursor = app.player.get_current()

        elif cmd == ":pv":
            app.player.prev()
            app.cursor = app.player.get_current()
        
        elif cmd == ":sk":
            app.player.skip(int(args[1]))
            app.cursor = app.player.get_current()

        elif cmd[0] == ":" and cmd[1:].isdigit():
            app.cursor = int(cmd[1:]) -1

        elif cmd == ":colorscheme":
            if len(args) > 1:
                try:
                    set_theme(args[1])
                except:
                    pass

        elif cmd == ":rnu" or cmd == ":relativenumber":
            app.config.set_relativenumber()

        elif cmd == ":nornu" or cmd == ":norelativenumber":
            app.config.set_relativenumber(False)

        elif cmd == ":usearrows":
            app.config.set_arrows()

        elif cmd == ":q":
            app.exit()
            return
        
        else:
            pass
        app.command = ""
        app.mode = "NORMAL"

    elif key == "\x7f":
        app.command = app.command[:-1]
    else:
        app.command += key

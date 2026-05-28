import shlex

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

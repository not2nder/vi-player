from core.enums import Mode, Key

def handle(app, key):
    use_arrows = app.config.player["usearrows"]

    if isinstance(key, str) and key.isdigit():
        app.motion += key
        return

    elif (key == 'j' or key == 'k') and app.motion:
        steps = int(app.motion)
        
        if key == 'j':
            move_down(app, steps)
        elif key == 'k':
            move_up(app, steps)

        app.motion = ""
        return

    elif key == 'j' or (use_arrows and key == Key.DOWN):
        move_down(app)

    elif key == 'k' or (use_arrows and key == Key.UP):
        move_up(app)

    elif key == 'g':
        if app.motion:
            goto_start(app)
        else:
            app.motion += key
            return

    elif key == 'G':
        goto_end(app)

    elif key == '%' and app.motion:
        percent = int(app.motion)/100
        app.cursor = int(app.mpv.count * percent)
        app.motion = ""
   
    elif key == 'q':
        app.exit()
    
    elif key == ":":
        enter_command(app)
        return

    app.motion = ""

def move_down(app, steps=1):
    if not app.mpv.playlist:
        return

    app.cursor = (app.cursor+steps) % app.mpv.count

def move_up(app, steps=1):
    if not app.mpv.playlist:
        return
    
    app.cursor = (app.cursor-steps) % app.mpv.count

def goto_start(app):
    if not app.mpv.playlist:
        return

    app.cursor = 0

def goto_end(app):
    if not app.mpv.playlist:
        return

    app.cursor = app.mpv.count-1

def enter_command(app):
    app.mode = Mode.COMMAND
    app.command += ":"

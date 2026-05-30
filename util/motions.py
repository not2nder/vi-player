from core.enums import Mode, Key

def handle(app, key):
    use_arrows = app.config.player["usearrows"]

    if not app.player.playlist: 
        return

    if isinstance(key, str) and key.isdigit():
        app.motion+= key
        return

    elif (key == 'j' or key == 'k') and app.motion:
        num = int(app.motion)
        if key == 'j':
            app.cursor = (app.cursor+num) % app.player.count
        elif key == 'k':
            app.cursor = (app.cursor-num) % app.player.count
        
        app.motion = ""
        return

    elif key == 'j' or (use_arrows and key == Key.DOWN):
        app.cursor = (app.cursor+1) % app.player.count

    elif key == 'k' or (use_arrows and key == Key.UP):
        app.cursor = (app.cursor-1) % app.player.count
    
    elif key == 'g':
        if app.motion:
            app.cursor = 0
        else:
            app.motion += key
            return

    elif key == 'G':
        app.cursor = app.player.count -1
    
    elif key == '%' and app.motion:
        percent = int(app.motion)/100
        app.cursor = int(app.player.count * percent)
        app.motion = ""
   
    elif key == 'q':
        app.exit()
    
    elif key == ":":
        app.mode = Mode.COMMAND
        app.command += key
        return

    app.motion = ""

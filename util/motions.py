def handle(app, key):
    if key.isdigit():
        app.motion+= key
        return

    elif (key == 'j' or key == 'k') and len(app.motion) >= 1:
        num = int(app.motion)
        if key == 'j':
            app.cursor = (app.cursor+num) % len(app.player.playlist)
        elif key == 'k':
            app.cursor = (app.cursor-num) % len(app.player.playlist)
        
        app.motion = ""
        return

    elif key == 'j' or (key == 'DOWN' and app.config.player['usearrows']):
        app.cursor = (app.cursor+1)%len(app.player.playlist)
    elif key == 'k' or (key == 'UP' and app.config.player['usearrows']):
        app.cursor = (app.cursor-1)%len(app.player.playlist)
    elif key == 'g':
        if len(app.motion) == 1:
            app.cursor = 0
        else:
            app.motion += key
            return
    elif key == 'G':
        app.cursor = len(app.player.playlist)-1
    
    elif key == '%' and len(app.motion) >=1:
        percent = int(app.motion)/100
        app.cursor = int(len(app.player.playlist)*percent)
        app.motion = ""
    elif key == ':':
        app.mode = "COMMAND"
        app.command += key
        return
    elif key == 'q':
        app.exit()
    
    app.motion = ""

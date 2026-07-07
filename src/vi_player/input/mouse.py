from vi_player.core.enums import Mode

def handle_event(app, event):
    if not event.pressed:
        return

    if event.button != 0:
        return

    hitbox = app.hitboxes.get(event.y)

    if hitbox is None:
        return

    if hitbox["field"] == "song":
        index = hitbox["index"]

        app.cursor = index
        app.mpv.current = index
        app.mpv.play()
    
    if hitbox["field"] == "empty":
        app.cursor = app.mpv.count - 1

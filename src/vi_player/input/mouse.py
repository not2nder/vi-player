from dataclasses import dataclass
from vi_player.core.enums import Mode

@dataclass(slots=True)
class MouseEvent:
    button: int
    x: int
    y: int
    pressed: bool
    released: bool

def parse_mouse(data):
    if not data.startswith(b'\x1b[<'):
        return None

    final = data[-1:]

    if final not in (b'M', b'm'):
        return None

    body = data[3:-1]

    try:
        button, x, y = map(int, body.split(b';'))
    except ValueError:
        return None

    return MouseEvent(
        button=button,
        x = x - 1,
        y = y - 1,
        pressed=final == b'M',
        released=final == b'm',
    )

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

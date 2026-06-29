from vi_player.core.enums import Key
from vi_player.command.keys import *

def key_dispatch(app, key):
    if key in KEY_EVENTS:
        KEY_EVENTS[key](app)

def handle_key(app, key):
    if isinstance(key, Key):
        key_dispatch(app, key)
        return

    elif isinstance(key, str):
        app.command.feed(key)

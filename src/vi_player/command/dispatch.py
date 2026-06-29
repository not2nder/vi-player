import shlex

from vi_player.core.enums import Key
from vi_player.command.ex import *
from vi_player.command.events import *

def key_dispatch(app, key):
    if key in KEY_EVENTS:
        KEY_EVENTS[key](app)

def handle_key(app, key):
    if key == Key.ENTER:
        args = shlex.split(app.command.value())
        cmd = args[0]

        command = COMMANDS.get(cmd)
        
        if command:
            command(app, args)
            app.buffer_add(app.command.value())
        else:
            app.message = f"Não é um comando do player: {cmd.strip(':')}"

        app.command.clear()
        app.mode = Mode.NORMAL

    if isinstance(key, Key):
        key_dispatch(app, key)
        return

    elif isinstance(key, str):
        app.command.feed(key)

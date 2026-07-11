import shlex

from vi_player.core.enums import Key, Mode
from vi_player.command.ex import EX_COMMANDS

def return_to_normal(app):
    app.command.clear()
    app.mode = Mode.NORMAL

def cmd_backspace(app):
    if app.command.value() != ":":
        app.command.backspace()
    else:
        return_to_normal(app)

def b_next(app):
    app.command.next()

def b_prev(app):
    app.command.prev()

def cmd_left(app):
    app.command.left()

def cmd_right(app):
    app.command.right()

def do_cmd(app):
    try:
        args = shlex.split(app.command.value())
    except ValueError as e:
        app.message = str(e)
        return_to_normal(app)
        return

    cmd = args[0]

    command = EX_COMMANDS.get(cmd)
    app.command.add(app.command.value())
    
    if command:
        command(app, args)
    else:
        app.message = f"Invalid command: {cmd.strip(':')}"

    app.command.clear()
    app.mode = Mode.NORMAL

KEY_EVENTS = {
    Key.ESC: return_to_normal,

    Key.UP: b_next,
    Key.DOWN: b_prev,
    
    Key.DEL: cmd_backspace,
    Key.LEFT: cmd_left,
    Key.RIGHT: cmd_right,
    
    Key.ENTER: do_cmd,
}

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
        app.command.clear()
        app.mode = Mode.NORMAL 

def b_next(app):
    if len(app.command_buffer) > 0:
        app.command.text = app.command_buffer[app.buffer_index]
        app.buffer_next()
        app.command.cursor = len(app.command.text)

def b_prev(app):
    if len(app.command_buffer) < 1:
        return

    if app.buffer_index == 0:
        app.command.text = ":"
    else:
        app.buffer_prev()
        app.command.text = app.command_buffer[app.buffer_index]
        app.command.cursor = len(app.command.text)

def cmd_left(app):
    app.command.left()

def cmd_right(app):
    app.command.right()

def do_cmd(app):
    args = shlex.split(app.command.value())
    cmd = args[0]

    command = EX_COMMANDS.get(cmd)
    
    if command:
        command(app, args)
        app.buffer_add(app.command.value())
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

from core.enums import Mode, Key
from util.motions import exit_player

def seek_foward(app):
    app.mpv.jump(10)

def seek_back(app):
    app.mpv.jump(-10)

def seek_home(app):
    app.mpv.seek_start()

def enter_command(app):
    app.mode = Mode.COMMAND
    app.command = ":"

def enter_normal(app):
    app.mode = Mode.NORMAL

def pause(app):
    app.mpv.pause()

MOVES = {
    "l": seek_foward,
    "h": seek_back,
    "0": seek_home,
    ":": enter_command,
    "q": exit_player,
    " ": pause
}

def handle(app, key):
    action = MOVES.get(key)
    if action:
        action(app)

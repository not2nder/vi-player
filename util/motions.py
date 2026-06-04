from dataclasses import dataclass
from core.enums import Mode, Key

@dataclass
class Motion:
    count: int
    action: str

def parse(motion: str):
    if not motion:
        return

    cursor = 0
    indice = 0
    count = 1
    action = ""
    
    if motion[0].isdigit():
        while cursor < len(motion) and motion[cursor].isdigit():
            cursor+=1
        indice = cursor

        count = int(motion[:indice])

    action = motion[indice:]

    return Motion(count, action)

def move_down(app, motion):
    if app.mpv.isempty:
        return

    app.cursor = (app.cursor+motion.count) % app.mpv.count

def move_up(app, motion):
    if app.mpv.isempty:
        return
    
    app.cursor = (app.cursor-motion.count) % app.mpv.count

def goto_start(app, motion):
    if app.mpv.isempty:
        return

    app.cursor = 0

def goto(app, motion):
    if app.mpv.isempty:
        return

    percent = motion.count/100
    app.cursor = int(app.mpv.count * percent)

def goto_end(app, motion):
    if app.mpv.isempty:
        return

    app.cursor = app.mpv.count-1

def enter_command(app, motion):
    app.mode = Mode.COMMAND
    app.command += ":"

def exit_player(app, motion):
    app.exit()

MOTIONS = {
    "j": move_down,
    "k": move_up,
    "gg": goto_start,
    "G": goto_end,
    "%": goto,
    ":": enter_command,
    "q": exit_player 
}

def iscomplete(motion: object):
    if not motion:
        return 
    
    if str(motion).isdigit():
        return False
    else:
        return True

def isvalid(motion: str):
    if not motion:
        return

    if motion.isdigit():
        return True

    action = parse(motion).action
    return any(i.startswith(action) for i in MOTIONS)

def handle_key(app, key):
    
    if isinstance(key, str):
        app.motion += key
    else:
        return

    if not isvalid(app.motion):
        app.motion = ""
        return

    obj = parse(app.motion)

    if iscomplete(obj):
        move = MOTIONS.get(obj.action)
        if move:
            move(app, obj)
            app.motion = ""


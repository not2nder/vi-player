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

def handle(app, key):
    use_arrows = app.config.player["usearrows"]

    if isinstance(key, str) and key.isdigit():
        app.motion += key
        return
    
    elif key == 'g':
        if app.motion:
            goto_start(app)
        else:
            app.motion += key
            return

    app.motion = ""

def move_down(app, motion):
    if app.mpv.is_empty:
        return

    app.cursor = (app.cursor+motion.count) % app.mpv.count

def move_up(app, motion):
    if app.mpv.is_empty:
        return
    
    app.cursor = (app.cursor-motion.count) % app.mpv.count

def goto_start(app, motion):
    if app.mpv.is_empty:
        return

    app.cursor = 0

def goto(app, motion):
    if app.mpv.is_empty:
        return

    percent = motion.count/100
    app.cursor = int(app.mpv.count * percent)

def goto_end(app, motion):
    if app.mpv.is_empty:
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

def is_complete(motion: str):
    if not motion:
        return 
    
    if motion.isdigit() or parse(motion).action not in MOTIONS:
        return False
    else:
        return True

def handle_key(app, key):
    
    if isinstance(key, str):
        app.motion += key
    
    if is_complete(app.motion):
        obj = parse(app.motion)
        move = MOTIONS.get(obj.action)
        
        if move:
            move(app, obj)

        app.motion = ""

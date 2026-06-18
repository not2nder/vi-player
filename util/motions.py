from dataclasses import dataclass
from core.enums import Mode, Key 

@dataclass(slots=True)
class Motion:
    count: int = 1
    action: str = ""

@dataclass(slots=True)
class Operator:
    count: int
    action: str

@dataclass(slots=True)
class Parsed:
    count: int
    key: str

@dataclass(slots=True)
class NormalCommand:
    operator: Operator | None = None
    motion: Motion | None = None

    def clear(self):
        self.motion = None

# PARSER
def parse(value):
    if not value:
        return None

    cursor = 0
    count = 1
    
    while cursor < len(value) and value[cursor].isdigit():
        cursor+=1
    
    if cursor:
        count = int(value[:cursor])

    action = value[cursor:]

    if not action:
        return Motion(count)

    if action in MOTIONS:
        return Motion(count, action)

    if action in OPERATORS:
        return Operator(count, action)

    return None

# MOVIMENTOS
def down(app, motion):
    if app.mpv.isempty:
        return

    return (app.cursor+motion.count) % app.mpv.count

def up(app, motion):
    if app.mpv.isempty:
        return
    
    return (app.cursor-motion.count) % app.mpv.count

def start(app, motion):
    if app.mpv.isempty:
        return

    return 0

def end(app, motion):
    if app.mpv.isempty:
        return

    return app.mpv.count-1

def goto(app, motion):
    if app.mpv.isempty:
        return

    percent = min(motion.count,99)/100
    return int(app.mpv.count * percent)

# AÇÕES
def play(app):
    app.mpv.current = app.cursor
    app.mpv.play()

def seek_forward(app):
    app.mpv.jump(10)

def seek_back(app):
    app.mpv.jump(-10)

def seek_home(app):
    app.mpv.seek_start()

def enter_command(app):
    app.mode = Mode.COMMAND
    app.command += ":"
    app.message = ""

def cut(app, motion):
    app.mpv.playlist.clear_register()

    for _ in range(app.cursor, app.cursor+motion.count):
        app.mpv.playlist.cut(app.cursor)

    if app.cursor >= app.mpv.count:
        app.cursor = app.mpv.count-1

# OPERAÇÕES
def paste(app, motion):
    app.mpv.playlist.paste(app.cursor)

def exit_player(app, motion):
    app.exit()

MOTIONS = {
    "j": down,
    "k": up,

    "gg": start,
    
    "G": end,
    "%": goto
}

OPERATORS = {
    "d": cut,
    "p": paste
}

ACTIONS = {
    "l": seek_forward,
    "h": seek_back,
    "0": seek_home,
    ":": enter_command,
    "q": exit_player
}

def isprefix(value):
    if not value:
        return False

    parsed = parse(value)

    if parsed and parsed.action == "":
        return True

    if parsed and parsed.action in MOTIONS:
        return True

    return any(
        key.startswith(value)
        for key in MOTIONS
    )

def iscomplete(value):
    parsed = parse(value)
    if not parsed:
        return False

    return parsed.action in MOTIONS

def execute(app, command):
    motion = command.motion

    if not motion:
        return

    func = MOTIONS.get(motion.action)

    if not func:
        return

    target = func(app, motion)

    if target is not None:
        app.cursor = max(
            0,
            min(target, app.mpv.count-1)
        )

def handle_key(app, key):   
    if key == Key.ENTER:
        play(app)
        return

    if not isinstance(key, str): 
        return

    app.input += key

    parsed = parse(app.input)

    if app.input in ACTIONS:
        ACTIONS[app.input](app)
        app.input = ""
        return 

    if not isprefix(app.input):
        app.input = ""
        app.pending.clear()
        return

    motion = parse(app.input)
    
    if motion:
        app.pending.motion = motion

    if not iscomplete(app.input):
        return

    execute(app, app.pending)

    app.pending.clear()
    app.input = ""


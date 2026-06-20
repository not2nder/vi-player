from dataclasses import dataclass
from core.enums import Mode, Key 

from enum import Enum, auto

class CommandType(Enum):
    MOTION = auto()
    OPERATOR = auto()
    ACTION = auto()
    INVALID = auto()
    INCOMPLETE = auto()

class Operator(Enum):
    NONE = auto()
    DELETE = auto()
    YANK = auto()

@dataclass
class OperatorArgument:
    operator: str | None = None

    count: int = 1
    motion: Motion | None = None

    start: int = 0
    end: int = 0

    @property
    def active(self):
        return self.operator != Operator.NONE

    def clear(self):
        self.operator = None
        self.motion = None
        self.count = 1

@dataclass(slots=True)
class Motion:
    count: int = 1
    action: str = ""

@dataclass(slots=True)
class Parsed:
    count: int
    key: str

@dataclass(slots=True)
class Command:
    command_type: CommandType
    key: str
    count: int = 1

class InputBuffer:
    def __init__(self):
        self.value = ""

    def feed(self, key):
        self.value += key
        return parse(self.value)

    def clear(self):
        self.value = ""

def parse(value):
    if not value:
        return None

    cursor = 0
    count = 1
    
    while cursor < len(value) and value[cursor].isdigit():
        cursor+=1
    
    if cursor:
        count = int(value[:cursor])

    key = value[cursor:]
    
    if key in MOTIONS:
        return Command(CommandType.MOTION, key, count)

    if key in ACTIONS:
        return Command(CommandType.ACTION, key, count)
    
    if isprefix(key) or key == "":
        return Command(CommandType.INCOMPLETE, key, count)

    return Command(CommandType.INVALID, key, count)

def down(app, motion):
    if app.mpv.isempty:
        return

    return (app.cursor+motion.count) % app.mpv.count

def up(app, motion):
    if app.mpv.isempty:
        return
    
    return (app.cursor-motion.count) % app.mpv.count

def goto(app, motion):
    if app.mpv.isempty:
        return

    return motion.count-1

def end(app, motion):
    if app.mpv.isempty:
        return

    return app.mpv.count-1

def percent(app, motion):
    if app.mpv.isempty:
        return

    percent = min(motion.count,99)/100
    return int(app.mpv.count * percent)


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

def cut(app, start, end):
    app.mpv.playlist.clear_register()
    #TO DO

def paste(app, motion):
    app.mpv.playlist.paste(app.cursor)

def exit_player(app):
    app.exit()

MOTIONS = {
    "j": down,
    "k": up,

    "gg": goto,
    
    "G": end,
    "%": percent
}

OPERATORS = {
    "d": Operator.DELETE,
    "p": Operator.YANK
}

ACTIONS = {
    "l": seek_forward,
    "h": seek_back,
    ":": enter_command,
    "q": exit_player,
}

def isprefix(value):
    if not value:
        return False

    if value.isdigit():
        return True

    return any(
        key.startswith(value)
        for key in MOTIONS
    )

def nv_motion(app, command):
    motion = Motion(
        action = command.key,
        count  = command.count
    ) 

    func = MOTIONS.get(motion.action)

    if func is None:
        return

    target = func(app, motion)

    if target is not None:
        app.cursor = max(
            0,
            min(target, app.mpv.count-1)
        )

def nv_action(app, command):
    ACTIONS[command.key](app)
    app.input.clear()

def nv_dispatch(app, command):
    if command is None:
        return

    match command.command_type:
        case CommandType.ACTION:
            nv_action(app, command)

        case CommandType.MOTION:
            nv_motion(app, command)
            app.input.clear()

        case CommandType.INCOMPLETE:
            return

        case CommandType.INVALID:
            app.input.clear()

def handle_key(app, key):   
    if key == Key.ENTER:
        play(app)
        return

    if not isinstance(key, str): 
        return

    command = app.input.feed(key)

    if command:
        nv_dispatch(app, command)

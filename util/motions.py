from dataclasses import dataclass
from core.enums import Mode, Key 

from enum import Enum, auto

class CommandType(Enum):
    MOTION = auto()
    OPERATOR = auto()
    ACTION = auto()
    INVALID = auto()
    INCOMPLETE = auto()

class OperatorType(Enum):
    DELETE = auto()
    YANK = auto()
    NONE = auto()

@dataclass(slots=True)
class PendingOperator:
    operator: OperatorType = OperatorType.NONE
    count: int = 1

    def clear(self):
        self.operator = OperatorType.NONE
        self.count = 1

@dataclass(slots=True)
class Operator:
    count: int = 1
    action: OperatorType = OperatorType.NONE

@dataclass(slots=True)
class Motion:
    count: int = 1
    action: str = ""

@dataclass(slots=True)
class Command:
    command_type: CommandType
    value: object

@dataclass(slots=True)
class Action:
    key: str

class InputBuffer:
    def __init__(self):
        self.value = ""
        self.display = ""

    def feed(self, key, pending=False):
        self.value += key
        self.display += key
        return parse(self.value, pending)

    def clear(self):
        self.value = ""

    def clear_display(self):
        self.display = ""

def parse(value, pending=False):
    if not value:
        return None

    cursor = 0
    count = 1
    
    while cursor < len(value) and value[cursor].isdigit():
        cursor+=1
    
    if cursor:
        count = int(value[:cursor])

    key = value[cursor:]
    
    if pending:
        if key in MOTIONS:
            return Command(
                CommandType.MOTION,
                Motion(count, key)
            )

        if key == "":
            return Command(
                CommandType.INCOMPLETE,
                key
            )
    
    if key in OPERATORS:
        return Command(
            CommandType.OPERATOR,
            Operator(count, OPERATORS[key])
        )

    if key in ACTIONS:
        return Command(
            CommandType.ACTION,
            Action(key)
        )
    
    if key in MOTIONS:
        return Command(
            CommandType.MOTION,
            Motion(count, key)
        )

    
    if key == "" or isprefix(key):
        return Command(CommandType.INCOMPLETE, key)

    return Command(CommandType.INVALID, key)

# MOVIMENTOS
def down(app, motion):
    if app.mpv.isempty:
        return

    return min(app.mpv.count, app.cursor+motion.count)

def up(app, motion):
    if app.mpv.isempty:
        return
    
    return max(0, app.cursor-motion.count)

def current(app, motion):
    if app.mpv.isempty:
        return

    return app.cursor + motion.count -1

def start(app, motion):
    if app.mpv.isempty:
        return
    
    return motion.count-1

def end(app, motion):
    if app.mpv.isempty:
        return
    if motion.count > 1:
        return motion.count-1

    return app.mpv.count-1

def percent(app, motion):
    if app.mpv.isempty:
        return
    pct = min(motion.count,99)/100
    return int(app.mpv.count * pct)

# ACTIONS
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
    app.command.text = ":"
    app.message = ""

def exit_player(app):
    app.exit()

def cut(app, index):
    if app.mpv.isempty:
        return 

    app.mpv.playlist.cut(index)

def yank(app, index):
    if app.mpv.isempty:
        return

    app.mpv.playlist.copy(index)

def paste(app):
    app.mpv.playlist.paste(app.cursor)

# EXECUÇÃO
def do_operator(app, start, end):
    if start > end:
        start, end = end, start

    counter = 0
    index = start
    
    operator = app.pending.operator
    app.mpv.playlist.clear_register()

    match operator:
        case OperatorType.DELETE:
            index = start
            while index <= end:
                cut(app, index)
                end -= 1
                counter += 1

            app.message = f"{counter} linha(s) a menos"

        case OperatorType.YANK:
            while index <= end:
                index = start
                yank(app, index)
                end -= 1
                counter += 1
                start += 1

            app.message = f"{counter} linha(s) copiada(s)"

    app.pending.clear()
    app.input.clear()
    app.input.clear_display()

def nv_motion(app, motion):
    func = MOTIONS.get(motion.action)
    if not func:
        return

    target = func(app, motion)
    if target is None:
        app.input.clear()
        app.input.clear_display()
        return

    if app.pending.operator != OperatorType.NONE:
        motion.count *= app.pending.count
        target = func(app, motion)

        start = app.cursor
        end   = target

        do_operator(app, start, end)
        
        if app.cursor > end:
            app.cursor = min(end, app.mpv.count-1)
        else:
            app.cursor = min(start, app.mpv.count-1)
        return

    app.cursor = max(0, min(target, app.mpv.count-1))
    app.input.clear_display()

def nv_operator(app, operator):
    app.pending.operator = operator.action
    app.pending.count = operator.count
    app.input.clear()

def nv_action(app, command):
    ACTIONS[command.key](app)
    app.input.clear()
    app.input.clear_display()

def nv_dispatch(app, command):
    if command is None:
        return

    match command.command_type:
        case CommandType.ACTION:
            nv_action(app, command.value)

        case CommandType.MOTION:
            nv_motion(app, command.value)
            app.input.clear()

        case CommandType.OPERATOR:
            if app.pending.operator == command.value.action:
                motion = Motion(
                    count = 1,
                    action="_"
                )
                nv_motion(app, motion)
                return 

            nv_operator(app, command.value)

        case CommandType.INCOMPLETE:
            return

        case CommandType.INVALID:
            app.input.clear()
            app.input.clear_display()
            app.pending.clear()

def handle_key(app, key):   
    if key == Key.ENTER:
        play(app)
        return

    if key == Key.ESC:
        app.pending.clear()
        app.input.clear()
        app.input.clear_display()
        return

    if not isinstance(key, str): 
        return

    command = app.input.feed(key, app.pending.operator != OperatorType.NONE)
    if not command:
        return

    nv_dispatch(app, command)

# MAPPING
MOTIONS = {
    "j": down,
    "k": up,
    "gg": start,
    "G": end,
    "%": percent,
    "_": current
}

OPERATORS = {
    "d": OperatorType.DELETE,
    "y": OperatorType.YANK
}

ACTIONS = {
    "l": seek_forward,
    "h": seek_back,
    "0": seek_home,
    ":": enter_command,
    "q": exit_player,
    "p": paste,
}

def isprefix(value):
    if not value:
        return False

    if value.isdigit():
        return True

    return any(key.startswith(value) for key in MOTIONS)


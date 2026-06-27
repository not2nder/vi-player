from dataclasses import dataclass
from core.enums import Mode, Key, PlaybackState

from enum import Enum, auto

class CommandType(Enum):
    MOTION     = auto()
    OPERATOR   = auto()
    ACTION     = auto()
    INVALID    = auto()
    INCOMPLETE = auto()

class OperatorType(Enum):
    DELETE = auto()
    YANK   = auto()
    NONE   = auto()

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
    key: str = ""

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
        return

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

#MOTIONS
def down(app, motion):
    if app.mpv.isempty:
        return

    if app.config.player['wrap_navigation']:
        return (app.cursor + motion.count) % app.mpv.count

    return min(app.cursor + motion.count, app.mpv.count-1)

def up(app, motion):
    if app.mpv.isempty:
        return
    
    if app.config.player['wrap_navigation']:
        return (app.cursor-motion.count) % app.mpv.count

    return min(app.cursor - motion.count, app.mpv.count-1)

def current(app, motion):
    if app.mpv.isempty:
        return

    return app.cursor + motion.count-1

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

#ACTIONS
def play(app):
    app.mpv.current = app.cursor
    app.mpv.play()

def pause(app):
    if app.mpv.isempty:
        return

    app.mpv.pause()

def seek_forward(app):
    app.mpv.jump(10)

def seek_back(app):
    app.mpv.jump(-10)

def seek_home(app):
    app.mpv.seek_start()

def enter_command(app):
    app.mode = Mode.COMMAND
    app.commandline.text = ":"
    app.message = ""

def cut(app, index):
    if app.mpv.isempty:
        return

    app.mpv.playlist.cut(index)

def yank(app, index):
    if app.mpv.isempty:
        return

    app.mpv.playlist.copy(index)

def paste(app):
    count = app.mpv.playlist.paste(app.cursor)
    app.cursor = app.cursor + count 

def volume_up(app):
   app.mpv.volumeup()

def volume_down(app):
    app.mpv.volumedown()

def mute(app):
    app.mpv.mute()

def next_song(app):
    if app.mpv.isempty:
        return

    if app.mpv.state == PlaybackState.WAITING:
        return

    app.mpv.next()
    app.cursor = app.mpv.current

def prev_song(app):
    if app.mpv.isempty:
        return

    if app.mpv.state == PlaybackState.WAITING:
        return
    
    app.mpv.prev()
    app.cursor = app.mpv.current

def exit_player(app):
    app.exit()

def do_operator(app, start, end):
    if start > end:
        start, end = end, start

    counter = 0
    i = start

    op = app.pending.operator
    app.mpv.playlist.clear_register()

    match op:
        case OperatorType.DELETE:
            while i <= end:
                cut(app, i)
                end -= 1
                counter += 1

            app.message = f"{counter} linha(s) a menos"
        
        case OperatorType.YANK:
            while i <= end:
                yank(app, start)
                end -= 1
                counter += 1
                start += 1

            app.message = f"{counter} linha(s) copiadas"

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
                motion = Motion(1,"_")
                nv_motion(app, motion)
                return

            nv_operator(app, command.value)

        case CommandType.INCOMPLETE:
            return

        case CommandType.INVALID:
            app.input.clear()
            app.input.clear_display()
            app.pending.clear()

MOTIONS = {
    "j": down,
    "k": up,

    "gg": start,
    "G": end,
    "%": percent,
    "_": current,
}

OPERATORS = {
    "d": OperatorType.DELETE,
    "y": OperatorType.YANK,
}

ACTIONS = {
    "p": paste,
    "q": exit_player,
    "l": seek_forward,
    "h": seek_back,
    "0": seek_home,
    " ": pause,
    "n": next_song,
    "N": prev_song,
    "m": mute,
    ":": enter_command
}

def handle_key(app, key):
    if key == Key.ENTER:
        play(app)
        return

    if key == Key.ESC:
        app.pending.clear()
        app.input.clear()
        app.input.clear_display()
        return

    if key == Key.UP:
        volume_up(app)
        return

    if key == Key.DOWN:
        volume_down(app)
        return
    
    if not isinstance(key, str):
        return

    command = app.input.feed(key, app.pending.operator != OperatorType.NONE)
    if not command:
        return

    nv_dispatch(app, command)

def isprefix(value):
    if not value:
        return False

    if value.isdigit():
        return True

    return any(key.startswith(value) for key in MOTIONS)

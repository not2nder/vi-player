from enum import Enum, auto

class Mode(Enum):
    NORMAL  = "NORMAL"
    COMMAND = "COMMAND"

class Key(Enum):
    UP = auto()
    DOWN    = auto()
    LEFT    = auto()
    RIGHT   = auto()
    DEL     = auto()
    ENTER   = auto()
    SPACE   = auto()
    ESC     = auto()
    ESC_SEQ = auto()

class PlaybackState(Enum):
    WAITING = "WAITING"
    PLAYING = "PLAYING"
    PAUSE   = "PAUSE"

class OperatorType(Enum):
    DELETE = auto()
    YANK   = auto()
    NONE   = auto()

from enum import Enum, auto

class Mode(Enum):
    NORMAL = "NORMAL"
    COMMAND = "COMANDO"

class Key(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    DEL = auto()
    ENTER = auto()
    SPACE = auto()
    ESC_SEQ = auto()

class PlaybackState(Enum):
    WAITING = "AGUARDANDO"
    PLAYING = "TOCANDO"
    PAUSE = "PAUSA"


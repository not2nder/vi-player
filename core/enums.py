from enum import Enum, auto

class Mode(Enum):
    NORMAL = 'NORMAL'
    COMMAND = 'COMANDO'

class Key(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    ESC_SEQ = auto()
    DEL = auto()

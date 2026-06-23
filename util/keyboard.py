import sys, tty, termios
from core.enums import Key

ANSI_CODES = {
    '\x7f': Key.DEL,
    '\x08': Key.DEL,
    '\r': Key.ENTER,
    '\x1b': Key.ESC,
    '\x1b[A': Key.UP,
    '\x1b[B': Key.DOWN,
    '\x1b[C': Key.RIGHT,
    '\x1b[D': Key.LEFT
}

def getch():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)

    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        if ch == '\x1b':
            import select

            if select.select([sys.stdin], [], [], 0.01)[0]:
                ch += sys.stdin.read(2)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    
    return parse_key(ch)

def parse_key(char: str):
    if char in ANSI_CODES:
        return ANSI_CODES[char]
    else:
        return char

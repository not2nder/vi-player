import sys, tty, termios
from core.enums import Key

ANSI_CODES = {
    '\x7f': Key.DEL,
    '\x08': Key.DEL,
    '\r': Key.ENTER,
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
            ch += sys.stdin.read(2)

    finally:
        ch = parse_key(ch)
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    
    return ch

def parse_key(char: str):
    if char in ANSI_CODES:
        return ANSI_CODES[char]
    else:
        return char

import sys, tty, termios
from core.enums import Key

def getch():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)

    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        if ch == '\x1b':
            ch += sys.stdin.read(2)
            ch = parse_bytes(ch)
        elif ch in ("\x7f", "\x08"):
            ch = Key.DEL
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return ch

def parse_bytes(char: str):
    if char == '\x1b[A':  return Key.UP
    elif char == '\x1b[B': return Key.DOWN
    elif char == '\x1b[C': return Key.RIGHT
    elif char == '\x1b[D': return Key.LEFT

    else: return Key.ESC_SEQ 

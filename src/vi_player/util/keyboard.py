import os, sys, tty, termios, select
from vi_player.core.enums import Key

ANSI_CODES = {
    b'\x7f': Key.DEL,
    b'\x08': Key.DEL,
    b'\r': Key.ENTER,
    b'\x1b': Key.ESC,
    b'\x1b[A': Key.UP,
    b'\x1b[B': Key.DOWN,
    b'\x1b[C': Key.RIGHT,
    b'\x1b[D': Key.LEFT
}

TIMEOUT = 0.03

def enter_raw_mode():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    tty.setraw(fd)
    return fd, old

def restore_terminal(fd, old):
    termios.tcsetattr(fd, termios.TCSADRAIN, old)

def read_key(fd):
    data = os.read(fd, 1)

    if data == b'\x1b':
        while select.select([fd],[],[], TIMEOUT)[0]:
            data += os.read(fd,1)
    return data

def getch(fd):
    ch = read_key(fd)
    return parse_key(ch)

def parse_key(data):
    if data in ANSI_CODES:
        return ANSI_CODES[data]
    
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return None

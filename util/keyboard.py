import os, sys, tty, termios, select
from core.enums import Key

TIMEOUT = 0.03

ANSI_CODES = {
    b"\x7f": Key.DEL,
    b"\x08": Key.DEL,
    b"\r": Key.ENTER,
    b"\n": Key.ENTER,
    b"\x1b": Key.ESC,

    b"\x1b[A": Key.UP,
    b"\x1b[B": Key.DOWN,
    b"\x1b[C": Key.RIGHT,
    b"\x1b[D": Key.LEFT,
}

def enter_raw_mode():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    tty.setraw(fd)
    return fd, old

def restore_terminal(fd, old):
    termios.tcsetattr(fd, termios.TCSADRAIN, old)

def read_key_sequence(fd):
    data = os.read(fd, 1)

    if data == b"\x1b":
        while select.select([fd], [], [], TIMEOUT)[0]:
            data += os.read(fd, 1)

    return data

def parse_key(data):
    if data in ANSI_CODES:
        return ANSI_CODES[data]

    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return None

def getch(fd):
    data = read_key_sequence(fd)
    return parse_key(data)


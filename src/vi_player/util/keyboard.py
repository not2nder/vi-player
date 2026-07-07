import os
import sys
import tty
import termios
import select
from dataclasses import dataclass

from vi_player.core.enums import Key

@dataclass(slots=True)
class MouseEvent:
    button: int
    x: int
    y: int
    pressed: bool
    released: bool

def parse_mouse(data):
    if not data.startswith(b'\x1b[<'):
        return None

    final = data[-1:]

    if final not in (b'M', b'm'):
        return None

    body = data[3:-1]

    try:
        button, x, y = map(int, body.split(b';'))
    except ValueError:
        return None

    return MouseEvent(
        button=button,
        x = x - 1,
        y = y - 1,
        pressed=final == b'M',
        released=final == b'm',
    )

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
        return read_esc_seq(fd, data)

    return read_utf8(fd, data)

def read_esc_seq(fd, data):
    while select.select([fd],[],[],TIMEOUT)[0]:
        data += os.read(fd,1)
    return data

def utf8_expected_len(first_byte):
    b = first_byte[0]

    if b >> 7 == 0:
        return 1

    if b >> 5 == 0b110:
        return 2

    if b >> 4 == 0b1110:
        return 3

    if b >> 3 == 0b11110:
        return 4

    return 1

def read_utf8(fd, first):
    expected = utf8_expected_len(first)

    data = first

    while len(data) < expected:
        data += os.read(fd, expected - len(data))

    return data

def getch(fd):
    ch = read_key(fd)
    return parse_key(ch)

def parse_key(data):
    mouse = parse_mouse(data)

    if mouse is not None:
        return mouse

    if data in ANSI_CODES:
        return ANSI_CODES[data]
    
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return None

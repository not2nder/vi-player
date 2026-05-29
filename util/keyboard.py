import sys, tty, termios

def getch():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)

    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        if ch == '\x1b':
            ch += sys.stdin.read(2)
            ch = parse_bytes(ch)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return ch

def parse_bytes(char: str):
    SEQUENCES = {
        '\x1b[A': 'UP',
        '\x1b[B': 'DOWN',
        '\x1b[C': 'RIGHT',
        '\x1b[D': 'LEFT'
    }

    return SEQUENCES.get(char, "ESC_SEQ")

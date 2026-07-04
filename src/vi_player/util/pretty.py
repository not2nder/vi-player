import sys
import re
import os
from wcwidth import wcswidth

RESET = "\x1b[0m"

ANSI_ESCAPE = re.compile(r'\x1b\[[0-9;?]*[ -/]*[@-~]')

FG_COLORS = {
    "black": 30,
    "red": 31,
    "green": 32,
    "yellow": 33,
    "blue": 34,
    "magenta": 35,
    "cyan": 36,
    "white": 37,
    "gray": 90,
    "grey": 90,
}

BG_COLORS = {
    "black": 40,
    "red": 41,
    "green": 42,
    "yellow": 43,
    "blue": 44,
    "magenta": 45,
    "cyan": 46,
    "white": 47,
    "gray": 100,
    "grey": 100,
}

BOLD_ON = "\x1b[1m"
BOLD_OFF = "\x1b[22m"

ITALIC_ON = "\x1b[3m"
ITALIC_OFF = "\x1b[23m"

UNDERLINE_ON = "\x1b[4m"
UNDERLINE_OFF = "\x1b[24m"

REVERSE_ON = "\x1b[7m"
REVERSE_OFF = "\x1b[27m"

def length(text):
    return wcswidth(ANSI_ESCAPE.sub('', text))

def fill(text: str, width: int) -> str:
    visible = length(text)

    pad = " "*max(0, width-visible)

    return text + pad

def paint(text: str, style):
    bold      = BOLD_ON if style.get("bold") else ""
    italic    = ITALIC_ON if style.get("italic") else ""
    underline = UNDERLINE_ON if style.get("underline") else ""
    reverse   = REVERSE_ON if style.get("reverse") else ""

    background = bg(style.get("bg"))
    foreground = fg(style.get("fg"))

    g_reset = RESET if not(background and foreground) else ""

    return (
        reverse
        +bold
        +italic
        +underline
        +foreground
        +background
        +text
        +REVERSE_OFF
        +BOLD_OFF
        +ITALIC_OFF
        +UNDERLINE_OFF
        +g_reset
    )

def padding(text: str, value: int = 1) -> str:
    return f"{' '*value}{text}{' '*value}"

def bg(color: str):
    if not color:
        return ""

    if color in BG_COLORS: 
        return f"\x1b[{BG_COLORS[color]}m"

    return hxtoansi(color)

def fg(color: str):
    if not color:
        return ""

    if color in FG_COLORS:
        return f"\x1b[{FG_COLORS[color]}m"

    return hxtoansi(color, False)

def bold(text: str):
    return f"\x1b[1m{text}\x1b[22m"

def underline(text: str):
    return f"\x1b[4m{text}\x1b[24m"

def justify(*args, width: int) -> str:
    if not args:
        return ""

    texts = [str(a) for a in args]

    text_length = sum(length(t) for t in texts)

    gaps = len(args) - 1

    if gaps <= 0:
        return texts[0]

    spaces = max(1, width-text_length)

    base = spaces//gaps
    extra = spaces % gaps

    result = ""

    for i, text in enumerate(texts[:-1]):
        result += text
        result += ' '*(base + (1 if i< extra else 0))

    result += texts[-1]

    return result

def truncate(text: str, max_width: int):
    if length(text) <= max_width:
        return text

    return text[:max_width-3]+"..."

def center(text: str, width: int) -> str:
    visible = length(text)

    if visible >= width:
        return text

    total = width - visible
    
    left = total//2
    right = total - left
    
    return f"{' '*left}{text}{' '*right}"

def reverse(text: str) -> str:
    return f"\x1b[7m{text}\x1b[0m"

def hxtoansi(color: str, bg: bool = True) -> str:
    if not color:
        return ""

    hex_color = color.lstrip("#")
    r, g, b = [int(hex_color[i:i+2], 16) for i in (0,2,4)]
    return f"\x1b[{48 if bg else 38};2;{r};{g};{b}m"


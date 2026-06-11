import sys
import re
import os
from wcwidth import wcswidth

RESET = "\x1b[0m"

ANSI_ESCAPE = re.compile(r'\x1b\[[0-9;?]*[ -/]*[@-~]')

def length(text):
    return wcswidth(ANSI_ESCAPE.sub('', text))

def fill(text: str, width: int) -> str:
    visible = length(text)

    pad = " "*max(0, width-visible)

    return text + pad

def paint(text: str, fg_color: str, bg_color: str):
    return bg(bg_color) + fg(fg_color) + text

def padding(text: str, value: int = 1) -> str:
    return f"{' '*value}{text}{' '*value}"

def bg(color: str):
    return hxtoansi(color)

def fg(color: str):
    return hxtoansi(color, False)

def bold(text: str):
    return f"\x1b[1m{text}\x1b[22m"

def underline(text: str):
    return f"\x1b[4m{text}\x1b[24m"

def dim(text: str):
    return f"\x1b[2m{text}\x1b[22m"

def red(text: str) -> str:
    return f"\x1b[31m{text}\x1b[39m"

def yellow(text: str) -> str:
    return f"\x1b[33m{text}\x1b[39m"

def blue(text: str) -> str:
    return f"\x1b[34m{text}\x1b[39m"

def error(text: str) -> str:
    return f"\x1b[031m{text}"

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


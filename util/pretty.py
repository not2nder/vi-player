import re
import os

cols, lines = os.get_terminal_size()

ANSI_ESCAPE = re.compile(r'\x1b\[[0-9;?]*[ -/]*[@-~]')

def length(text):
    return len(ANSI_ESCAPE.sub('', text))

def fill(text: str, width: int = cols) -> str:
    visible = length(text)

    pad = " "*max(0, width-visible)

    return text + pad

def justify(*args, width: int = cols, padding: int = 0) -> str:
    content_width = sum(length(a) for a in args) + (padding*2)

    if content_width >= width:
        return " ".join(args)

    gap = width - content_width
    
    return f"{' '*padding}{args[0]}{' '*gap}{args[1]}{' '*padding}"

def center(text: str, width: int = cols) -> str:
    visible = length(text)
    if visible >= width:
        return text

    total = width - visible
    left = total//2
    right = total - left
    return f"{' '*left}{text}{' '*right}"

def reverse(text: str) -> str:
    return f"\x1b[7m{text}\x1b[0m"

def colorize(text: str, color: str, background: bool = True) -> str:
    hex_color = color.lstrip("#")
    r, g, b = [int(hex_color[i:i+2], 16) for i in (0,2,4)]
    
    layer=  48 if background else 38
    return f"\x1b[{layer};2;{r};{g};{b}m{text}\x1b[{layer+1}m"

def printf(text: str, pos: str, offset: int = 0):
    line = 1

    if pos == "start":
        line = 1

    elif pos == "mid":
        line = (lines//2)

    elif pos == "end":
        line = lines
    
    print(
        f"\x1b[{line+offset};1H"
        f"\x1b[2K"
        f"{text}",
        end="",
        flush=True
    )


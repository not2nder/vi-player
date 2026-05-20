import re
import os

cols, lines = os.get_terminal_size()

def length(text):
    ANSI_ESCAPE = re.compile(r'\x1b\[[0-9;?]*[ -/]*[@-~]')
    return len(ANSI_ESCAPE.sub('', text))

def fill(text: str, width: int = cols) -> str:
    visible = length(text)

    pad = " "*max(0, width-visible)

    return text + pad

def padding(text: str, value: int = 1) -> str:
    return f"{' '*value}{text}{' '*value}"

def bg(text: str, color: str):
    return f"{hxtoansi(color)}{text}\x1b[48m"

def fg(text: str, color: str):
    return f"{hxtoansi(color, False)}{text}\x1b[38m"

def bold(text: str):
    return f"\x1b[1m{text}\x1b[22m"

def dim(text: str):
    return f"\x1b[2m{text}\x1b[0m"

def justify(*args, width: int = cols) -> str:
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

def hxtoansi(color: str, bg: bool = True) -> str:
    hex_color = color.lstrip("#")
    r, g, b = [int(hex_color[i:i+2], 16) for i in (0,2,4)]
    return f"\x1b[{48 if bg else 38};2;{r};{g};{b}m"

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


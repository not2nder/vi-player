from util.pretty import paint, fill, underline, bold, RESET
from core.theme import get_theme
from core.enums import Mode
from util import lexer

def draw(screen, command, motion, mode):
    theme = get_theme()

    if mode == Mode.COMMAND:
        text = command

    elif mode == Mode.NORMAL:
        text = motion.rjust(screen.width-2)

    text = highlight(text)
    line = paint(fill(text, width=screen.width), theme.fg, theme.bg) + RESET
    
    screen.draw(screen.height, line)

def highlight(text: str) -> str:
    TOKEN_STYLES = {
        "PATH": lambda x: underline(x),
        "DIGIT": lambda x: bold(x)
    }

    res = ""

    for token in lexer.tokenize(text):
        if token.token_type in TOKEN_STYLES:
            res += TOKEN_STYLES[token.token_type](token.text)
        else:
            res += token.text
    return res


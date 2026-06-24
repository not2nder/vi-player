from util.pretty import *
from core.theme import get_theme
from core.enums import Mode
from util import lexer

def draw(screen, command, motion, message, mode):
    theme = get_theme()

    if mode == Mode.COMMAND:
        text = draw_cursor(command, theme)
    
    elif mode == Mode.NORMAL:
        text = justify(message, motion, width=screen.width-1)
    else:
        text = ""

    line = paint(
        fill(text, width=screen.width),
        theme.style("Normal")
    ) + RESET
    
    screen.draw(screen.height, line)

def draw_cursor(command, theme):
    text = command.text
    cursor = command.cursor

    if cursor >= len(text):
        return text + paint(' ', theme.style("CursorBlock")) + paint(' ', theme.style("Normal"))

    before = text[:cursor]
    current = text[cursor]
    after = text[cursor+1:]

    return (
        before
        + paint(current, theme.style("CursorBlock"))
        + paint(after, theme.style("Normal"))
    )

#def highlight(text: str) -> str:
#    TOKEN_STYLES = {
#        "PATH": lambda x: underline(x),
#        "DIGIT": lambda x: bold(x)
#    }
#
#    res = ""
#
#    for token in lexer.tokenize(text):
#        if token.token_type in TOKEN_STYLES:
#            res += TOKEN_STYLES[token.token_type](token.text)
#        else:
#            res += token.text
#   return res


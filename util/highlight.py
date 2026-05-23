from util import lexer

RESET = "\x1b[0m"

TOKEN_STYLES = {
    "PATH": {
        "underline": True
    },
    "COMMAND": {
        "bold"
        }
}

def highlight(text: str):
    result = ""
    for token in lexer.tokenizer(text):
        result += f"{TOKEN_COLORS[token.tipo]}{token.texto}{RESET}"

    return result


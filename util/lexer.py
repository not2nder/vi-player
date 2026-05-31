from dataclasses import dataclass
import shlex

@dataclass
class Token:
    text: str
    token_type: str
    start: int
    end: int

def tokenize(text: str):
    cursor = 0
    tokens = []

    while cursor < len(text):
        char = text[cursor]

        if char.isspace():
            inicio = cursor
            while cursor < len(text) and text[cursor].isspace():
                cursor += 1
            fim = cursor

            tokens.append(Token(text[inicio:fim], "SPACE", inicio, fim))
        
        elif char == ":":
            inicio = cursor
            while cursor < len(text) and not text[cursor].isspace():
                cursor +=1
            fim = cursor
            tokens.append(Token(text[inicio:fim], "COMMAND", inicio, fim))

        elif char.isdigit():
            inicio = cursor
            while cursor < len(text) and not text[cursor].isspace():
                cursor +=1
            fim = cursor
            tokens.append(Token(text[inicio:fim], "DIGIT", inicio, fim))
        
        elif (
            text.startswith("~/", cursor) or
            text.startswith("./", cursor) or
            text.startswith("../", cursor) or
            text.startswith("/", cursor) or 
            text.startswith("~", cursor)
        ):
            inicio = cursor
            while cursor < len(text) and not text[cursor].isspace():
                cursor += 1
            fim = cursor
            tokens.append(Token(text[inicio:fim], "PATH", inicio, fim))

        else:
            inicio = cursor
            while cursor < len(text) and not text[cursor].isspace():
                cursor += 1
            fim = cursor
            tokens.append(Token(text[inicio:fim], "TEXT", inicio, fim))

    return tokens


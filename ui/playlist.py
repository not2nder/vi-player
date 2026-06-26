from util.pretty import *
from core.theme import get_theme

from dataclasses import dataclass
from enum import Enum, auto

class TokenType(Enum):
    FIELD = auto()
    ALIGN = auto()
    TEXT  = auto()

@dataclass(slots=True)
class Token:
    type: TokenType
    value: str = ""

@dataclass(slots=True)
class Segment:
    text: str
    field: str
    style: str = "Normal" 

@dataclass(slots=True)
class Layout:
    left: list[Segment]
    right: list[Segment]
    gap: int

FMT = "%t %a %= %b%d"

def parse_format(fmt):
    i = 0
    tokens = []

    while i < len(fmt):
        if fmt[i] != "%":
            tokens.append(Token(TokenType.TEXT, fmt[i]))
            i += 1
            continue

        i += 1

        if i >= len(fmt):
            break

        code = fmt[i]

        if code == "=":
            tokens.append(Token(TokenType.ALIGN))
        elif code in "tabdf":
            tokens.append(Token(TokenType.FIELD, code))
        elif code == "%":
            tokens.append(Token(TokenType.TEXT, "%"))
        else:
            raise ValueError(f"Campo inválido: {code}")

        i+=1

    return tokens

def resolve(tokens, song, selected = False):
    fields = {
        "t": song.title,
        "a": song.artist,
        "b": song.album,
        "f": song.filename,
        "d": padding(song.time)
    }

    if selected:
        styles = {
            "t": "CursorLine",
            "a": "CursorLineMuted",
            "b": "CursorLineMuted",
            "f": "CursorLine",
            "d": "CursorLine",
            "text": "CursorLine"
        }
    else:
        styles = {
            "t": "Normal",
            "a": "Muted",
            "b": "Muted",
            "d": "Normal",
            "f": "Normal",
            "text": "Normal"
        }

    result = []

    for token in tokens:
        if token.type == TokenType.FIELD:
            result.append(
                Segment(
                    text  = fields[token.value],
                    field = token.value,
                    style = styles[token.value]
                )
            )
        elif token.type == TokenType.TEXT:
            result.append(
                Segment(
                    text  = token.value,
                    field = "text",
                    style = styles["text"]
                )
            )
        elif token.type == TokenType.ALIGN:
            result.append(
                Segment(
                    text  = "",
                    field = "align",
                    style = styles["text"]
                )
            )

    return result

def build_layout(segments, width):
    left = []
    right = []

    align = False

    for segment in segments:
        if segment.field == "align":
            align = True
            continue

        if align:
            right.append(segment)
        else:
            left.append(segment)

    lwidth = sum(length(seg.text) for seg in left)
    rwidth = sum(length(seg.text) for seg in right)

    gap = width - lwidth - rwidth
    if gap < 1:
        gap = 1
    
    return Layout(
        left,
        right,
        gap
    )

def render(layout, theme):
    output= ""

    for segment in layout.left:
        output += paint(
            segment.text,
            theme.style(segment.style)
        )

    output += " " * layout.gap
    
    for segment in layout.right:
        output += paint(
            segment.text,
            theme.style(segment.style)
        )

    return output 

def draw(screen, app):
    theme = get_theme()

    FMT = app.config.player["playlist"]
    FORMAT_TOKENS = parse_format(FMT)

    visible_lines = screen.height - 3

    scroll = max(0, app.cursor-visible_lines+2)
    max_scroll = max(0, app.mpv.count-visible_lines)
    scroll = min(scroll, max_scroll)
    
    visible_songs = app.mpv.playlist[scroll:scroll+visible_lines]
    
    for i, song in enumerate(visible_songs):
        index = i + scroll
        selected = index == app.cursor

        if app.config.player["number"]:
            number = build_index(
                index,
                app.cursor,
                get_digits(app.mpv.count),
                app.config.player["relativenumber"]
            )

            number = paint(
                number,
                style = theme.style("CursorLineNr" if selected else "LineNr")
            )
        else:
            number = ""

        segments = resolve(
            FORMAT_TOKENS,
            song,
            selected
        )

        layout = build_layout(
            segments,
            screen.width - length(number)
        )

        content = render(layout, theme)

        line = number + content + RESET

        screen.draw(i+1, line)

    for i in range(len(visible_songs), visible_lines):
        line = build_empty_line(screen.width, theme)
        screen.draw(i+1, line)

def build_index(index, cursor, digits, rnu):
    if rnu and index != cursor:
        return padding(str(abs(index-cursor)).rjust(digits))
    
    elif not rnu:
        return padding(str(index+1).rjust(digits))

    else:
        return padding(str(index+1).ljust(digits))

def build_title(song, freespace):
    return truncate(song.title, freespace)

def build_time(song):
    return padding(song.time)

def get_digits(count):
    return max(2, len(str(count)))

def build_empty_line(width, theme):
    char = theme.fillchars.get("eob","~")
    fillchar = fill(char, width)

    return paint(fillchar, theme.style("Muted"))


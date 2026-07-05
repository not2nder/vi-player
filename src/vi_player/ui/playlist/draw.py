from vi_player.util.pretty import (
    justify,
    padding,
    truncate,
    length,
    fill,
    paint,
    RESET,
)
from vi_player.core.theme import get_theme

def render(screen, app):
    theme = get_theme()
    
    width = screen.width
    visible_lines = screen.height - 3

    count  = app.mpv.count
    cursor = app.cursor
    
    show_number    = app.config.get("number")
    relativenumber = app.config.get("relativenumber")
    digits         = get_digits(count)

    styles = {
        "normal": theme.style("Normal"),
        "linenr": theme.style("LineNr"),
        "cursor_line": theme.style("CursorLine"),
        "cursor_linenr": theme.style("CursorLineNr"),
        "muted": theme.style("Muted"),
    }

    eob_char  = theme.fillchars.get("eob", "~") 
    
    scroll = get_scroll(cursor, count, visible_lines)
    visible_songs = app.mpv.playlist[scroll:scroll + visible_lines]
    
    for i, song in enumerate(visible_songs):
        index = i + scroll

        selected = index == cursor

        if show_number:
            number = build_index(index, cursor, digits, relativenumber)
        else:
            number = ""

        duration = build_time(song)
        textspace = max(0, width - length(number) - length(duration) - 1)

        title = build_title(song, textspace)
        
        line = build_line(
            number,
            title,
            duration,
            width,
            styles["cursor_linenr"] if selected else styles["linenr"],
            styles["cursor_line"] if selected else styles["normal"]
        )

        screen.draw(i + 1, line)

    empty_line = build_empty_line(width, eob_char, styles["muted"])

    for i in range(len(visible_songs), visible_lines):
        screen.draw(i + 1, empty_line)

def build_index(index, cursor, digits, rnu):
    if rnu and index != cursor:
        return padding(str(abs(index - cursor)).rjust(digits))
    
    elif not rnu:
        return padding(str(index + 1).rjust(digits))

    else:
        return padding(str(index + 1).ljust(digits))

def build_title(song, freespace):
    return truncate(song.title, freespace)

def build_time(song):
    return padding(song.time)

def get_digits(count):
    return max(2, len(str(count)))

def get_scroll(cursor, count, visible):
    scroll = max(0, cursor - visible + 8)
    max_scroll = max(0, count - visible)

    return min(scroll, max_scroll)

def build_line(index, title, duration, width, index_style, line_style):
    freespace = max(0, width - length(index))
    
    text = justify(title, duration, width=freespace)
    
    index = paint(index, index_style)
    text = paint(text, line_style)

    return index + text + RESET

def build_empty_line(width, char, style):
    text = fill(char, width)
    return paint(text, style)


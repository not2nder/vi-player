from util.pretty import *

from core.theme import get_theme

def draw(screen, app):
    theme = get_theme()

    visible_lines = screen.height - 3

    scroll = max(0, app.cursor-visible_lines+2)
    max_scroll = max(0, app.mpv.count-visible_lines)
    scroll = min(scroll, max_scroll)
    
    visible_songs = app.mpv.playlist[scroll:scroll+visible_lines]
    
    for i, song in enumerate(visible_songs):
        index = i+scroll

        number = build_index(
            index,
            app.cursor,
            get_digits(app.mpv.count),
            app.config.player["relativenumber"]
        )

        duration = build_time(song)
        textspace = screen.width-length(number)-length(duration)

        title = build_title(song, textspace)

        line = build_line(
            number,
            title,
            duration,
            screen.width,
            index == app.cursor,
            theme
        )

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
    return truncate(song.name, freespace)

def build_time(song):
    return padding(song.time)

def get_digits(count):
    return max(2, len(str(count)))

def build_line(index, title, duration, width, selected, theme):
    
    freespace = width-length(index)

    text = justify(
        title,
        duration,
        width=freespace
    )

    if selected:
        index = paint(index,theme.inum_fg, theme.inum_bg)
        text = paint(text, theme.iline_fg, theme.iline_bg)

    else:
        index = paint(index,theme.index_fg, theme.index_bg)
        text = paint(text, theme.fg, theme.bg)

    return index+text + RESET

def build_empty_line(width, theme):
    return paint(fill(bold("~ "), width), theme.index_fg, theme.bg)


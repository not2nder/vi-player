from vi_player.util.pretty import *
from vi_player.core.theme import get_theme

def draw(screen, app):
    statusline = app.config.statusline
    separator = statusline.get("separator", "-")

    WIDGETS = {
        "mode": build_mode,
        "song": build_song,
        "album": build_album,
        "artist": build_artist,
        "state": build_state,
        "theme": build_theme,
        "position": build_position,
        "percent": build_percent,
    }
    
    left = [
        WIDGETS[item](app)
        for item in statusline.get("left", [])
        if item in WIDGETS
    ]
 
    right = [
        WIDGETS[item](app)
        for item in statusline.get("right", [])
        if item in WIDGETS
    ]

    line = build_statusline(left, right, separator, screen.width)

    screen.draw(screen.height-1, line)

def build_statusline(left: list, right: list, separator: str, width: int):
    theme = get_theme()

    result = ""
    left = [padding(t) for t in left if t]
    right = [padding(t) for t in right if t]

    left_text = separator.join(left)
    right_text = separator.join(right)

    gap = width-length(left_text)-length(right_text)
    gap = max(0, gap)
    space = ' '*gap

    result = f"{left_text}{space}{right_text}"
    result = paint(
        result,
        theme.style("StatusLine")
    )

    return result

def build_mode(app):
    return app.mode.value

def build_song(app):
    return app.mpv.get_current_song().title if app.mpv.playing_song else "Sem Música"

def build_state(app):
    return app.mpv.state.value

def build_theme(app):
    return get_theme().meta["name"]

def build_position(app):
    if app.mpv.isempty:
        return "Empty"

    return f"{app.cursor+1}/{app.mpv.count}"

def build_percent(app):
    if app.mpv.count <=1:
        percent = 0
    else:
        percent = (app.cursor / (app.mpv.count - 1)) * 100

    if percent > 99:
        text = "Start"
    elif percent < 1:
        text = "End"
    else:
        text = f"{percent:.0f}%"

    return text.rjust(6)

def build_album(app):
    album = app.mpv.get_current_song().album if app.mpv.playing_song else ""
    return album

def build_artist(app):
    artist = app.mpv.get_current_song().artist if app.mpv.playing_song else ""
    return artist

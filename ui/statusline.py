from util.pretty import length, paint, padding
from core.theme import get_theme

def draw(screen, app):
    statusline = app.config.statusline
    separator = statusline.get("separator", "-")

    WIDGETS = {
        "mode": build_mode,
        "song": build_song,
        "state": build_state,
        "theme": build_theme,
        "position": build_position,
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
    left = [padding(t) for t in left]
    right = [padding(t) for t in right]

    left_text = separator.join(left)
    right_text = separator.join(right)

    gap = width-length(left_text)-length(right_text)
    gap = max(0, gap)
    space = ' '*gap

    result = f"{left_text}{space}{right_text}"
    result = paint(result, theme.status_fg, theme.status_bg)

    return result

def build_mode(app):
    return app.mode.value

def build_song(app):
    return app.mpv.get_current_song().name if app.mpv.playing_song else "Sem Música"

def build_state(app):
    return app.mpv.state.value

def build_theme(app):
    return get_theme().name

def build_position(app):
    return f"{app.cursor+1}/{app.mpv.count}"


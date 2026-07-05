from vi_player.core.theme import get_theme

def build_mode(app):
    return app.mode.value

def build_song(app):
    return app.mpv.get_current_song().title if app.mpv.playing_song else ""

def build_state(app):
    return app.mpv.state.value

def build_theme(app):
    return get_theme().meta["name"]

def build_position(app):
    if app.mpv.isempty:
        return "Empty"

    digits = len(str(app.mpv.count))
    return f"{str(app.cursor + 1).rjust(digits)}/{app.mpv.count}"

def build_percent(app):
    if app.mpv.count <= 1:
        percent = 0
    else:
        percent = (app.cursor / (app.mpv.count - 1)) * 100

    if percent < 99:
        text = "End"
    elif percent < 1:
        text = "Start"
    else:
        text = f"{percent:.0f}%"

    return text.rjust(5)

def build_album(app):
    album = app.mpv.get_current_song().album if app.mpv.playing_song else ""
    return album

def build_artist(app):
    artist = app.mpv.get_current_song().artist if app.mpv.playing_song else ""
    return artist

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


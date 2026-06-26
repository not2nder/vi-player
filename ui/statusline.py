from lupa import LuaRuntime

from util.pretty import *
from core.theme import get_theme

lua = LuaRuntime()

with open("lua/lualine.lua", "r", encoding="utf-8") as file:
    LUALINE = lua.execute(file.read())

LEFT_SECTIONS = [
    "lualine_a",
    "lualine_b",
    "lualine_c"
]

RIGHT_SECTIONS = [
    "lualine_x",
    "lualine_y",
    "lualine_z"
]

def render_sections(names, app):
    result = []

    for name in names:
        section = LUALINE["sections"][name]
        result.extend(
            get_section_components(section, app)
        )

    return result

def get_section_components(section, app):
    components = []

    for _, table in section.items():
        components.append(render_component(table, app))

    return components

def render_component(component, app):
    name = component["name"]

    value = WIDGETS[name](app)
    fmt = component["fmt"]

    if fmt:
        value = fmt(value)

    return value

def draw(screen, app):
    statusline = app.config.statusline
    separator = "|"
   
    left = render_sections(LEFT_SECTIONS, app)
    right = render_sections(RIGHT_SECTIONS, app)

    line = build_statusline(left, right, separator, screen.width)

    screen.draw(screen.height-1, line)

def build_statusline(left: list, right: list, separator: str, width: int):
    theme = get_theme()

    result = ""
    left = [padding(bold(t)) for t in left if t]
    right = [padding(bold(t)) for t in right if t]

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
    return f"{app.cursor+1}/{app.mpv.count}"

def build_percent(app):
    percent = (app.cursor/(app.mpv.count-1))*100

    if percent > 99:
        text = "Fim"
    elif percent < 1:
        text = "Início"
    else:
        text = f"{percent:.0f}%"

    return text.rjust(6)

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
 

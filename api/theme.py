from pathlib import Path
from core.theme import set_theme, get_theme
from core.lua_utils import to_lua

class ThemeAPI:
    def __init__(self, app):
        self.app = app

    def current(self):
        return get_theme().meta["name"]

    def list(self):
        path = Path("~/.config/vi-player/themes").expanduser()
        themes = sorted(file.stem for file in path.glob("*.toml"))

        return self.app.luahost.to_lua(themes)

    def set(self, name):
        set_theme(name)
        self.app.dirty = True

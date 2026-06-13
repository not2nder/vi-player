from pathlib import Path
import tomllib

CURRENT_THEME = None

class Theme:
    def __init__(self, data): 
        self.meta = data.get("meta", {})
        self.palette = data.get("palette", {})
        self.fillchars = data.get("fillchars", {})

        self.highlights = {}

        for name, style in data.get("highlight", {}).items():
            self.highlights[name] = {
                "fg": self.resolve(style.get("fg")),
                "bg": self.resolve(style.get("bg"))
        }

    @classmethod
    def builtin(cls):
        return cls({
            "meta": {
                "name": "builtin",
                "author": "native"
            },
            "palette": {},
            "highlight": {
                "Normal": {
                    "fg": None,
                    "bg": None
                },
                "CursorLine": {
                   "fg": "blue",
                    "bg": None
                },
                "LineNr": {
                    "fg": "yellow",
                    "bg": None
                },
                "CursorLineNr": {
                    "fg": "blue",
                    "bg": None
                },
                "StatusLine": {
                    "fg": None,
                    "bg": None
                },
                "Muted": {
                    "fg": None,
                    "bg": None
                }
            },
            "fillchars": {
                "eob": "~"    
            }
        })

    def resolve(self, value):
        if value is None:
            return None

        if value in self.palette:
            return self.palette[value]

        return value

    def style(self, name):
        if name in self.highlights:
            return self.highlights[name]

        return self.highlights["Normal"]

def load_theme(name):
    theme_file = Path.home()/".config"/"vi-player"/"themes"/f"{name}.toml"

    with open(theme_file, "rb") as f:
        theme = tomllib.load(f)

    return Theme(theme)

def set_theme(name):
    global CURRENT_THEME
    
    if name is None or not name:
        CURRENT_THEME = Theme.builtin()
        return

    CURRENT_THEME = load_theme(name)

def get_theme():
    return CURRENT_THEME

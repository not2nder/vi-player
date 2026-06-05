from pathlib import Path
import tomllib

CURRENT_THEME = None

class Theme:
    def __init__(self, colors):
        self.bg = colors["bg"]
        self.fg = colors["fg"]

        self.secondary_bg = colors.get("secondary_bg", self.bg)
        self.secondary_fg = colors.get("secondary_fg", self.fg)
         
        self.status_bg = colors.get("statusline_bg", self.secondary_bg)
        self.status_fg = colors.get("statusline_fg", self.secondary_fg)
        
        self.mode_bg = colors.get("mode_bg", self.secondary_bg)
        self.mode_fg = colors.get("mode_fg", self.secondary_fg)

        self.iline_bg = colors.get("indicator_line_bg", self.secondary_bg)
        self.iline_fg = colors.get("indicator_line_fg", self.secondary_fg)

        self.index_bg = colors.get("index_bg", self.bg)
        self.index_fg = colors.get("index_fg", self.fg)

        self.time_fg = colors.get("time_fg", self.bg)

        self.inum_bg = colors.get("indicaor_num_bg", self.bg)
        self.inum_fg = colors.get("indicator_num_fg", self.fg)

def load_theme(name):
    theme_file = Path.home()/".config"/"vi-player"/"themes"/f"{name}.toml"
    
    with open(theme_file, "rb") as f:
        theme = tomllib.load(f)

    return Theme(theme["colors"])

def set_theme(name):
    global CURRENT_THEME
    CURRENT_THEME = load_theme(name)

def get_theme():
    return CURRENT_THEME

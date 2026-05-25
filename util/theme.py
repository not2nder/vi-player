from pathlib import Path
import tomllib

class Theme:
    def __init__(self, colors):
        self.bg = colors["bg"]
        self.fg = colors["fg"]

        self.secondary_bg = colors.get("secondary_bg", self.bg)
        self.secondary_fg = colors.get("secondary_fg", self.fg)
        
        self.statusline_bg = colors.get("statusline_bg", self.secondary_bg)
        self.statusline_fg = colors.get("statusline_fg", self.secondary_fg)

        self.hg_bg = colors.get("highlight_bg", self.secondary_bg)
        self.hg_fg = colors.get("highlight_fg", self.secondary_fg)

        self.index_bg = colors.get("index_bg", self.bg)
        self.index_fg = colors.get("index_fg", self.secondary_fg)

def load_theme(name):
    theme_file = Path.home()/".config"/"vi-player"/"themes"/f"{name}.toml"
    
    with open(theme_file, "rb") as f:
        theme = tomllib.load(f)

    return Theme(theme["colors"])

def get_current_theme():
    config_path = Path.home()/".config"/"vi-player"
    
    with open(config_path/"config.toml", "rb") as f:
        config = tomllib.load(f)

    current_theme = config["general"]["theme"]

    return load_theme(current_theme)

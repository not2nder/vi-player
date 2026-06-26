from pathlib import Path
import json

CURRENT_CONFIG = None
CONFIG_FILE = Path.home()/".config"/"vi-player"/"config.json"

class Config:
    def __init__(self, data):
        self.general = data.get("general", {})
        self.general["theme"] = self.general.get("theme", None)
        
        self.player = data.get("player", {})
        self.player["relativenumber"] = self.player.get("relativenumber", True)
        self.player["number"] = self.player.get("number", True)
        self.player["wrap_navigation"] = self.player.get("wrap_navigation", False)
        self.player["playlist"] = self.player.get("playlist_format", "%t %= %b %d")

        self.statusline = data.get("statusline", {})

    def set_theme(self, name):
        self.general["theme"] = name

    def set_number(self, value = None):
        if value is None:
            self.player["number"] = not self.player["number"]
        else:
            self.player["number"] = value
    
    def set_relativenumber(self, value = None):
        if value is None:
            self.player["relativenumber"] = not self.player["relativenumber"]
        else:
            self.player["relativenumber"] = value

    def set_wrap(self, value = None):
        if value is None:
            self.player["wrap_navigation"] = not self.player["wrap_navigation"]
        else:
            self.player["wrap_navigation"] = value

    def set_playlist_fmt(self, value = None):
        if value is None:
            return

        self.player["playlist"] = value

    def to_dict(self):
        return {
            "general": self.general,
            "player": self.player,
            "statusline": self.statusline
        }

def load_config():
    global CURRENT_CONFIG

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        config = json.load(f)

    CURRENT_CONFIG = Config(config)

def get_config():
    return CURRENT_CONFIG

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

        self.statusline = data.get("statusline", {})

    def set_theme(self, name):
        self.general["theme"] = name

    def set(self, name, value):
        self.player[name] = value

    def get(self, value):
        return self.player[value]

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

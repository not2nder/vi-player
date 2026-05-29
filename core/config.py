from pathlib import Path
import json

CURRENT_CONFIG = None
CONFIG_FILE = Path.home()/".config"/"vi-player"/"config.json"

class Config:
    def __init__(self, data):
        self.general = data.get("general", {})
        self.general["theme"] = self.general.get("theme", "default")
        
        self.player = data.get("player", {})
        self.player["relativenumber"] = self.player.get("relativenumber", True)
        self.player["usearrows"] = self.player.get("usearrows", False)

    def set_theme(self, name):
        self.general["theme"] = name

    def set_arrows(self):
        self.player["usearrows"] = not self.player["usearrows"]

    def set_relativenumber(self, value = None):
        if value is None:
            self.player["relativenumber"] = not self.player["relativenumber"]
        else:
            self.player["relativenumber"] = value

    def to_dict(self):
        return {
            "general": self.general,
            "player": self.player
        }

def load_config():
    global CURRENT_CONFIG

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        config = json.load(f)

    CURRENT_CONFIG = Config(config)

def get_config():
    return CURRENT_CONFIG

from pathlib import Path
import json

CURRENT_CONFIG = None
CONFIG_FILE = Path.home()/".config"/"vi-player"/"config.json"

class Config:
    def __init__(self, data):
        self.general = data.get("general", {})
        self.general["theme"] = self.general.get("theme", "default")

    def set_theme(self, name):
        self.general["theme"] = name

    def to_dict(self):
        return {
            "general": self.general
        }

def load_config():
    global CURRENT_CONFIG

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        config = json.load(f)

    CURRENT_CONFIG = Config(config)

def save():
    global CURRENT_CONFIG

    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(CURRENT_CONFIG.to_dict(), f, indent=2)

def get_config():
    return CURRENT_CONFIG

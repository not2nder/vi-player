from pathlib import Path
import tomllib

CURRENT_CONFIG = None

class Config:
    def __init__(self, data):
        general = data.get("general", {})
        self.theme = general.get("theme", "default")

def load_config():
    global CURRENT_CONFIG
    config_file = Path.home()/".config"/"vi-player"/"config.toml"

    with open(config_file, "rb") as f:
        config = tomllib.load(f)

    CURRENT_CONFIG = Config(config)

def get_config():
    return CURRENT_CONFIG

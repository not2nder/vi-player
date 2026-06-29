import shutil
from importlib.resources import files
from pathlib import Path

def ensure_config():
    config_dir = Path.home()/".config"/"vi-player"
    themes_dir = config_dir/"themes"

    config_dir.mkdir(parents=True, exist_ok=True)
    themes_dir.mkdir(parents=True, exist_ok=True)
    
    assets = files("vi_player").joinpath("assets")
    
    config_src = assets.joinpath("config.json")
    config_dst = config_dir/"config.json"

    if not config_dst.exists():
        shutil.copy2(config_src, config_dst)

    themes_src = assets.joinpath("themes")

    for theme_src in themes_src.iterdir():
        theme_dst = themes_dir / theme_src.name

        if not theme_dst.exists():
            shutil.copy2(theme_src, theme_dst)

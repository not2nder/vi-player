import argparse
from .core.app import App
from .config.bootstrap import ensure_config
from . import __version__

def main():
    parser = argparse.ArgumentParser(
        prog = "viplay",
        description="A Vim-like music player for the terminal.",
    )

    parser.add_argument(
        "directory",
        nargs ="?",
        help  = "music directory to open", 
    )

    parser.add_argument(
        "-v",
        "--version",
        action  = "version",
        version = f"VI-PLAYER {__version__}"
    )

    args = parser.parse_args()

    ensure_config()
    app = App()

    if args.directory:
        app.mpv.playlist.load_directory(args.directory)

    app.run()

if __name__ == "__main__":
    main()

import sys
from .core.app import App
from .config.bootstrap import ensure_config

def main():
    ensure_config()
    app = App()

    if len(sys.argv) > 1:
        path = sys.argv[1]
        app.mpv.playlist.load_directory(path)

    app.run()

if __name__ == "__main__":
    main()

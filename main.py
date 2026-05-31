import sys
from core.app import App

app = App()

if len(sys.argv) > 1:
    path = sys.argv[1]
    app.mpv.playlist.load_directory(path)

app.run()

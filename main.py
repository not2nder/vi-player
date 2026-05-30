import sys
from core.app import App

app = App()

if len(sys.argv) > 1:
    path = sys.argv[1]
    app.player.load_songs(path)
else:
    app.player.playlist = []

app.run()

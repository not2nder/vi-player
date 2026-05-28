import sys
from core.app import App
from util.keyboard import getch

import signal

app = App()

if len(sys.argv) > 1:
    path = sys.argv[1]
    app.player.load_songs(path)

def handle_resize(sigun, frame):
    app.screen.clear()
    app.screen.resize()
    app.draw()

signal.signal(signal.SIGWINCH, handle_resize)
 
while app.running:

    if app.screen.check_resize():
        app.screen.resize()

    app.draw()

    key = getch()

    app.handle_key(key)


from pathlib import Path
import mpv

class Player:
    def __init__(self):
        self.playlist = []
        self.current = 0
        self.state = None
        self.song = None
        self.player = mpv.MPV(video=False)

    def load_songs(self, path):
        self.set_current(0)
        self.playlist = list(Path(path).expanduser().glob("*.mp3"))

        return self.playlist

    def play(self):
        self.song = str(self.playlist[self.current])
        self.player.play(self.song)
        self.set_state("TOCANDO")

    def pause(self):
        self.player.pause = not self.player.pause
        self.set_state("PAUSA")

    def next(self):
        self.set_current((self.current+1) % len(self.playlist))
        self.play()

    def prev(self):
        self.set_current((self.current-1) % len(self.playlist))
        self.play()

    def skip(self, index):
        if not 1 <= index <= len(self.playlist):
            return

        self.set_current(index-1)
        self.play()

    def set_state(self, text):
        self.state = text

    def get_state(self):
        return self.state

    def set_current(self, index):
        self.current = index

    def get_current(self):
        return self.current
    
    def get_playlist(self):
        return self.playlist

    def exit(self):
        self.player.terminate()

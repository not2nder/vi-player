from pathlib import Path

from core.song import Song
from core.enums import PlaybackState

import mpv

class Player:
    def __init__(self):
        self.playlist: list[Song] = []
        
        self.current: int = 0
        self.playing_song: Song = None
        
        self.state = PlaybackState.WAITING
        
        self.player = mpv.MPV(video=False)

    @property
    def count(self):
        return len(self.playlist)

    def load_songs(self, directory) -> list[Song]:
        path = Path(directory)

        if not path.exists():
            return self.playlist

        songs = [Song(file) for file in path.glob("*.mp3")]

        self.playlist = songs
        return self.playlist

    def play(self):
        if not self.playlist:
            return

        self.playing_song = self.playlist[self.current]
        self.player.play(str(self.playing_song.path))
        self.state = PlaybackState.PLAYING

    def pause(self):
        self.player.pause = not self.player.pause

        if self.player.pause:
            self.state = PlaybackState.PAUSE
        else:
            self.state = PlaybackState.PLAYING
    
    def next(self):
        self.current = (self.current+1) % self.count 
        self.player.pause = False
        self.play()

    def prev(self):
        self.current = (self.current-1) % self.count
        self.player.pause = False
        self.play()

    def skip(self, index):
        if not 1 <= index <= self.count:
            return

        self.current = index-1
        self.play()

    def get_current_song(self):
        if self.playing_song is None:
            return None
            
        self.playing_song.load_metadata()
        return self.playing_song

    def exit(self):
        self.player.terminate()

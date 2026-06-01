from pathlib import Path

from core.song import Song
from core.playlist import Playlist
from core.enums import PlaybackState

import mpv

class Player:
    def __init__(self):
        self.playlist = Playlist()
        
        self.current: int = 0
        self.playing_song: Song = None
        
        self.state = PlaybackState.WAITING
        
        self.player = mpv.MPV(video=False)

    @property
    def count(self):
        return len(self.playlist)

    @property
    def isempty(self):
        if self.playlist:
            return False 
        else:
            return True
    
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

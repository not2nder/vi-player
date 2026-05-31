from pathlib import Path

from core.song import Song

class Playlist:
    def __init__(self):
        self.songs = []

    def __len__(self):
        return len(self.songs)

    def __iter__(self):
        return iter(self.songs)
    
    def __getitem__(self, index):
        return self.songs[index]

    def __bool__(self):
        return bool(self.songs)

    def add(self, song: Song):
        self.songs.append(song)

    def load_directory(self, path):
        self.clear()
        self.add_dir(path)
    
    def add_dir(self, path):
        for file in Path(path).expanduser().glob("*.mp3"):
            self.add(Song(file))

    def remove(self, song: Song):
        self.songs.remove(song)

    def clear(self):
        self.songs.clear()



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
        path = Path(path).expanduser()

        if not path.exists():
            return None

        if not path.is_dir():
            return None

        files = list(path.glob("*.mp3"))
        for file in files:
            self.add(Song(file))

        return len(files)

    def remove(self, song: Song):
        self.songs.remove(song)

    def clear(self):
        self.songs.clear()


from pathlib import Path

from vi_player.core.song import Song

class Playlist:
    def __init__(self):
        self.songs = []
        self.register = []

    def __len__(self):
        return len(self.songs)

    def __iter__(self):
        return iter(self.songs)
    
    def __getitem__(self, index):
        return self.songs[index]

    def __bool__(self):
        return bool(self.songs)
    
    def cut(self, index):
        if index < 0 or index >= len(self.songs):
            return

        deleted = self.songs.pop(index)
        self.register.append(deleted)

    def copy(self, index):
        if index < 0 or index >= len(self.songs):
            return

        self.register.append(self.songs[index])

    def paste(self, index):
        for i in range(len(self.register)):
            self.songs.insert(index+i+1, self.register[i])

        return len(self.register)

    def clear_register(self):
        self.register.clear()

    def add(self, song: Song):
        self.songs.append(song)

    def load_directory(self, path):
        if not Path(path).expanduser().exists():
            raise FileNotFoundError(f"Can't load playlist for '{path}': no such directory")
            return

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


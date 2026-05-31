from pathlib import Path

from dataclasses import dataclass
from typing import Optional

from mutagen.easyid3 import EasyID3
from mutagen import File

@dataclass
class Song:
    path: Path

    title: Optional[str] = None
    artist: Optional[str] = None
    album: Optional[str] = None

    duration: Optional[int] = None

    def __post_init__(self):
        self.path = Path(self.path)

        if self.title is None:
            self.title = self.path.stem

    def load_metadata(self):
        try:
            audio = EasyID3(self.path)

            self.title = audio.get("title", [self.title])[0]
            self.artist = audio.get("artist", ["Unknown"])[0]
            self.album = audio.get("album", ["Unknown"])[0]

        except Exception:
            self.artist = "Desconhecido"
            self.album = "Desconhecido"

        return self

    def get_name(self) -> str:
        if self.artist:
            return f"{self.artist} - {self.title}"
        else:
            return self.title

    def get_time(self):
        duration = File(self.path).info.length
        mins = int(duration//60)
        secs = int(duration%60)

        return f"{mins}:{str(secs).rjust(2,'0')}"


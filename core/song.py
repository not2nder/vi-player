from pathlib import Path
from dataclasses import dataclass
from typing import Optional

from mutagen.easyid3 import EasyID3
from mutagen import File

@dataclass
class Song:
    path: Path

    _title: Optional[str] = None
    _artist: Optional[str] = ""
    _album: Optional[str] = ""

    _duration: Optional[float] = None

    meta_loaded: bool = False
    time_loaded: bool = False

    def __post_init__(self):
        self.path = Path(self.path)
        self._title = self.path.stem

    @property
    def title(self):
        return self._title

    @property
    def artist(self):
        self.load_metadata()
        return self._artist

    @property
    def album(self):
        self.load_metadata()
        return self._album

    @property
    def time(self):
        if not self.time_loaded:
            self._duration = File(self.path).info.length
            self.time_loaded = True

        mins = int(self._duration // 60)
        secs = int(self._duration % 60)

        return f"{mins}:{secs:02d}"

    def load_metadata(self):
        if self.meta_loaded:
            return self

        try:
            audio = EasyID3(self.path)

            self._title = audio.get("title", [self._title])[0]
            self._artist = audio.get("artist", [""])[0]
            self._album = audio.get("album", [""])[0]

        except Exception:
            self._artist = ""
            self._album = ""

        finally:
            self.meta_loaded = True

        return self

from pathlib import Path

from dataclasses import dataclass
from typing import Optional

from mutagen.easyid3 import EasyID3
from mutagen import File

@dataclass
class Song:
    path: Path

    _title: Optional[str] = None
    _artist: Optional[str] = None
    _album: Optional[str] = None

    meta_loaded: bool = False

    def __post_init__(self):
        self.path = Path(self.path)

        if self.title is None:
            self._title = self.path.stem
   
    @property
    def title(self):
        self.load_metadata()
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
        duration = File(self.path).info.length
        mins = int(duration//60)
        secs = int(duration%60)
        return f"{mins}:{str(secs).rjust(2,'0')}"

    def load_metadata(self):
        if not self.meta_loaded:
            try:
                audio = EasyID3(self.path)

                self._title = audio.get("title", [self.title])[0]
                self._artist = audio.get("artist", [""])[0]
                self._album = audio.get("album", [""])[0]
                
            except Exception:
                self._artist = ""
                self._album = ""
            
            finally:
                self.meta_loaded = True
        
        return self

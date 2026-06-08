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
    
    meta_loaded: bool = False

    def __post_init__(self):
        self.path = Path(self.path)

        if self.title is None:
            self.title = self.path.stem
   
    @property
    def name(self):
        self.load_metadata()
        return self.title

    @property
    def release(self):
        self.load_metadata()
        return self.album

    @property
    def composer(self):
        self.load_metadata()
        return self.artist

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

                self.title = audio.get("title", [self.title])[0]
                self.artist = audio.get("artist", [""])[0]
                self.album = audio.get("album", [""])[0]
                
            except Exception:
                self.artist = ""
                self.album = ""
            
            finally:
                self.meta_loaded = True
        
        return self

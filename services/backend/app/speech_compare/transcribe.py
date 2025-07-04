# speech_compare/transcribe.py
from abc import ABC, abstractmethod
from pathlib import Path
import whisperx

class AbstractTranscriber(ABC):
    @abstractmethod
    def transcribe(self, wav: Path) -> dict: ...

class WhisperXTranscriber(AbstractTranscriber):
    def __init__(self):
        self.model = whisperx.load_model("base", device="cuda", download_root=".models")
    def transcribe(self, wav: Path) -> dict:
        return self.model.transcribe(str(wav))

def get_transcriber(name="whisperx") -> AbstractTranscriber:
    if name == "whisperx": return WhisperXTranscriber()
    raise ValueError(f"Unknown transcriber {name}")

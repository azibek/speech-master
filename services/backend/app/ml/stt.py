# Whisper interface
import whisper

_model = whisper.load_model("base")

def transcribe(path: str) -> str:
    result = _model.transcribe(path, fp16=False, language="en")
    return result["text"].strip()

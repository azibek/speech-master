# speech_compare/ingest.py
from pydub import AudioSegment, effects, silence
from config import SAMPLE_RATE, DATA_DIR, PAUSE_THRESH_S
from pathlib import Path

def preprocess(src_path: Path) -> Path:
    snd = AudioSegment.from_file(src_path).set_frame_rate(SAMPLE_RATE).set_channels(1)
    snd = effects.normalize(snd)
    chunks = silence.split_on_silence(
        snd, min_silence_len=int(PAUSE_THRESH_S * 1000),
        silence_thresh=snd.dBFS - 16, keep_silence=100
    )
    cleaned = AudioSegment.empty()
    for ch in chunks: cleaned += ch
    out = DATA_DIR / f"{src_path.stem}_clean.wav"
    cleaned.export(out, format="wav")
    return out

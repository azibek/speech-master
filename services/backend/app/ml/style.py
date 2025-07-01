# Style profiling
import numpy as np, json, parselmouth
from resemblyzer import VoiceEncoder, preprocess_wav
import librosa, pathlib

encoder = VoiceEncoder()

# --- personas pre-computed at repo clone ---
PERSONA_DIR = pathlib.Path(__file__).parent.parent / "data" / "embeddings"
personas = json.loads((PERSONA_DIR / "personas_meta.json").read_text())

def extract(wav_path: str):
    wav = preprocess_wav(wav_path)
    embed = encoder.embed_utterance(wav)

    snd = parselmouth.Sound(wav_path)
    pitch = snd.to_pitch()
    mean_pitch = pitch.selected_array['frequency'][pitch.selected_array['frequency']>0].mean()
    duration = snd.get_total_duration()
    words = len(librosa.effects.split(librosa.load(wav_path, sr=16000)[0]))
    wpm = words / (duration/60)

    return embed, {"mean_pitch": mean_pitch, "wpm": wpm}

def load_persona(pid: str):
    meta = personas[pid]
    return np.array(meta["embedding"]), meta["prosody"]

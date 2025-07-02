from resemblyzer import VoiceEncoder, preprocess_wav
import parselmouth, librosa, json, pathlib, numpy as np

root = pathlib.Path(__file__).parent.parent / "data" / "personas"
out  = pathlib.Path(__file__).parent.parent / "data" / "embeddings"
out.mkdir(parents=True, exist_ok=True)

encoder = VoiceEncoder()
meta = {}

for wav_path in root.glob("*.wav"):
    pid = wav_path.stem.lower()          # e.g. mrbeast.wav → mrbeast
    wav = preprocess_wav(wav_path)
    embed = encoder.embed_utterance(wav).tolist()

    snd = parselmouth.Sound(str(wav_path))
    pitch = snd.to_pitch()
    mean_pitch = float(pitch.selected_array['frequency'][pitch.selected_array['frequency']>0].mean())

    duration = snd.get_total_duration()
    words = len(librosa.effects.split(librosa.load(wav_path, sr=16000)[0]))
    wpm = words / (duration/60)

    meta[pid] = {"embedding": embed,
                 "prosody": {"mean_pitch": mean_pitch, "wpm": wpm}}

(out / "personas_meta.json").write_text(json.dumps(meta, indent=2))
print("✅ personas_meta.json rebuilt")

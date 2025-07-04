# speech_compare/features.py
import parselmouth, librosa, numpy as np, spacy, textstat, json
from lexicalrichness import LexicalRichness
from pathlib import Path

nlp = spacy.load("en_core_web_lg")

def prosody_metrics(wav_path: Path) -> dict:
    snd = parselmouth.Sound(str(wav_path))
    pitch = snd.to_pitch()
    return {
        "duration_s": snd.get_total_duration(),
        "mean_pitch_Hz": pitch.selected_array['frequency'].mean(),
        "pitch_IQR_Hz": np.subtract(*np.percentile(pitch.values[pitch.values>0], [75, 25])),
        "jitter_local": snd.to_pitch().get_jitter_local(),
        "shimmer_local": snd.to_intensity().get_shimmer_local()
    }

def language_metrics(text: str) -> dict:
    doc = nlp(text)
    lr  = LexicalRichness(text)
    hedges = sum(1 for token in doc if token.lower_ in {"just","maybe","kind","sort"})
    return {
        "words": len(doc),
        "wpm": len(doc) / (doc[-1].whitespace_ != ""),
        "ttr": lr.ttr,
        "flesch_kincaid": textstat.flesch_kincaid_grade(text),
        "sentiment": doc._.polarity if doc.has_extension("polarity") else 0,
        "hedge_pct": hedges / max(len(doc),1)
    }

def save_metrics(path: Path, metrics: dict):
    path.write_text(json.dumps(metrics, indent=2))

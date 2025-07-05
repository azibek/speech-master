# speech_compare/features.py
import parselmouth, librosa, numpy as np, spacy, textstat, json
from lexicalrichness import LexicalRichness
from pathlib import Path
import parselmouth.praat as praat

nlp = spacy.load("en_core_web_lg")

def prosody_metrics(wav_path: Path) -> dict:
    snd   = parselmouth.Sound(str(wav_path))
    pitch = snd.to_pitch()

    # --- pitch array ---------------------------------------------------------
    freqs = pitch.selected_array['frequency']          # numpy float64[]
    freqs = freqs[freqs > 0]                           # remove unvoiced frames
    if freqs.size == 0:                                # all unvoiced?  return NaNs
        freqs = np.array([np.nan])

    # --- point-process for jitter / shimmer ----------------------------------
    pp = praat.call(snd,  # Sound + Pitch objects
                    "To PointProcess (periodic, cc)",
                    75, 500)       # min & max pitch for periodicity

    jitter_local  = praat.call(pp,
                               "Get jitter (local)", 0, 0,
                               0.0001, 0.02, 1.3)      # Praat defaults
    shimmer_local = praat.call([snd, pp], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)

    return {
        "duration_s"    : snd.get_total_duration(),
        "mean_pitch_Hz" : float(np.nanmean(freqs)),
        "pitch_IQR_Hz"  : float(np.subtract(*np.nanpercentile(freqs, [75, 25]))),
        "jitter_local"  : float(jitter_local),
        "shimmer_local" : float(shimmer_local),
    }

def language_metrics(text: str, duration_s: float) -> dict:
    doc = nlp(text)
    lr  = LexicalRichness(text)
    hedges = sum(1 for token in doc if token.lower_ in {"just","maybe","kind","sort"})
    minutes = max(duration_s / 60.0, 1e-6)
    wpm = len(doc) / minutes
    return {
        "words": len(doc),
        "wpm": wpm,
        "ttr": lr.ttr,
        "flesch_kincaid": textstat.flesch_kincaid_grade(text),
        "sentiment": doc._.polarity if doc.has_extension("polarity") else 0,
        "hedge_pct": hedges / max(len(doc),1)
    }

def save_metrics(path: Path, metrics: dict):
    path.write_text(json.dumps(metrics, indent=2))

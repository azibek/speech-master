"""
Requires:
  pip install TTS soundfile numpy
"""

import io
import soundfile as sf
from TTS.api import TTS
import torch
# ── 1. Load XTTS-v2 once at start-up ────────────────────────────────
# The first call downloads the model (~400 MB) and initialises GPUs if available.

device = "cuda" if torch.cuda.is_available() else "cpu"

_xtts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2",
            progress_bar=False, gpu=True)   # set gpu=False to force CPU

# ── 2. (Optional) very light “style” mapping  ───────────────────────
# XTTS doesn’t have ElevenLabs-style ‘VoiceSettings’, but we can tweak
# speaking rate or add text-prompt tags.  Adjust as you like.
_style_map = {
    "mrbeast": dict(speed=1.05),          # slightly faster & energetic
    "aliabdaal": dict(speed=1.00),
    "emma":    dict(speed=0.95),          # calmer
}

# ── 3. The public helper you’ll import elsewhere ────────────────────
def clone(text: str, user_wav: str, persona_style: str = "mrbeast") -> bytes:
    """
    Generate speech that mimics the voice in `user_wav`.
    
    Args:
        text:           Text to speak.
        user_wav:       Path to a short reference clip (≈6–10 s, 16-24 kHz).
        persona_style:  One of the keys in _style_map (optional).

    Returns:
        WAV bytes (PCM 24 kHz, 16-bit, mono).
    """
    # Pick style parameters if available
    style_args = _style_map.get(persona_style, {})

    # Run TTS – returns a NumPy array at 24 kHz
    audio = _xtts.tts(text=text,
                      speaker_wav=user_wav,
                      language="en",
                      **style_args)

    # Convert the NumPy signal to in-memory WAV bytes
    with io.BytesIO() as buf:
        sf.write(buf, audio, samplerate=24000, format="WAV")
        return buf.getvalue()

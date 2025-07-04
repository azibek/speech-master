# speech_compare/config.py
from pathlib import Path
import os

ROOT           = Path(__file__).resolve().parent
DATA_DIR       = ROOT.parent / "data"
REPORT_DIR     = DATA_DIR / "reports"
MODEL_CACHE    = DATA_DIR / ".models"
MODEL_CACHE.mkdir(exist_ok=True)
SAMPLE_RATE    = 16_000
PAUSE_THRESH_S = 0.25          # silence > threshold is trimmed
LLM_MODEL      = "gpt-4o-mini" # pick your OpenAI plan model
OPENAI_KEY     = os.getenv("OPENAI_API_KEY")
PERSONA_DIR    = (DATA_DIR / "personas").resolve()
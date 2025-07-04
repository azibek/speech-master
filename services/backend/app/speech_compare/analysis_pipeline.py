from pathlib import Path

from app.config import REPORT_DIR
from app.speech_compare.ingest import preprocess
from app.speech_compare.transcribe import get_transcriber
from app.speech_compare.features import prosody_metrics, language_metrics, save_metrics
from app.speech_compare.compare import diff
from app.speech_compare.coach import get_coach
from app.speech_compare.report import render

def run_pipeline(user_wav: Path, persona_wav: Path, coach_name: str, run_id: str) -> Path:
    """Core analysis; returns full path to HTML report."""
    try:
        transcriber = get_transcriber()
        user_result = transcriber.transcribe(user_wav)
        user_text    = user_result["text"]
        persona_result = transcriber.transcribe(user_wav)
        persona_text = persona_result['text']

        user_metrics    = prosody_metrics(user_wav)    | language_metrics(user_text)
        persona_metrics = prosody_metrics(persona_wav) | language_metrics(persona_text)

        delta = diff(user_metrics, persona_metrics)
        gaps  = (delta.loc["user"] - delta.loc["persona"]).nlargest(3).to_dict()

        coach = get_coach(name=coach_name)
        tips  = coach.advise(gaps)

        report_path = REPORT_DIR / f"{run_id}.html"
        render(delta, tips, out_name=run_id)  # writes the HTML
        return report_path
    except Exception as e:
        raise Exception(e)
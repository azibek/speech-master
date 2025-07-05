import traceback
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
        user_result = transcriber.transcribe(user_wav)['segments']
        user_text    = " ".join([seg['text'] for seg in user_result])
        persona_result = transcriber.transcribe(user_wav)['segments']
        persona_text = " ".join([ seg['text'] for seg in persona_result])

        
        u_pros = prosody_metrics(user_wav)
        u_lang = language_metrics(user_text, u_pros["duration_s"])
        user_metrics = u_pros | u_lang

        p_pros = prosody_metrics(persona_wav)
        p_lang = language_metrics(persona_text, p_pros["duration_s"])
        user_metrics = p_pros | p_lang

        user_metrics    = prosody_metrics(user_wav)    | language_metrics(user_text, u_pros["duration_s"])
        persona_metrics = prosody_metrics(persona_wav) | language_metrics(persona_text, p_pros["duration_s"])

        delta = diff(user_metrics, persona_metrics)
        gaps  = (delta["user"] - delta["persona"]).nlargest(3).to_dict()

        coach = get_coach(name=coach_name)
        tips  = coach.advise(gaps)

        report_path = REPORT_DIR / f"{run_id}.html"
        render(delta, tips, out_name=run_id)  # writes the HTML
        return report_path
    except Exception as e:
        print(traceback.format_exc())
        raise Exception(e)
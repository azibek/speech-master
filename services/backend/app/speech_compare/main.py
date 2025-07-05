# speech_compare/main.py
import argparse, pandas as pd
from pathlib import Path
from app.speech_compare.ingest import preprocess
from app.speech_compare.transcribe import get_transcriber
from app.speech_compare.features import prosody_metrics, language_metrics, save_metrics
from app.speech_compare.compare import diff
from app.speech_compare.coach import advise
from app.speech_compare.report import render
from app.config import DATA_DIR

def run(user_raw: Path, persona_raw: Path):
    DATA_DIR.mkdir(exist_ok=True)
    user_wav    = preprocess(user_raw)
    persona_wav = preprocess(persona_raw)

    transcriber = get_transcriber()
    u_text = transcriber.transcribe(user_wav)["text"]
    p_text = transcriber.transcribe(persona_wav)["text"]
    
    u_pros = prosody_metrics(user_wav)
    u_lang = language_metrics(u_text, u_pros["duration_s"])
    u_metrics = u_pros | u_lang

    p_pros = prosody_metrics(persona_wav)
    p_lang = language_metrics(p_text, p_pros["duration_s"])
    p_metrics = p_pros | p_lang

    save_metrics(DATA_DIR/"user.json", u_metrics)
    save_metrics(DATA_DIR/"persona.json", p_metrics)

    delta = diff(u_metrics, p_metrics)
    gaps  = delta.loc["user"] - delta.loc["persona"]
    tips  = advise(gaps.nlargest(3).to_dict())

    render(delta, tips, out_name="speech_report")
    print("✅ Report written to reports/speech_report.html")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--user", required=True,  help="path to user's audio")
    parser.add_argument("--persona", required=True, help="path to persona audio")
    run(**vars(parser.parse_args()))


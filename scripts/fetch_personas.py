#!/usr/bin/env python
"""
fetch_personas.py
-----------------
Download 30-second WAV clips for each persona.

Prereqs (install once):
  pip install yt-dlp
  # ffmpeg must be on PATH
"""

from __future__ import annotations
import argparse, json, subprocess, sys, tempfile
from pathlib import Path
from typing import List, Dict

# --------------------------------------------------------------------------- #
# 1️⃣  Persona catalogue – edit or load via --manifest
# --------------------------------------------------------------------------- #
PERSONAS: List[Dict[str, str]] = [
    # {
    #     "id": "mrbeast",
    #     "url": "https://www.youtube.com/watch?v=hTSaweR8qMI",
    #     "start": "00:00:05"      # HH:MM:SS
    # },
    # {
    #     "id": "aliabdaal",
    #     "url": "https://www.youtube.com/watch?v=ZAWvRqQwvSM",
    #     "start": "00:00:05"
    # },
    # {
    #     "id": "emmachamberlain",
    #     "url": "https://www.youtube.com/watch?v=zLlWBOkU0PA",
    #     "start": "00:09:10"
    # },
    {
        "id": "morganfreeman",
        "url": "https://www.youtube.com/watch?v=lwf8rPvLajE",
        "start" : "00:00:10"
    }
]

# --------------------------------------------------------------------------- #
# 2️⃣  Helpers
# --------------------------------------------------------------------------- #
def run(cmd: list[str]) -> None:
    """Run a subprocess, raise if non-zero."""
    subprocess.run(cmd, check=True, text=True)

def download_and_convert(id_: str, url: str, start: str,
                         duration: int, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    tmp_dir = Path(tempfile.mkdtemp())
    try:
        m4a_path = tmp_dir / f"{id_}.m4a"

        # yt-dlp: best audio-only
        print(f"➡️  {id_}: downloading audio …")
        run([
            "yt-dlp",
            "--quiet",
            "--extract-audio",
            "--audio-format", "m4a",
            "--audio-quality", "0",
            "--output", str(m4a_path),
            url,
        ])

        wav_path = out_dir / f"{id_}.wav"
        print(f"🎧  {id_}: trimming & converting → WAV …")

        # ffmpeg: trim, mono, 16 kHz, WAV
        run([
            "ffmpeg",
            "-hide_banner", "-loglevel", "error",
            "-ss", start,
            "-t", str(duration),
            "-i", str(m4a_path),
            "-ac", "1",
            "-ar", "16000",
            "-vn",  # no video
            "-y",   # overwrite
            str(wav_path),
        ])
        print(f"✅  {id_} saved to {wav_path}\n")
    finally:
        # clean temp files
        for p in tmp_dir.glob("*"):
            p.unlink(missing_ok=True)
        tmp_dir.rmdir()

# --------------------------------------------------------------------------- #
# 3️⃣  CLI
# --------------------------------------------------------------------------- #
def main(argv: List[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Download & prepare persona WAV files.")
    parser.add_argument(
        "--manifest", type=Path,
        help="Optional JSON file overriding the default persona list."
    )
    parser.add_argument(
        "--duration", type=int, default=30,
        help="Clip length in seconds (default: 30)."
    )
    args = parser.parse_args(argv)

    personas = PERSONAS
    if args.manifest:
        personas = json.loads(args.manifest.read_text())

    out_dir = Path(__file__).resolve().parents[2] / "speech-master" / "data" / "personas"

    for p in personas:
        try:
            download_and_convert(
                id_=p["id"],
                url=p["url"],
                start=p.get("start", "00:00:00"),
                duration=args.duration,
                out_dir=out_dir,
            )
        except subprocess.CalledProcessError as exc:
            print(f"⚠️  {p['id']} failed: {exc}", file=sys.stderr)

if __name__ == "__main__":
    main()

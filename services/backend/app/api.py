from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException
from pydantic import BaseModel
import uuid, tempfile, asyncio
from app.ml import stt, style, tts
from app.utils import storage, scoring

router = APIRouter()

class AnalysisResponse(BaseModel):
    transcript: str
    similarity: float
    metrics: dict[str, float]
    advice: list[str]
    reference_audio_url: str

@router.post("/analyze_and_clone", response_model=AnalysisResponse)
async def analyze_and_clone(
    persona_id: str,
    background_tasks: BackgroundTasks,
    audio: UploadFile = File(...),
):
    if audio.content_type not in ("audio/wav", "audio/wave", "audio/x-wav"):
        raise HTTPException(400, f"Please upload a WAV file. Curr file: {audio.content_type} ")

    # ---- 1. Save raw upload locally ----
    tmp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name
    with open(tmp_path, "wb") as f:
        f.write(await audio.read())

    # ---- 2. Transcribe ----
    transcript = stt.transcribe(tmp_path)

    # ---- 3. Style metrics ----
    user_vec, user_prosody = style.extract(tmp_path)
    persona_vec, persona_prosody = style.load_persona(persona_id)
    sim, metrics = scoring.compare(user_vec, user_prosody,
                                   persona_vec, persona_prosody)

    advice = scoring.generate_tips(metrics)

    # ---- 4. Voice clone in background ----
    async def clone_and_upload():
        cloned = tts.clone(text=transcript,
                           user_wav=tmp_path,
                           persona_style=persona_id)
        url = storage.upload_bytes(
            data=cloned,
            blob_name=f"data/clones/{uuid.uuid4()}.wav",
            content_type="audio/wav",
        )
        return url

    reference_audio_url = await clone_and_upload()

    # ---- 5. Upload raw clip (optional log) ----
    background_tasks.add_task(
        storage.upload_file, tmp_path, f"uploads/{uuid.uuid4()}.wav"
    )

    return AnalysisResponse(
        transcript=transcript,
        similarity=round(sim * 100, 1),
        metrics=metrics,
        advice=advice,
        reference_audio_url=reference_audio_url,
    )

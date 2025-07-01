# Voice cloning
from elevenlabs import generate, VoiceSettings
import io

def clone(text: str, user_wav: str, persona_style: str) -> bytes:
    # quick heuristic: map persona -> voice settings
    preset = {
        "mrbeast": VoiceSettings(stability=0.3, similarity_boost=0.5),
        "aliabdaal": VoiceSettings(stability=0.6, similarity_boost=0.2),
        "emma": VoiceSettings(stability=0.7, similarity_boost=0.1),
    }[persona_style]

    audio = generate(
        text=text,
        voice_cloning_enabled=True,
        voice_clone_file=user_wav,
        voice_settings=preset,
        model="eleven_multilingual_v2",
        output_format="wav"
    )
    return io.BytesIO(audio).read()

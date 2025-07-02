from elevenlabs import ElevenLabs, VoiceSettings

client = ElevenLabs()          # reads ELEVEN_API_KEY env var if set

def clone(text: str, user_wav: str, persona_style: str) -> bytes:
    style_map = {
        "mrbeast": VoiceSettings(stability=0.3, similarity_boost=0.5),
        "aliabdaal": VoiceSettings(stability=0.6, similarity_boost=0.2),
        "emma": VoiceSettings(stability=0.7, similarity_boost=0.1),
    }
    audio = client.generate(
        text=text,
        voice_clone=user_wav,                # path to the user’s clip
        voice_settings=style_map[persona_style],
        model="eleven_multilingual_v2",
        output_format="wav"
    )
    return audio  # already bytes

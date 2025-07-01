# Similarity metrics
import numpy as np

def compare(user_vec, user_prosody, persona_vec, persona_prosody):
    sim = float(np.dot(user_vec, persona_vec) /
                (np.linalg.norm(user_vec) * np.linalg.norm(persona_vec)))

    # Prosody deltas (norm-direction so higher == better match)
    wpm_ratio   = min(user_prosody["wpm"] / persona_prosody["wpm"], 2.0)
    pitch_ratio = min(user_prosody["mean_pitch"] / persona_prosody["mean_pitch"], 2.0)

    metrics = {
        "voice_embedding": sim,
        "speech_rate": wpm_ratio,
        "pitch_match": pitch_ratio
    }
    return sim, metrics

def generate_tips(metrics):
    tips = []
    if metrics["speech_rate"] < 0.8:
        tips.append("Speak faster to match energy.")
    elif metrics["speech_rate"] > 1.2:
        tips.append("Slow down slightly for clarity.")

    if metrics["pitch_match"] < 0.8:
        tips.append("Raise average pitch to convey excitement.")
    elif metrics["pitch_match"] > 1.2:
        tips.append("Lower pitch for a calmer tone.")

    if metrics["voice_embedding"] < 0.6:
        tips.append("Mimic the persona’s phrasing and word choice.")

    return tips

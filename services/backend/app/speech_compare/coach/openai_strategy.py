# speech_compare/coach/openai_strategy.py
import openai, os
from .base import CoachStrategy

_PROMPT = (
    "You are a concise speech coach. "
    "Given metric gaps below, output ONLY three bullet tips (≤ 25 words each)."
)

class OpenAICoach(CoachStrategy):
    def __init__(self, model: str = "gpt-4o-mini", api_key: str | None = None):
        openai.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model

    def advise(self, gaps: dict[str, float]) -> list[str]:
        msg = _PROMPT + "\n\nGAPS:\n" + "\n".join(f"{k}: {v:.2f}" for k, v in gaps.items())
        resp = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": msg}],
            max_tokens=120,
        )
        return [
            l.strip("•- ").strip()
            for l in resp.choices[0].message.content.splitlines()
            if l.strip()
        ][:3]

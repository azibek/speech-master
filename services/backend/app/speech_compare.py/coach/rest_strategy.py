# speech_compare/coach/rest_strategy.py
import requests, json
from .base import CoachStrategy

class RestAPICoach(CoachStrategy):
    """
    Expects POST {prompt:"…"} and returns JSON {"tips": ["tip1","tip2","tip3"]}.
    Adapt to your endpoint contract.
    """

    def __init__(self, url: str, auth_token: str | None = None, timeout: int = 30):
        self.url, self.auth_token, self.timeout = url, auth_token, timeout

    def advise(self, gaps: dict[str, float]) -> list[str]:
        prompt = (
            "Give three short speech-improvement bullets (≤ 25 words each) "
            "for the following metric gaps:\n"
            + "\n".join(f"{k}: {v:.2f}" for k, v in gaps.items())
        )
        headers = {"Authorization": f"Bearer {self.auth_token}"} if self.auth_token else {}
        resp = requests.post(self.url, headers=headers, json={"prompt": prompt}, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json().get("tips", [])[:3]

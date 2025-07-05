from __future__ import annotations
import os, re
from typing import List, Dict
from openai import OpenAI
from .base import CoachStrategy

SYSTEM_TEMPLATE = (
    "You are a concise speech coach. "
    "Use simple and easy to understand language without using speech analysis jargon"
    "Output data:"
    "1. Return exactly three bullet points (max 25 words each) to improve the "
    "speaker's delivery given the metric gaps below."
    "2. Provide 3 sample exercises and its sample responses alongwith target time for directed improvement"
)

class OllamaServerCoach(CoachStrategy):
    """
    Fetch coaching tips from a llama.cpp server that mimics the OpenAI Chat API.

    Parameters
    ----------
    base_url : str
        URL of the server root, e.g. 'http://localhost:8001/v1'.
    model    : str
        The model ID exposed by the server (often the GGUF filename stem).
    api_key  : str
        Any non-empty string; llama.cpp just checks the header exists.
    """

    def __init__(
        self,
        base_url: str = "http://127.0.0.1:11434/v1",
        model: str = "llama3.1",
        api_key: str = "llama-local-key",
        temperature: float = 0.3,
    ) -> None:
        # OpenAI Python v1 client
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.model = model
        self.temperature = temperature

    # ------------------------------------------------------------------ #

    def advise(self, gaps: Dict[str, float]) -> List[str]:
        user_prompt = "\n".join(f"{k}: {v:.2f}" for k, v in gaps.items())

        response = self.client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            max_tokens=120,
            messages=[
                {"role": "system", "content": SYSTEM_TEMPLATE},
                {"role": "user",   "content": user_prompt},
            ],
        )

        text = response.choices[0].message.content.strip()

        # extract up to three bullet lines
        tips: List[str] = []
        for line in text.splitlines():
            m = re.match(r"\s*(?:\d+[\).\-]|[•\-])\s*(.+)", line)
            tip = (m.group(1) if m else line).strip()
            if tip:
                tips.append(tip)
            if len(tips) == 3:
                break
        return tips

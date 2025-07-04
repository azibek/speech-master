# speech_compare/coach/local_strategy.py
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from .base import CoachStrategy

class LocalLLMCoach(CoachStrategy):
    """
    Example: Uses the lightweight `google/flan-t5-base`.
    Replace with any fine-tuned model you host locally.
    """
    def __init__(self, model_name: str = "google/flan-t5-base", device: int = -1):
        tok = AutoTokenizer.from_pretrained(model_name)
        mod = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        self.generator = pipeline("text2text-generation", model=mod, tokenizer=tok, device=device)

    def advise(self, gaps: dict[str, float]) -> list[str]:
        prompt = (
            "You are a concise speech coach. "
            "Return exactly three bullet tips (max 25 words each) for these metric gaps:\n"
            + "\n".join(f"{k}: {v:.2f}" for k, v in gaps.items())
        )
        out = self.generator(prompt, max_new_tokens=60)[0]["generated_text"]
        return [
            l.strip("•- ").strip()
            for l in out.splitlines()
            if l.strip()
        ][:3]

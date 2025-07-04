# speech_compare/coach/__init__.py
from .openai_strategy import OpenAICoach
from .local_strategy import LocalLLMCoach
from .rest_strategy import RestAPICoach
from .base import CoachStrategy


def get_coach(name: str = "openai", **kwargs) -> CoachStrategy:
    name = name.lower()
    if name == "openai":
        return OpenAICoach(**kwargs)
    if name == "local":
        return LocalLLMCoach(**kwargs)
    if name == "rest":
        return RestAPICoach(**kwargs)
    raise ValueError(f"Unknown coach strategy '{name}'.")

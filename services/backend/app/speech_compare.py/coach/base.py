# speech_compare/coach/base.py
from abc import ABC, abstractmethod
from typing import List


class CoachStrategy(ABC):
    """Return ≤ 3 coaching bullets for the largest metric gaps."""

    @abstractmethod
    def advise(self, gaps: dict[str, float]) -> List[str]: ...

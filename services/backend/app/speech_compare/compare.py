# speech_compare/compare.py
import pandas as pd

WEIGHTS = {
    "wpm": .25, "pitch_IQR_Hz": .20, "hedge_pct": .20,
    "ttr": .15, "jitter_local": .10, "shimmer_local": .10
}

def score(df: pd.DataFrame) -> pd.Series:
    # Normalise to 0-1 per column, then weighted sum
    norm = (df - df.min()) / (df.max() - df.min() + 1e-9)
    return norm.mul(pd.Series(WEIGHTS), axis=1).sum(axis=1)

def diff(user_metrics: dict, persona_metrics: dict) -> pd.DataFrame:
    df = pd.DataFrame([user_metrics, persona_metrics], index=["user","persona"])
    df["score"] = score(df)
    return df.T

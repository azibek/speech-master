# speech_compare/report.py
import plotly.express as px, pandas as pd, jinja2, base64, io
from app.config import REPORT_DIR

def _radar(df: pd.DataFrame) -> str:
    fig = px.line_polar(df.reset_index(), r="user", theta="index",
                        line_close=True, template="plotly_white")
    buf = io.BytesIO(); fig.write_image(buf, format="png"); buf.seek(0)
    return "data:image/png;base64,"+base64.b64encode(buf.read()).decode()

def render(df: pd.DataFrame, suggestions: list[str], out_name: str):
    template = jinja2.Template((REPORT_DIR/"template.html").read_text())
    img = _radar(df.drop("score"))
    html = template.render(table=df.to_html(), radar=img, tips=suggestions)
    (REPORT_DIR/f"{out_name}.html").write_text(html)

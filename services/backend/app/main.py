from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.backend.app.api import router
app = FastAPI(
    title="Speak-Like-Idol API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # tighten for prod
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/health", tags=["Meta"])
def health():
    return {"status": "ok"}

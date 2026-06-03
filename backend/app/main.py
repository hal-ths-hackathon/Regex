from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4

app = FastAPI(title="Regex Game API")

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/v1/stages/generate")
def generate(level: str = "easy"):
    # Minimal mock response matching documented schema
    return {
        "stage_id": str(uuid4()),
        "hint": "3桁の数字と4桁の数字をハイフンで繋いだもの",
        "noise_text": "xk3 12-345 999-8888a 123-4567 8b-9999",
        "correct_string": "123-4567",
    }


@app.get("/healthz")
def health():
    return {"status": "ok"}

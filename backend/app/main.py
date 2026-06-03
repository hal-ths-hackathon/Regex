from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4

from app.generator import generate_stage

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
    return generate_stage(level)


@app.get("/healthz")
def health():
    return {"status": "ok"}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from app.generator import generate_stage

# 開発用機能（Swagger UI / デバッグページ）は ENABLE_DEV_TOOLS=true のときだけ有効にする。
# 本番では未設定のままにすること。
ENABLE_DEV_TOOLS = os.environ.get("ENABLE_DEV_TOOLS", "").lower() in ("1", "true", "yes")

app = FastAPI(
    title="Regex Game API",
    docs_url="/docs" if ENABLE_DEV_TOOLS else None,
    redoc_url="/redoc" if ENABLE_DEV_TOOLS else None,
    openapi_url="/openapi.json" if ENABLE_DEV_TOOLS else None,
)

# CORS: 環境変数 CORS_ORIGINS からカンマ区切りで読み取り（デフォルトは開発用 localhost 3000 と Vite 5173）
_cors_env = os.environ.get("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173")
origins = [o.strip() for o in _cors_env.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=[],
)


@app.get("/api/v1/stages/generate")
def generate(level: str = "easy"):
    return generate_stage(level)


@app.get("/healthz")
def health():
    return {"status": "ok"}


if ENABLE_DEV_TOOLS:
    # Mount static files and register debug page endpoint
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

    @app.get("/debug")
    def debug():
        return FileResponse("app/static/debug.html")

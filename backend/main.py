import os
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from starlette.middleware.sessions import SessionMiddleware
from app.database import Base, engine
from app.exceptions.exceptions import AppError
from app.logging_config import configure_logging
from app.routes import auth, recommendations, playlists

configure_logging()

ORIGINS = ["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000", "http://127.0.0.1:3000"]

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.exception_handler(AppError)
async def handle_app_error(request: Request, exc: AppError) -> JSONResponse:
    logger.warning(
        f"{exc.__class__.__name__} on {request.method} {request.url.path}: {exc.message}"
    )
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


@app.exception_handler(Exception)
async def handle_unexpected_error(request: Request, exc: Exception) -> JSONResponse:
    logger.opt(exception=exc).error(
        f"Unhandled error on {request.method} {request.url.path}"
    )
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})

app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET_KEY"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(recommendations.router)
app.include_router(playlists.router)


@app.get("/health")
def health():
    return {"status": "ok"}

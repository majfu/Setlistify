from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import os
from dotenv import load_dotenv
from app.routes import auth

ORIGINS = ["http://localhost:5173", "http://localhost:3000"]

load_dotenv()

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET_KEY"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)


@app.get("/health")
def health():
    return {"status": "ok"}

import datetime

from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
import os
import httpx

SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
FRONTEND_LOGGED_IN_REDIRECT_URL = "http://127.0.0.1:5173/add-artists"
FRONTEND_LOG_IN_REDIRECT_URL = "http://127.0.0.1:5173/"

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/login")
def login():
    params = {
        "client_id": os.getenv("SPOTIFY_CLIENT_ID"),
        "response_type": "code",
        "redirect_uri": os.getenv("SPOTIFY_REDIRECT_URI"),
        "scope": "playlist-modify-public playlist-modify-private",
    }

    query = "&".join(f"{key}={value}" for key, value in params.items())

    return RedirectResponse(f"{SPOTIFY_AUTH_URL}?{query}")


@router.get("/callback")
async def callback(request: Request, code: str):
    params = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": os.getenv("SPOTIFY_REDIRECT_URI"),
        "client_id": os.getenv("SPOTIFY_CLIENT_ID"),
        "client_secret": os.getenv("SPOTIFY_CLIENT_SECRET"),
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(TOKEN_URL, data=params)

    if response.status_code != 200:
        return RedirectResponse(f"{FRONTEND_LOG_IN_REDIRECT_URL}?error=auth_failed")

    tokens = response.json()

    request.session["access_token"] = tokens["access_token"]
    request.session["refresh_token"] = tokens.get("refresh_token")

    expiry = datetime.datetime.now().timestamp() + tokens["expires_in"]
    request.session["expires_at"] = expiry

    return RedirectResponse(FRONTEND_LOGGED_IN_REDIRECT_URL)


@router.post("/refresh_token")
async def refresh_token(request: Request):
    session = request.session
    refresh_token = session.get("refresh_token")

    if not refresh_token:
        return RedirectResponse("/auth/login")

    if not _is_token_expired(session):
        return RedirectResponse(FRONTEND_LOGGED_IN_REDIRECT_URL)

    try:
        new_tokens = await _fetch_new_spotify_tokens(refresh_token)
        _update_session_with_new_tokens(session, new_tokens)
        return RedirectResponse(FRONTEND_LOGGED_IN_REDIRECT_URL)
    except Exception:
        return RedirectResponse("/auth/login")


def _is_token_expired(session: dict) -> bool:
    now = datetime.datetime.now().timestamp()
    expires_at = session.get("expires_at", 0)
    return now > (expires_at - 60)


async def _fetch_new_spotify_tokens(refresh_token: str) -> dict:
    params = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': os.getenv("SPOTIFY_CLIENT_ID"),
        'client_secret': os.getenv("SPOTIFY_CLIENT_SECRET")
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(TOKEN_URL, data=params)
        response.raise_for_status()
        return response.json()


def _update_session_with_new_tokens(session: dict, token_info: dict):
    now = datetime.datetime.now().timestamp()
    session['access_token'] = token_info['access_token']
    session['expires_at'] = now + token_info['expires_in']

    if "refresh_token" in token_info:
        session['refresh_token'] = token_info['refresh_token']

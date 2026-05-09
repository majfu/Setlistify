import os
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List

CHOSEN_MODEL = os.getenv("CHOSEN_MODEL", "CLAUDE").upper()
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-opus-4-5")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3-flash-preview")

THINKING_BUDGET_TOKENS = 2000
MAX_TOKENS = 4096
MAX_CONCURRENT_CALLS = 5

FORMAT_INSTRUCTION = (
    "You return data only in this exact format, no extra text: song,song,song"
)

if CHOSEN_MODEL == "CLAUDE":
    from anthropic import Anthropic
    _claude_client = Anthropic()
elif CHOSEN_MODEL == "GEMINI":
    import google.generativeai as genai
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    _gemini_model = genai.GenerativeModel(GEMINI_MODEL)
else:
    raise ValueError(f"Unsupported CHOSEN_MODEL: {CHOSEN_MODEL}")


def get_artist_tracks_dict(artists: List[str]) -> Dict[str, List[str]]:
    with ThreadPoolExecutor(max_workers=MAX_CONCURRENT_CALLS) as executor:
        tracks_per_artist = list(executor.map(_get_tracks_for_artist, artists))
    return dict(zip(artists, tracks_per_artist))


def _get_tracks_for_artist(artist: str) -> List[str]:
    text = _generate(_build_recommendations_prompt(artist))
    return _parse_response(text)


def _generate(prompt: str) -> str:
    if CHOSEN_MODEL == "CLAUDE":
        response = _claude_client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=MAX_TOKENS,
            thinking={"type": "enabled", "budget_tokens": THINKING_BUDGET_TOKENS},
            system=FORMAT_INSTRUCTION,
            messages=[{"role": "user", "content": prompt}],
        )
        return next((b.text for b in response.content if b.type == "text"), "")

    return _gemini_model.generate_content(
        f"{prompt}\n\n{FORMAT_INSTRUCTION}"
    ).text


def _parse_response(response_text: str) -> List[str]:
    return [track.strip() for track in response_text.split(",") if track.strip()]


def _build_recommendations_prompt(artist: str) -> str:
    return f"""Jadę na festiwal muzyczny, {artist} będzie na nim grać.

Podaj 10 piosenek tego artysty, które najczęściej pojawiają się w jego setlistach koncertowych lub są jego największymi hitami (czyli takie, które bardzo prawdopodobnie zostaną zagrane).
"""

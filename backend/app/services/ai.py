import os
from typing import Dict, List

CHOSEN_MODEL = os.getenv("CHOSEN_MODEL", "CLAUDE").upper()
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-6")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3-flash-preview")

FORMAT_INSTRUCTION = (
    "You return data only in this exact format, no extra text: "
    "artist name:song,song,song;artist name:song,song,song"
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
    text = _generate(_build_recommendations_prompt(artists))
    return _parse_response(text)


def _generate(prompt: str) -> str:
    if CHOSEN_MODEL == "CLAUDE":
        response = _claude_client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=4096,
            system=FORMAT_INSTRUCTION,
            messages=[{"role": "user", "content": prompt}],
        )
        return next((b.text for b in response.content if b.type == "text"), "")

    return _gemini_model.generate_content(
        f"{prompt}\n\n{FORMAT_INSTRUCTION}"
    ).text


def _parse_response(response_text: str) -> Dict[str, List[str]]:
    artist_tracks_dict = {}

    for entry in response_text.split(";"):
        if ":" not in entry:
            continue

        artist_name, tracks_str = entry.split(":", 1)
        artist_tracks_dict[artist_name] = [track for track in tracks_str.split(",")]

    return artist_tracks_dict


def _build_recommendations_prompt(artists: List[str]) -> str:
    return f"""Jadę na festiwal muzyczny, ci artyści będą na nim grać: {artists}

Dla każdego artysty podaj 10 piosenek, które najczęściej pojawiają się w ich setlistach koncertowych lub są ich największymi hitami (czyli takie, które bardzo prawdopodobnie zostaną zagrane).
"""

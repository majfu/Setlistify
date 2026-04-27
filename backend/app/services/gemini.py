import os
from typing import Dict, List

import google.generativeai as genai

GEMINI_MODEL = "gemini-2.0-flash"

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
_model = genai.GenerativeModel(GEMINI_MODEL)


def get_artist_tracks_dict(artists: List[str]) -> Dict[str, List[str]]:
    response = _model.generate_content(_build_recommendations_prompt(artists))
    return _parse_response(response.text)


def _parse_response(response_text: str) -> Dict[str, List[str]]:
    artist_tracks_dict = {}

    for entry in response_text.split(";"):
        if ":" not in entry:
            continue

        artist_name, tracks_str = entry.split(":", 1)
        artist_tracks_dict[artist_name] = [track for track in tracks_str.split(",")]

    return artist_tracks_dict


def _build_recommendations_prompt(artists: List[str]) -> str:
    return f"""
  Jadę na festiwal muzyczny, ci artyści będą na nim grać: {artists}

  Dla każdego artysty podaj 10 piosenek, które najczęściej pojawiają się w ich setlistach koncertowych lub są ich największymi hitami (czyli takie, które bardzo prawdopodobnie zostaną zagrane).

  Zwróć wynik dokładnie w tym formacie (bez dodatkowego tekstu):
  artist name:song,song,song,song;artist name:song,song,song,song
"""

import os
from typing import Dict, List, Tuple, Type

from loguru import logger
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from app.exceptions.exceptions import RecommendationGenerationError

CHOSEN_MODEL = os.getenv("CHOSEN_MODEL", "CLAUDE").upper()
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-opus-4-8")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3-flash-preview")

MAX_TOKENS_PER_ARTIST = 60
MAX_TOKENS_BASE = 256
MAX_TOKENS_CEILING = 8192

FORMAT_INSTRUCTION = (
    "Your ENTIRE response must be ONLY the formatted data below — no preamble, no explanation, "
    "no trailing text, no markdown, no code fences. The first character of your response must be "
    "the first artist's name.\n\n"
    "Format: artist name:song,song,song;artist name:song,song,song\n\n"
    "Use exact song titles only — no featured-artist annotations, no album names, "
    "no parentheticals, no commas inside titles. If unsure of a title, OMIT it "
    "rather than invent one."
)

_RETRYABLE_AI_ERRORS: Tuple[Type[Exception], ...] = ()

if CHOSEN_MODEL == "CLAUDE":
    from anthropic import (
        Anthropic,
        APIConnectionError,
        APITimeoutError,
        InternalServerError,
        RateLimitError,
    )

    _claude_client = Anthropic()
    _RETRYABLE_AI_ERRORS = (
        APIConnectionError,
        APITimeoutError,
        InternalServerError,
        RateLimitError,
    )
elif CHOSEN_MODEL == "GEMINI":
    import google.generativeai as genai
    from google.api_core import exceptions as google_exceptions

    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    _gemini_model = genai.GenerativeModel(GEMINI_MODEL)
    _RETRYABLE_AI_ERRORS = (
        google_exceptions.ServiceUnavailable,
        google_exceptions.TooManyRequests,
        google_exceptions.DeadlineExceeded,
        google_exceptions.InternalServerError,
    )
else:
    raise ValueError(f"Unsupported CHOSEN_MODEL: {CHOSEN_MODEL}")


def get_artist_tracks_dict(setlists_per_artist: Dict[str, set[str]]) -> Dict[str, List[str]]:
    artists = list(setlists_per_artist.keys())
    prompt = _build_recommendations_prompt(setlists_per_artist)

    try:
        text = _generate(prompt, num_artists=len(artists))
    except Exception as exc:
        logger.error(f"{CHOSEN_MODEL} recommendation generation failed: {exc!r}")
        raise RecommendationGenerationError() from exc

    logger.info(f"Generated recommendations for {len(artists)} artists")
    return _parse_response(text, expected_artists=artists)


@retry(
    reraise=True,
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=0.5, min=0.5, max=8),
    retry=retry_if_exception_type(_RETRYABLE_AI_ERRORS),
)
def _generate(prompt: str, num_artists: int) -> str:
    max_tokens = min(MAX_TOKENS_CEILING, MAX_TOKENS_BASE + MAX_TOKENS_PER_ARTIST * num_artists)

    if CHOSEN_MODEL == "CLAUDE":
        response = _claude_client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=max_tokens,
            messages=[
                {"role": "user", "content": f"{prompt}\n\n{FORMAT_INSTRUCTION}"},
            ],
        )
        return next((b.text for b in response.content if b.type == "text"), "")

    return _gemini_model.generate_content(f"{prompt}\n\n{FORMAT_INSTRUCTION}").text


def _parse_response(response_text: str, expected_artists: List[str]) -> Dict[str, List[str]]:
    response_text = _trim_to_first_artist(response_text, expected_artists)

    artist_tracks_dict = {}
    for entry in response_text.split(";"):
        if ":" not in entry:
            continue

        artist_name, tracks_str = entry.split(":", 1)
        artist_tracks_dict[artist_name.strip()] = [
            track.strip() for track in tracks_str.split(",") if track.strip()
        ]

    return artist_tracks_dict


def _trim_to_first_artist(response_text: str, expected_artists: List[str]) -> str:
    artist_positions = (response_text.lower().find(artist.lower()) for artist in expected_artists)
    found_positions = (position for position in artist_positions if position >= 0)

    if not found_positions:
        return response_text

    first_artist_position = min(found_positions)
    return response_text[first_artist_position:]


def _build_recommendations_prompt(setlists_per_artist: Dict[str, set[str]]) -> str:
    context_block = "\n".join(
        _format_artist_line(artist, songs) for artist, songs in setlists_per_artist.items()
    )

    return (
        "Jadę na festiwal muzyczny. Dla każdego z poniższych artystów podaj 15 piosenek, "
        "które najprawdopodobniej zagrają na żywo — kluczem jest częstotliwość pojawiania się "
        "w niedawnych setlistach koncertowych, a w drugiej kolejności bycie ich największymi hitami.\n\n"
        "Poniżej masz piosenki, które każdy z artystów zagrał niedawno na żywo. "
        "Traktuj je jako potwierdzone, prawdziwe tytuły z prawdziwych setlistów — "
        "użyj ich jako punktu odniesienia, żeby nie wymyślać nieistniejących piosenek. "
        "MOŻESZ je podać w odpowiedzi, jeśli pasują, ale uzupełnij listę o inne piosenki, "
        "co do których masz pewność, że artysta gra je na żywo:\n"
        f"{context_block}\n\n"
        "Wymagania:\n"
        "- Dokładnie 15 piosenek na każdego artystę.\n"
        "- Jeśli dla artysty nie ma żadnych piosenek powyżej, podaj 15 jego największych hitów.\n"
        "- Jeśli nie jesteś pewien tytułu, POMIŃ go zamiast zgadywać — lepiej mniej piosenek niż wymyślone.\n"
    )


def _format_artist_line(artist: str, songs: set[str]) -> str:
    songs_str = ", ".join(songs) if songs else "(brak danych)"
    return f"- {artist}: {songs_str}"

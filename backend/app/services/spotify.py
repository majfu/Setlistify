from collections import Counter
from typing import Dict, List, Optional, Set, Tuple
from urllib.parse import quote

import requests

from app.schemas.recommendations import ArtistRecommendation, TrackData

SPOTIFY_API_BASE_URL = "https://api.spotify.com/v1/"
SEARCH_TRACKS_LIMIT_PER_ARTIST = 15


def build_gemini_recommendations(
        artist_tracks: Dict[str, List[str]],
        headers: dict,
) -> Tuple[List[ArtistRecommendation], Set[str]]:
    recommendations = []
    seen_uris = set()

    for artist, tracks in artist_tracks.items():
        track_items = [_search_track(track, artist, headers) for track in tracks]
        track_items = [track for track in track_items if track is not None]

        if not track_items:
            continue

        for track in track_items:
            seen_uris.add(track["uri"])

        artist_name = _most_common_artist(track_items)
        track_data = _build_track_data_dict(track_items, is_gemini_recommended=True)

        recommendations.append(ArtistRecommendation(artistName=artist_name, tracks=track_data))

    return recommendations, seen_uris


def build_search_recommendations(
        artists: List[str],
        headers: dict,
        seen_uris: Set[str],
) -> List[ArtistRecommendation]:
    recommendations = []

    for artist in artists:
        track_items = _search_tracks_by_artist(artist, headers, SEARCH_TRACKS_LIMIT_PER_ARTIST)
        unique_track_items = [track for track in track_items if track["uri"] not in seen_uris]

        if not unique_track_items:
            continue

        artist_name = _most_common_artist(unique_track_items)
        track_data = _build_track_data_dict(unique_track_items, is_gemini_recommended=False)

        recommendations.append(ArtistRecommendation(artistName=artist_name, tracks=track_data))

    return recommendations


def _search_tracks_by_artist(artist: str, headers: dict, limit: int) -> List[dict]:
    query = quote(f"artist:{artist}")
    url = f"{SPOTIFY_API_BASE_URL}search?q={query}&type=track&limit={limit}"
    response = requests.get(url, headers=headers)

    return response.json()["tracks"]["items"]


def _search_track(track: str, artist: str, headers: dict) -> Optional[dict]:
    query = quote(f"track:{track} artist:{artist}")
    url = f"{SPOTIFY_API_BASE_URL}search?q={query}&type=track&limit=1"
    response = requests.get(url, headers=headers)

    items = response.json()["tracks"]["items"]
    return items[0] if items else None


def _most_common_artist(track_items: List[dict]) -> str:
    return Counter(track["artists"][0]["name"] for track in track_items).most_common(1)[0][0]


def _build_track_data_dict(
        track_items: List[dict],
        is_gemini_recommended: bool,
) -> Dict[str, TrackData]:
    return {
        track["name"]: TrackData(
            uri=track["uri"],
            isGeminiRecommended=is_gemini_recommended,
            popularity=track.get("popularity"),
        )
        for track in track_items
    }

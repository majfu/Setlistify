from collections import Counter
from typing import Dict, List, Optional, Set, Tuple
from urllib.parse import quote

import requests
from loguru import logger

from app.exceptions.exceptions import SpotifyError
from app.services.retry import retry_external_call
from app.schemas.recommendations import ArtistRecommendation, TrackData

SPOTIFY_API_BASE_URL = "https://api.spotify.com/v1/"
SEARCH_TRACKS_LIMIT_PER_ARTIST = 15
MAX_TRACKS_PER_REQUEST = 100
REQUEST_TIMEOUT = 10


@retry_external_call
def _request(method: str, url: str, **kwargs) -> requests.Response:
    response = requests.request(method, url, timeout=REQUEST_TIMEOUT, **kwargs)
    response.raise_for_status()
    return response


def _spotify_request(method: str, url: str, **kwargs) -> requests.Response:
    try:
        return _request(method, url, **kwargs)
    except requests.RequestException as exc:
        logger.error(f"Spotify {method} {url} failed: {exc!r}")
        raise SpotifyError() from exc


def create_empty_playlist(playlist_title: str, headers: dict) -> Tuple[str, str]:
    url = f"{SPOTIFY_API_BASE_URL}me/playlists"
    response = _spotify_request("POST", url, headers=headers, json={"name": playlist_title})

    body = response.json()
    if "id" not in body or "uri" not in body:
        logger.error(f"Spotify create-playlist returned unexpected body: {body}")
        raise SpotifyError("Spotify did not return a playlist id")

    logger.info(f"Created Spotify playlist {body['id']}")
    return body["id"], body["uri"]


def add_tracks_to_playlist(playlist_id: str, uris: List[str], headers: dict) -> None:
    url = f"{SPOTIFY_API_BASE_URL}playlists/{playlist_id}/tracks"
    for start in range(0, len(uris), MAX_TRACKS_PER_REQUEST):
        batch = uris[start:start + MAX_TRACKS_PER_REQUEST]
        _spotify_request("POST", url, headers=headers, json={"uris": batch})

    logger.info(f"Added {len(uris)} tracks to Spotify playlist {playlist_id}")


def delete_playlist(playlist_id: str, headers: dict) -> None:
    url = f"{SPOTIFY_API_BASE_URL}playlists/{playlist_id}/followers"
    _spotify_request("DELETE", url, headers=headers)


def build_ai_recommendations(
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
        track_data = _build_track_data_dict(track_items, is_ai_recommended=True)

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
        track_data = _build_track_data_dict(unique_track_items, is_ai_recommended=False)

        recommendations.append(ArtistRecommendation(artistName=artist_name, tracks=track_data))

    return recommendations


def _search_tracks_by_artist(artist: str, headers: dict, limit: int) -> List[dict]:
    query = quote(f"artist:{artist}")
    url = f"{SPOTIFY_API_BASE_URL}search?q={query}&type=track&limit={limit}"
    response = _spotify_request("GET", url, headers=headers)

    return _extract_track_items(response)


def _search_track(track: str, artist: str, headers: dict) -> Optional[dict]:
    query = quote(f"track:{track} artist:{artist}")
    url = f"{SPOTIFY_API_BASE_URL}search?q={query}&type=track&limit=1"
    response = _spotify_request("GET", url, headers=headers)

    items = _extract_track_items(response)
    return items[0] if items else None


def _extract_track_items(response: requests.Response) -> List[dict]:
    body = response.json()
    if "tracks" not in body:
        return []
    return body["tracks"]["items"]


def _most_common_artist(track_items: List[dict]) -> str:
    return Counter(track["artists"][0]["name"] for track in track_items).most_common(1)[0][0]


def _build_track_data_dict(
        track_items: List[dict],
        is_ai_recommended: bool,
) -> Dict[str, TrackData]:
    return {
        track["name"]: TrackData(
            uri=track["uri"],
            isAIRecommended=is_ai_recommended,
            popularity=track.get("popularity"),
        )
        for track in track_items
    }

import requests
from fastapi import APIRouter, Request, status

from app.schemas.playlists import PlaylistCreate
from app.services.spotify import SPOTIFY_API_BASE_URL

router = APIRouter(prefix="/playlists", tags=["playlists"])

MAX_TRACKS_PER_REQUEST = 100


@router.post("/", status_code=status.HTTP_200_OK)
def create_playlist(playlist_data: PlaylistCreate, request: Request):
    playlist_title = playlist_data.playlistTitle
    playlist_tracks = playlist_data.selectedTracks
    uris = [track.uri for track in playlist_tracks]

    access_token = request.session.get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}

    playlist_id = _create_empty_playlist(playlist_title, headers)
    if playlist_id is None:
        return

    _add_tracks_to_playlist(playlist_id, uris, headers)


def _create_empty_playlist(playlist_title: str, headers: dict) -> str | None:
    url = f"{SPOTIFY_API_BASE_URL}me/playlists"
    response = requests.post(url, headers=headers, json={"name": playlist_title})
    return response.json().get("id")


def _add_tracks_to_playlist(playlist_id: str, uris: list[str], headers: dict) -> None:
    url = f"{SPOTIFY_API_BASE_URL}playlists/{playlist_id}/tracks"
    for start in range(0, len(uris), MAX_TRACKS_PER_REQUEST):
        batch = uris[start:start + MAX_TRACKS_PER_REQUEST]
        requests.post(url, headers=headers, json={"uris": batch})

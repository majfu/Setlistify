from fastapi import APIRouter, Request, status

from app.schemas.playlists import PlaylistCreate
from app.services import spotify

router = APIRouter(prefix="/playlists", tags=["playlists"])


@router.post("/", status_code=status.HTTP_200_OK)
def create_playlist(playlist_data: PlaylistCreate, request: Request):
    playlist_title = playlist_data.playlistTitle
    playlist_tracks = playlist_data.selectedTracks
    uris = [track.uri for track in playlist_tracks]

    access_token = request.session.get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}

    playlist_id = spotify.create_empty_playlist(playlist_title, headers)
    if playlist_id is None:
        return

    spotify.add_tracks_to_playlist(playlist_id, uris, headers)

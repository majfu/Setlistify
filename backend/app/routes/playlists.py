from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.playlists import PlaylistCreate
from app.services import playlist_store, spotify

router = APIRouter(prefix="/playlists", tags=["playlists"])


@router.post("/", status_code=status.HTTP_200_OK)
def create_playlist(
        playlist_data: PlaylistCreate,
        request: Request,
        db: Session = Depends(get_db),
):
    playlist_title = playlist_data.playlistTitle
    selected_tracks = playlist_data.selectedTracks
    uris = [track.uri for track in selected_tracks]

    access_token = request.session.get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}

    playlist_data = spotify.create_empty_playlist(playlist_title, headers)
    if playlist_data is None:
        return

    spotify_id, spotify_uri = playlist_data
    spotify.add_tracks_to_playlist(spotify_id, uris, headers)
    playlist_store.save_playlist(db, playlist_title, spotify_id, spotify_uri, selected_tracks)

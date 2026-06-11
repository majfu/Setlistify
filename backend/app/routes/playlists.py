from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.playlists import PlaylistCreate, PlaylistRead, PlaylistsPage
from app.services import playlist_store, spotify

router = APIRouter(prefix="/playlists", tags=["playlists"])


@router.get("/", response_model=PlaylistsPage)
def list_playlists(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    playlists, total = playlist_store.get_playlists_page(db, page, page_size)
    return PlaylistsPage(
        playlists=[
            PlaylistRead(id=p.id, title=p.title, createdAt=p.created_at)
            for p in playlists
        ],
        total=total,
    )


@router.delete("/{playlist_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_playlist(playlist_id: int, request: Request, db: Session = Depends(get_db)):
    playlist = playlist_store.get_playlist(db, playlist_id)
    if playlist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    access_token = request.session.get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}

    spotify.delete_playlist(playlist.spotify_id, headers)
    playlist_store.delete_playlist(db, playlist)


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

from fastapi import APIRouter, Depends, Query, status
from loguru import logger
from sqlalchemy.orm import Session

from app.database import get_db
from app.routes.dependencies import get_auth_headers
from app.exceptions.exceptions import PlaylistNotFoundError
from app.schemas.playlists import (
    PlaylistAddTracks,
    PlaylistCreate,
    PlaylistRead,
    PlaylistsPage,
)
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
def delete_playlist(
    playlist_id: int,
    db: Session = Depends(get_db),
    headers: dict = Depends(get_auth_headers),
):
    playlist = playlist_store.get_playlist(db, playlist_id)
    if playlist is None:
        raise PlaylistNotFoundError()

    spotify.delete_playlist(playlist.spotify_id, headers)
    playlist_store.delete_playlist(db, playlist)


@router.post("/", status_code=status.HTTP_200_OK)
def create_playlist(
    payload: PlaylistCreate,
    db: Session = Depends(get_db),
    headers: dict = Depends(get_auth_headers),
):
    selected_tracks = payload.selectedTracks
    uris = [track.uri for track in selected_tracks]

    spotify_id, spotify_uri = spotify.create_empty_playlist(payload.playlistTitle, headers)
    spotify.add_tracks_to_playlist(spotify_id, uris, headers)
    playlist_store.save_playlist(
        db, payload.playlistTitle, spotify_id, spotify_uri, selected_tracks
    )
    logger.info(f"Created playlist {payload.playlistTitle!r} ({len(uris)} tracks)")


@router.post("/{playlist_id}/tracks", status_code=status.HTTP_200_OK)
def add_tracks(
    playlist_id: int,
    payload: PlaylistAddTracks,
    db: Session = Depends(get_db),
    headers: dict = Depends(get_auth_headers),
):
    playlist = playlist_store.get_playlist(db, playlist_id)
    if playlist is None:
        raise PlaylistNotFoundError()

    to_add = playlist_store.filter_out_existing_tracks(playlist, payload.selectedTracks)
    if not to_add:
        return

    uris = [track.uri for track in to_add]
    spotify.add_tracks_to_playlist(playlist.spotify_id, uris, headers)
    playlist_store.add_tracks(db, playlist, to_add)
    logger.info(f"Added {len(uris)} tracks to playlist {playlist_id}")

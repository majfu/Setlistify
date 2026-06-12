from typing import List, Optional, Tuple

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.artist import Artist
from app.models.playlist import Playlist
from app.models.playlist_track import PlaylistTrack
from app.models.track import Track
from app.schemas.playlists import SelectedTrack


def save_playlist(
    db: Session,
    title: str,
    spotify_id: str,
    spotify_uri: str,
    tracks: List[SelectedTrack],
) -> Playlist:
    playlist = Playlist(title=title, spotify_id=spotify_id, spotify_uri=spotify_uri)
    db.add(playlist)
    db.flush()

    _link_new_tracks(db, playlist, tracks)

    db.commit()
    db.refresh(playlist)
    return playlist


def add_tracks(
    db: Session, playlist: Playlist, tracks: List[SelectedTrack]
) -> List[SelectedTrack]:
    added = _link_new_tracks(db, playlist, tracks)
    db.commit()
    return added


def filter_out_existing_tracks(
    playlist: Playlist, tracks: List[SelectedTrack]
) -> List[SelectedTrack]:
    existing_uris = {link.track.spotify_uri for link in playlist.track_links}
    new_tracks: List[SelectedTrack] = []

    for track in tracks:
        if track.uri in existing_uris:
            continue
        existing_uris.add(track.uri)
        new_tracks.append(track)

    return new_tracks


def _link_new_tracks(
    db: Session, playlist: Playlist, tracks: List[SelectedTrack]
) -> List[SelectedTrack]:
    added = filter_out_existing_tracks(playlist, tracks)
    for selected in added:
        artist = _get_or_create_artist(db, selected.artistName)
        track = _get_or_create_track(db, selected, artist)
        db.add(
            PlaylistTrack(
                playlist_id=playlist.id,
                track_id=track.id,
                is_ai_recommended=selected.isAIRecommended,
                is_selected=selected.isSelected,
            )
        )
    return added


def get_playlists_page(
    db: Session, page: int, page_size: int
) -> Tuple[List[Playlist], int]:
    total = db.scalar(select(func.count()).select_from(Playlist)) or 0
    playlists_query = (
        select(Playlist)
        .order_by(Playlist.created_at.desc(), Playlist.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    playlists = list(db.scalars(playlists_query).all())
    return playlists, total


def get_playlist(db: Session, playlist_id: int) -> Optional[Playlist]:
    return db.query(Playlist).filter(Playlist.id == playlist_id).first()


def delete_playlist(db: Session, playlist: Playlist) -> None:
    db.delete(playlist)
    db.commit()


def _get_or_create_artist(db: Session, name: str) -> Artist:
    artist = db.query(Artist).filter(Artist.name == name).first()
    if artist is None:
        artist = Artist(name=name)
        db.add(artist)
        db.flush()
    return artist


def _get_or_create_track(db: Session, selected: SelectedTrack, artist: Artist) -> Track:
    track = db.query(Track).filter(Track.spotify_uri == selected.uri).first()
    if track is None:
        track = Track(
            title=selected.title,
            spotify_uri=selected.uri,
            popularity_rating=selected.popularity,
            artist_id=artist.id,
        )
        db.add(track)
        db.flush()
    return track

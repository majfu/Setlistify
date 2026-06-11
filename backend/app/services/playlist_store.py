from typing import List

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

    for selected in tracks:
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

    db.commit()
    db.refresh(playlist)
    return playlist


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

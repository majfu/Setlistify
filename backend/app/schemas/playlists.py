from pydantic import BaseModel

from app.schemas.recommendations import TrackData


class PlaylistCreate(BaseModel):
    playlistTitle: str
    selectedTracks: list[TrackData]
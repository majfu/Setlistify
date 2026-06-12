from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SelectedTrack(BaseModel):
    title: str
    artistName: str
    uri: str
    isAIRecommended: bool = False
    popularity: Optional[int] = None
    isSelected: bool = False


class PlaylistCreate(BaseModel):
    playlistTitle: str
    selectedTracks: list[SelectedTrack]


class PlaylistAddTracks(BaseModel):
    selectedTracks: list[SelectedTrack]


class PlaylistRead(BaseModel):
    id: int
    title: str
    createdAt: datetime


class PlaylistsPage(BaseModel):
    playlists: list[PlaylistRead]
    total: int

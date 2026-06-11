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

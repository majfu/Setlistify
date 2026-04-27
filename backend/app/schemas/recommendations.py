from pydantic import BaseModel
from typing import Dict, List, Optional


class ArtistsList(BaseModel):
    artistsList: List[str]


class TrackData(BaseModel):
    uri: str
    isGeminiRecommended: bool
    popularity: Optional[int] = None


class ArtistRecommendation(BaseModel):
    artistName: str
    tracks: Dict[str, TrackData]


class RecommendationsResponse(BaseModel):
    recommendations: List[ArtistRecommendation]

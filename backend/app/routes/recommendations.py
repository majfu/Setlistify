from fastapi import APIRouter, Depends, status
from loguru import logger

from app.routes.dependencies import get_auth_headers
from app.schemas.recommendations import ArtistsList, RecommendationsResponse
from app.services import ai, setlist, spotify

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.post("/", response_model=RecommendationsResponse, status_code=status.HTTP_200_OK)
def get_recommendations(
    artists_list: ArtistsList,
    headers: dict = Depends(get_auth_headers),
):
    artists = artists_list.artistsList

    setlists_per_artist = setlist.get_recent_song_names_per_artist(artists)
    artist_tracks = ai.get_artist_tracks_dict(setlists_per_artist)
    ai_recs, seen_uris = spotify.build_ai_recommendations(artist_tracks, headers)
    search_recs = spotify.build_search_recommendations(artists, headers, seen_uris)

    merged = {rec.artistName: rec for rec in ai_recs}
    for rec in search_recs:
        if rec.artistName in merged:
            merged[rec.artistName].tracks.update(rec.tracks)
        else:
            merged[rec.artistName] = rec

    return RecommendationsResponse(recommendations=list(merged.values()))

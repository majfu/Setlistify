from fastapi import APIRouter, Request, status

from app.schemas.recommendations import ArtistsList, RecommendationsResponse
from app.services import ai, spotify

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.post("/", response_model=RecommendationsResponse, status_code=status.HTTP_200_OK)
def get_recommendations(artists_list: ArtistsList, request: Request):
    access_token = request.session.get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}
    artists = artists_list.artistsList

    artist_tracks = ai.get_artist_tracks_dict(artists)
    ai_recs, seen_uris = spotify.build_ai_recommendations(artist_tracks, headers)
    search_recs = spotify.build_search_recommendations(artists, headers, seen_uris)

    merged = {rec.artistName: rec for rec in ai_recs}
    for rec in search_recs:
        if rec.artistName in merged:
            merged[rec.artistName].tracks.update(rec.tracks)
        else:
            merged[rec.artistName] = rec

    return RecommendationsResponse(recommendations=list(merged.values()))

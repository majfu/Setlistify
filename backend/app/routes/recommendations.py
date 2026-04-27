from fastapi import APIRouter, Request, status

from app.schemas.recommendations import ArtistsList, RecommendationsResponse
from app.services import gemini, spotify

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.post("/", response_model=RecommendationsResponse, status_code=status.HTTP_200_OK)
def get_recommendations(artists_list: ArtistsList, request: Request):
    access_token = request.session.get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}
    artists = artists_list.artistsList

    artist_tracks = gemini.get_artist_tracks_dict(artists)
    gemini_recs, seen_uris = spotify.build_gemini_recommendations(artist_tracks, headers)
    search_recs = spotify.build_search_recommendations(artists, headers, seen_uris)

    return RecommendationsResponse(recommendations=gemini_recs + search_recs)

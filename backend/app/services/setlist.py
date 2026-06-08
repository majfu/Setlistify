import os
from typing import Iterator, List

import requests

SETLIST_API_BASE_URL = "https://api.setlist.fm/rest"
SEARCH_SETLIST_URL = "/1.0/search/setlists"
SETLIST_API_KEY = os.getenv("SETLIST_API_KEY")

SETLISTS_TO_FETCH = 2


def get_recent_song_names(artist_name: str) -> set[str]:
    setlists = _fetch_setlists(artist_name)[:SETLISTS_TO_FETCH]
    return set(_iter_song_names(setlists))


def _fetch_setlists(artist_name: str) -> List[dict]:
    headers = {
        "x-api-key": SETLIST_API_KEY,
        "Accept": "application/json",
    }
    params = {"artistName": artist_name}
    response = requests.get(
        f"{SETLIST_API_BASE_URL}{SEARCH_SETLIST_URL}",
        headers=headers,
        params=params,
    )

    return response.json()["setlist"]


def _iter_song_names(setlists: List[dict]) -> Iterator[str]:
    for setlist in setlists:
        for set_block in setlist["sets"]["set"]:
            for song in set_block["song"]:
                yield song["name"]

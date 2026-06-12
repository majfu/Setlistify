import pytest

from app.services import playlist_store


@pytest.mark.parametrize(
    "page, page_size, expected_count",
    [
        (1, 2, 2),
        (3, 2, 1),
        (1, 10, 5),
        (4, 2, 0),
    ],
)
def test_list_playlists_pagination(client, make_playlist, page, page_size, expected_count):
    for i in range(5):
        make_playlist(f"P{i}")

    response = client.get("/playlists/", params={"page": page, "page_size": page_size})

    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 5
    assert len(body["playlists"]) == expected_count


def test_delete_playlist_removes_it(client, db_session, make_playlist, monkeypatch):
    unfollowed = {}
    monkeypatch.setattr(
        "app.services.spotify.delete_playlist",
        lambda spotify_id, headers: unfollowed.update(id=spotify_id),
    )
    playlist_id = make_playlist("ToDelete")

    response = client.delete(f"/playlists/{playlist_id}")

    assert response.status_code == 204
    assert unfollowed["id"] == "sid-ToDelete"
    assert playlist_store.get_playlist(db_session, playlist_id) is None


def test_delete_missing_playlist_returns_404(client):
    response = client.delete("/playlists/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Playlist not found"}


def test_delete_without_auth_returns_401(app, make_playlist):
    from fastapi.testclient import TestClient

    playlist_id = make_playlist("NeedsAuth")
    unauthenticated = TestClient(app)

    response = unauthenticated.delete(f"/playlists/{playlist_id}")

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated with Spotify"}


def test_add_tracks_only_persists_new_ones(client, db_session, make_playlist, monkeypatch):
    added_to_spotify = {}
    monkeypatch.setattr(
        "app.services.spotify.add_tracks_to_playlist",
        lambda spotify_id, uris, headers: added_to_spotify.update(uris=uris),
    )
    playlist_id = make_playlist("Existing", track_count=1)
    existing_uri = "spotify:track:Existing-0"

    payload = {
        "selectedTracks": [
            {"title": "Existing song 0", "artistName": "Test Artist", "uri": existing_uri},
            {"title": "Brand new", "artistName": "Test Artist", "uri": "spotify:track:new-1"},
        ]
    }
    response = client.post(f"/playlists/{playlist_id}/tracks", json=payload)

    assert response.status_code == 200
    assert added_to_spotify["uris"] == ["spotify:track:new-1"]
    playlist = playlist_store.get_playlist(db_session, playlist_id)
    assert len(playlist.track_links) == 2

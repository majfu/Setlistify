import pytest
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from starlette.middleware.sessions import SessionMiddleware

from app.database import Base, get_db
from app.exceptions.exceptions import AppError
from app.models import artist, playlist, playlist_track, track
from app.routes import playlists
from app.routes.dependencies import get_auth_headers
from app.schemas.playlists import SelectedTrack
from app.services import playlist_store

FAKE_HEADERS = {"Authorization": "Bearer test-token"}


@pytest.fixture
def db_session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = TestingSession()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)


@pytest.fixture
def app(db_session):
    test_app = FastAPI()
    test_app.add_middleware(SessionMiddleware, secret_key="test-secret")

    @test_app.exception_handler(AppError)
    async def _handle_app_error(request, exc: AppError):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})

    test_app.include_router(playlists.router)
    test_app.dependency_overrides[get_db] = lambda: db_session
    return test_app


@pytest.fixture
def client(app):
    app.dependency_overrides[get_auth_headers] = lambda: FAKE_HEADERS
    return TestClient(app)


@pytest.fixture
def make_playlist(db_session):

    def _make(title: str, *, track_count: int = 0) -> int:
        tracks = [
            SelectedTrack(
                title=f"{title} song {i}",
                artistName="Test Artist",
                uri=f"spotify:track:{title}-{i}",
                isSelected=True,
            )
            for i in range(track_count)
        ]
        created = playlist_store.save_playlist(
            db_session, title, f"sid-{title}", f"spotify:playlist:{title}", tracks
        )
        return created.id

    return _make

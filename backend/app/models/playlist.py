from app.database import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class Playlist(Base):
    __tablename__ = "playlists"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    spotify_uri = Column(String(200), nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    track_links = relationship("PlaylistTrack", back_populates="playlist", cascade="all, delete-orphan")

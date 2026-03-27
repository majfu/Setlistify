from app.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Track(Base):
    __tablename__ = "tracks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    spotify_uri = Column(String(200), nullable=False, unique=True)
    popularity_rating = Column(Integer, nullable=True)

    artist_id = Column(Integer, ForeignKey("artists.id"), nullable=False)
    artist = relationship("Artist", back_populates="tracks")

    playlist_links = relationship("PlaylistTrack", back_populates="tracks")
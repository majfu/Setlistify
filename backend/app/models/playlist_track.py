from app.database import Base
from sqlalchemy import Column, Integer, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship


class PlaylistTrack(Base):
    __tablename__ = "playlist_tracks"
    __table_args__ = UniqueConstraint("playlist_id", "track_id")

    id = Column(Integer, primary_key=True)
    playlist_id = Column(Integer, ForeignKey("playlists.id"), nullable=False)
    track_id = Column(Integer, ForeignKey("tracks.id"), nullable=False)

    is_ai_recommended = Column(Boolean, default=False)
    is_selected = Column(Boolean, default=False)

    playlist = relationship("Playlist", back_populates="track_links")
    track = relationship("Track", back_populates="playlist_links")

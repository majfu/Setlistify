from app.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Artist(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, unique=True)

    tracks = relationship("Track", back_populates="artist")

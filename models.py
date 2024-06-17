# models.py

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Film(Base):
    __tablename__ = 'films'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    release_date = Column(Date)
    genre = Column(String(100))

class Series(Base):
    __tablename__ = 'series'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    release_date = Column(Date)
    genre = Column(String(100))
    seasons = Column(Integer)

class Statistics(Base):
    __tablename__ = 'statistics'

    id = Column(Integer, primary_key=True, index=True)
    film_id = Column(Integer, ForeignKey('films.id'))
    series_id = Column(Integer, ForeignKey('series.id'))
    date = Column(Date)
    views = Column(Integer)
    likes = Column(Integer)
    dislikes = Column(Integer)

    film = relationship("Film", back_populates="statistics")
    series = relationship("Series", back_populates="statistics")

Film.statistics = relationship("Statistics", back_populates="film")
Series.statistics = relationship("Statistics", back_populates="series")

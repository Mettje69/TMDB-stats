from sqlalchemy.orm import Session
from models import Film, Series, Statistics

def get_movies(db: Session):
    return db.query(Film).all()

def get_series(db: Session):
    return db.query(Series).all()

def get_movie_by_id(db: Session, movie_id: int):
    return db.query(Film).filter(Film.id == movie_id).first()

def get_series_by_id(db: Session, series_id: int):
    return db.query(Series).filter(Series.id == series_id).first()

def get_statistics_for_movie(db: Session, movie_id: int):
    return db.query(Statistics).filter(Statistics.film_id == movie_id).all()

def get_statistics_for_series(db: Session, series_id: int):
    return db.query(Statistics).filter(Statistics.series_id == series_id).all()

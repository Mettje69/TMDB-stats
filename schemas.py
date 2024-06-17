from pydantic import BaseModel
from datetime import date

class FilmBase(BaseModel):
    title: str
    director: str
    release_date: date
    genre: str
    rating: int

class FilmCreate(FilmBase):
    pass

class Film(FilmBase):
    id: int

    class Config:
        orm_mode = True

class SeriesBase(BaseModel):
    title: str
    seasons: int
    release_date: date
    genre: str
    rating: int

class SeriesCreate(SeriesBase):
    pass

class Series(SeriesBase):
    id: int

    class Config:
        orm_mode = True

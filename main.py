from fastapi import FastAPI, Depends, Request
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from database import engine, SessionLocal
import models, crud, schemas

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root(request: Request, db: Session = Depends(get_db)):
    movies = crud.get_movies(db)
    series = crud.get_series(db)
    return templates.TemplateResponse("index.html", {"request": request, "movies": movies, "series": series})

@app.get("/movie/{movie_id}")
def read_movie(request: Request, movie_id: int, db: Session = Depends(get_db)):
    movie = crud.get_movie_by_id(db, movie_id)
    statistics = crud.get_statistics_for_movie(db, movie_id)
    return templates.TemplateResponse("movie_detail.html", {"request": request, "movie": movie, "statistics": statistics})

@app.get("/series/{series_id}")
def read_series(request: Request, series_id: int, db: Session = Depends(get_db)):
    series = crud.get_series_by_id(db, series_id)
    statistics = crud.get_statistics_for_series(db, series_id)
    return templates.TemplateResponse("series_detail.html", {"request": request, "series": series, "statistics": statistics})

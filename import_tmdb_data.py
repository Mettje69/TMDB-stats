import requests
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Film, Series, Statistics

# TMDb API configuration
API_KEY = '8834198b524b63a993e6d2cc4874493c'  # Replace with your actual API key
BASE_URL = 'https://api.themoviedb.org/3'

def fetch_movies_from_tmdb():
    endpoint = f'{BASE_URL}/movie/popular'
    params = {
        'api_key': API_KEY
    }
    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        return response.json().get('results', [])
    else:
        print(f"Failed to fetch movies from TMDb. Status code: {response.status_code}")
        return []

def fetch_movie_details(movie_id):
    endpoint = f'{BASE_URL}/movie/{movie_id}'
    params = {
        'api_key': API_KEY
    }
    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch movie details from TMDb. Status code: {response.status_code}")
        return {}

def fetch_series_from_tmdb():
    endpoint = f'{BASE_URL}/tv/popular'
    params = {
        'api_key': API_KEY
    }
    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        return response.json().get('results', [])
    else:
        print(f"Failed to fetch TV series from TMDb. Status code: {response.status_code}")
        return []

def fetch_series_details(series_id):
    endpoint = f'{BASE_URL}/tv/{series_id}'
    params = {
        'api_key': API_KEY
    }
    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch series details from TMDb. Status code: {response.status_code}")
        return {}

def import_movies_to_db():
    movies = fetch_movies_from_tmdb()
    db = SessionLocal()
    try:
        for movie in movies:
            movie_details = fetch_movie_details(movie.get('id'))
            genres = ' '.join([genre.get('name') for genre in movie_details.get('genres', [])])
            db_movie = Film(
                title=movie.get('title'),
                release_date=movie.get('release_date'),
                genre=genres
            )
            db.add(db_movie)
            db.commit()  # Commit to get the movie ID
            
            # Populate statistics
            db_stat = Statistics(
                film_id=db_movie.id,
                series_id=None,
                date=movie.get('release_date'),
                views=int(movie.get('popularity', 0) * 1000),
                likes=int(movie.get('vote_count', 0) * (movie.get('vote_average', 0) / 10)),
                dislikes=int(movie.get('vote_count', 0) * (1 - (movie.get('vote_average', 0) / 10)))
            )
            db.add(db_stat)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error importing movies to database: {str(e)}")
    finally:
        db.close()

def import_series_to_db():
    series = fetch_series_from_tmdb()
    db = SessionLocal()
    try:
        for tv_series in series:
            series_details = fetch_series_details(tv_series.get('id'))
            genres = ' '.join([genre.get('name') for genre in series_details.get('genres', [])])
            db_series = Series(
                title=tv_series.get('name'),
                release_date=tv_series.get('first_air_date'),
                genre=genres,
                seasons=series_details.get('number_of_seasons')
            )
            db.add(db_series)
            db.commit()  # Commit to get the series ID
            
            # Populate statistics
            db_stat = Statistics(
                film_id=None,
                series_id=db_series.id,
                date=tv_series.get('first_air_date'),
                views=int(tv_series.get('popularity', 0) * 1000),
                likes=int(tv_series.get('vote_count', 0) * (tv_series.get('vote_average', 0) / 10)),
                dislikes=int(tv_series.get('vote_count', 0) * (1 - (tv_series.get('vote_average', 0) / 10)))
            )
            db.add(db_stat)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error importing TV series to database: {str(e)}")
    finally:
        db.close()

if __name__ == '__main__':
    import_movies_to_db()
    import_series_to_db()

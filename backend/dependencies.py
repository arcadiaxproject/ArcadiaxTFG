from database import db
from repositories.videogame_repo import VideogameRepository
from repositories.film_repo import FilmRepository
from services.videogame_service import VideogameService
from services.film_service import FilmService

# Repositories
videogame_repo = VideogameRepository(db["videogames"])
film_repo = FilmRepository(db["films"])

# Services
videogame_service = VideogameService(videogame_repo)
film_service = FilmService(film_repo)


def get_videogame_service() -> VideogameService:
    return videogame_service


def get_film_service() -> FilmService:
    return film_service

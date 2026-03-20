from database import db
from config import settings
from repositories.videogame_repo import VideogameRepository
from repositories.film_repo import FilmRepository
from services.videogame_service import VideogameService
from services.film_service import FilmService
from services.playback_service import PlaybackService
from events.publisher import EventPublisher

# Repositories
videogame_repo = VideogameRepository(db["videogames"])
film_repo = FilmRepository(db["films"])

# Event publisher
event_publisher = EventPublisher(settings.REDIS_URL)

# Services
videogame_service = VideogameService(videogame_repo)
film_service = FilmService(film_repo)
playback_service = PlaybackService(videogame_repo, film_repo, event_publisher)


def get_videogame_service() -> VideogameService:
    return videogame_service


def get_film_service() -> FilmService:
    return film_service


def get_playback_service() -> PlaybackService:
    return playback_service

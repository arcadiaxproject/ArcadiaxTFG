from database import db
from repositories.videogame_repo import VideogameRepository
from services.videogame_service import VideogameService

# Repositories
videogame_repo = VideogameRepository(db["videogames"])

# Services
videogame_service = VideogameService(videogame_repo)


def get_videogame_service() -> VideogameService:
    return videogame_service

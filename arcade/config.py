from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    REDIS_URL: str = "redis://localhost:6379"
    RETROARCH_PATH: str = "/Applications/RetroArch.app/Contents/MacOS/RetroArch"
    PPSSPP_PATH: str = "/Applications/PPSSPP.app/Contents/MacOS/PPSSPP"
    ROMS_PATH: str = "~/roms"
    TRAILERS_PATH: str = "~/trailers"
    MEDIA_PLAYER: str = "mpv"   # mpv o vlc

    class Config:
        env_file = ".env"


settings = Settings()

import os
from dotenv import load_dotenv

load_dotenv()


def _normalise_db_url(url):
    """Render/Heroku hand out URLs starting with 'postgres://', but modern
    SQLAlchemy requires 'postgresql://'. This rewrites the prefix so the app
    doesn't crash on boot. This is the #1 cause of failed deployments."""
    if url and url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    return url


class Config:
    """Settings shared by all environments."""
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-key-change-in-production")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # reject uploads larger than 16 MB


class DevelopmentConfig(Config):
    """Used on your computer: a simple SQLite file, debug messages on."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"


class ProductionConfig(Config):
    """Used on Render: the real PostgreSQL database, debug off."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = _normalise_db_url(os.getenv("DATABASE_URL"))


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
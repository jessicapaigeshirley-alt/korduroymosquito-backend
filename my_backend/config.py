
import os


class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET = None
    SQLALCHEMY_DATABASE_URI = None


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = False

    JWT_SECRET = os.getenv("JWT_SECRET")
    SQLALCHEMY_DATABASE_URI = (
        os.getenv("DATABASE_URL") or "sqlite:///dev.db"
    )


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True

    JWT_SECRET = os.getenv("JWT_SECRET")
    SQLALCHEMY_DATABASE_URI = (
        os.getenv("DATABASE_URL") or "sqlite:///:memory:"
    )


class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False

    JWT_SECRET = os.getenv("JWT_SECRET")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")


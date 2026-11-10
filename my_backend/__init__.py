
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask

# Load environment variables before importing config classes
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

from .extensions import db, migrate
from .config import (
    DevelopmentConfig,
    TestingConfig,
    ProductionConfig,
)


def create_app(config_name):
    app = Flask(__name__)

    configs = {
        "development": DevelopmentConfig,
        "testing": TestingConfig,
        "production": ProductionConfig,
    }

    app.config.from_object(configs[config_name])

    db.init_app(app)
    migrate.init_app(app, db)

    from . import models

    from .listings import listings_bp
    app.register_blueprint(listings_bp)

    from .health import health_bp
    app.register_blueprint(health_bp)

    from .auth import auth_bp
    app.register_blueprint(auth_bp)
    
    return app



from flask import Flask
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

    from .listings import listings_bp
    app.register_blueprint(listings_bp)

    return app


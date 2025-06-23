from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)

    # only now do we create our tables, against whatever DATABASE_URI is active
    with app.app_context():
        db.create_all()

    from .routes import bp as users_bp  # assume you turn your routes into a Blueprint
    app.register_blueprint(users_bp)
    return app
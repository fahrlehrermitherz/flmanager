from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Extensions initialisieren
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Blueprints importieren
    from auth.routes import auth
    from main.routes import main

    # Blueprints registrieren
    app.register_blueprint(auth)
    app.register_blueprint(main)

    # Datenbank-Tables erstellen (nur beim Start)
    with app.app_context():
        db.create_all()

    return app

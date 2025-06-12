from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from models import db

# LoginManager vorbereiten
login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # Redirect wenn nicht eingeloggt
login_manager.login_message_category = 'info'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialisierung
    db.init_app(app)
    login_manager.init_app(app)

    # Blueprints importieren und registrieren
    from auth.routes import auth
    from main.routes import main

    app.register_blueprint(auth)
    app.register_blueprint(main)

    return app

from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

# Initialisiere DB und LoginManager
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialisiere Extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Blueprints importieren
    from auth.routes import auth as auth_blueprint
    from main.routes import main as main_blueprint
    from buero.routes import buero as buero_blueprint
    from schueler.routes import schueler_bp

    # Blueprints registrieren
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(buero_blueprint)
    app.register_blueprint(schueler_bp)

    # Auto-Tabellenerstellung
    with app.app_context():
        db.create_all()
        print("✅ Tabellen erstellt oder geprüft (Auto-Start).")

    # Root-Route für Sichtbarkeit
    @app.route('/')
    def index():
        return "✅ Der FLManager-Server läuft! Bitte /auth/login aufrufen."

    return app

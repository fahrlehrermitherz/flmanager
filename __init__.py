from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

# DB-Instanz global vorbereiten
db = SQLAlchemy()

# Login-Manager vorbereiten
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Extensions initialisieren
    db.init_app(app)
    login_manager.init_app(app)

    # Blueprints importieren und registrieren
    from auth.routes import auth
    from main.routes import main
    from schueler.routes import schueler_bp
    from buero.routes import buero

    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(schueler_bp)
    app.register_blueprint(buero)

    @app.route("/")
    def index():
        return "✅ App läuft! Öffne /auth/login im Browser."

    return app

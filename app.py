from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

# Initialisierungen
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Extensions initialisieren
    db.init_app(app)
    login_manager.init_app(app)

    # Blueprints importieren und registrieren
    from auth.routes import auth as auth_blueprint
    from main.routes import calendar_bp as main_blueprint  # Hier der geänderte Import
    from schueler.routes import schueler_bp as schueler_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(schueler_blueprint, url_prefix='/schueler')

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

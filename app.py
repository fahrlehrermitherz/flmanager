from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    from auth.routes import auth as auth_blueprint
    from main.routes import main as main_blueprint
    from schueler.routes import schueler_bp as schueler_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(schueler_blueprint)

    @app.route("/")
    def index():
        return "✅ App läuft ohne db.create_all() – Tabellen sind bereits vorhanden."

    return app

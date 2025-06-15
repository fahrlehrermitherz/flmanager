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

    # Tabellen bei App-Start erstellen
    def create_tables():
        with app.app_context():
            db.create_all()
            print("✅ Tabellen wurden erstellt oder sind bereits vorhanden.")

    app.before_first_request(create_tables)

    @app.route("/")
    def index():
        return "✅ App läuft! Öffne /auth/login im Browser."

    return app

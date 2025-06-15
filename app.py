from flask import Flask
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
    from schueler.routes import schueler_bp as schueler_blueprint

    # Blueprints registrieren
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(buero_blueprint)
    app.register_blueprint(schueler_blueprint)

    # Optional: Root-Redirect definieren
    @app.route('/')
    def index():
        from flask import redirect, url_for
        return redirect(url_for('auth.login'))

    return app

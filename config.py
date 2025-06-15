import os

class Config:
    # Sicherheitsschlüssel für Sessions, CSRF etc.
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret"

    # Datenbank-URL: Railway DATABASE_URL oder lokale SQLite als Fallback
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///local.db"

    # SQLAlchemy-Tracking deaktivieren (spart Ressourcen)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Debug-Mode optional steuerbar
    DEBUG = os.environ.get("FLASK_DEBUG", "0") == "1"

    # Optionale SSL-Engine-Optionen (für Railway oder andere DBs mit SSL-Zwang)
    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {
            "sslmode": "require"
        }
    }

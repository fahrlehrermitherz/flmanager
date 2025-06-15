import os

class Config:
    # Sicherheitsschlüssel für Sessions, CSRF etc.
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret"

    # Datenbank: Railway URL oder lokale SQLite-DB als Fallback
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///local.db"

    # SQLAlchemy Tracking deaktivieren (spart Ressourcen)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Debug-Mode (optional steuerbar über Umgebungsvariable FLASK_DEBUG=1)
    DEBUG = os.environ.get("FLASK_DEBUG", "0") == "1"

import os

class Config:
    # Sicherheitsschlüssel für Sessions, CSRF etc.
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret"

    # Datenbank: Railway > Lokal-Fallback
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///local.db"

    # Optional: Track-Mod deaktivieren
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Optional (nur wenn du Debug-Mode explizit steuern willst):
    DEBUG = os.environ.get("FLASK_DEBUG") == "1"

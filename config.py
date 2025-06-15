import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")

    # Datenbank-URL: DATABASE_URL > PUBLIC_DATABASE_URL > Fallback SQLite
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL") or 
        os.environ.get("PUBLIC_DATABASE_URL") or 
        "sqlite:///local.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    if SQLALCHEMY_DATABASE_URI.startswith("postgresql"):
        SQLALCHEMY_ENGINE_OPTIONS = {
            "connect_args": {
                "sslmode": "require"
            }
        }
    else:
        SQLALCHEMY_ENGINE_OPTIONS = {}

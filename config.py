import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret"
    
    # Nimmt Public DB, falls vorhanden, ansonsten DATABASE_URL
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("PUBLIC_DATABASE_URL") or 
        os.environ.get("DATABASE_URL") or 
        "sqlite:///local.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # SSL für Railway-Postgres
    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {
            "sslmode": "require"
        }
    }

import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")
    
    # Datenbank-URL: Public URL > DATABASE_URL > Fallback SQLite
 SQLALCHEMY_DATABASE_URI = (
    os.environ.get("postgresql://postgres:bydexzqxToeTpGxCynAynqxRRqBThlXd@nozomi.proxy.rlwy.net:37182/railway") or 
    os.environ.get("postgresql://postgres:bydexzqxToeTpGxCynAynqxRRqBThlXd@postgres.railway.internal:5432/railway") or 
    "sqlite:///local.db"
)

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Railway: SSL erzwingen, nur wenn Postgres verwendet wird
    if SQLALCHEMY_DATABASE_URI.startswith("postgresql"):
        SQLALCHEMY_ENGINE_OPTIONS = {
            "connect_args": {
                "sslmode": "require"
            }
        }
    else:
        SQLALCHEMY_ENGINE_OPTIONS = {}

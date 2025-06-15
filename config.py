import os
import logging

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or "sqlite:///local.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")

    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgresql"):
        SQLALCHEMY_ENGINE_OPTIONS = {
            "connect_args": {
                "sslmode": "require"
            }
        }
    else:
        SQLALCHEMY_ENGINE_OPTIONS = {}

# Logging für Debug-Zwecke
logging.basicConfig(level=logging.INFO)
logging.info(f"🔑 Using DB URI: {Config.SQLALCHEMY_DATABASE_URI}")

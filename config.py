import os
from dotenv import load_dotenv

# Carregar variáveis do ficheiro .env
load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    WTF_CSRF_SECRET_KEY = os.getenv("WTF_CSRF_SECRET_KEY") or SECRET_KEY
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///mealplanner.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"

    @classmethod
    def init_app(cls, app):
        secret_key = app.config.get("SECRET_KEY")
        if not secret_key or len(secret_key) < 32:
            raise RuntimeError("Set SECRET_KEY to a strong value of at least 32 characters")
        if os.getenv("RENDER") and not os.getenv("DATABASE_URL") and not app.testing:
            raise RuntimeError("DATABASE_URL is required on Render")

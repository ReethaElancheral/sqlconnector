import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "mysecret")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///product_catalog.db"  # local fallback
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

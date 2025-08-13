import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'product_secret_key')

    # MySQL connection using environment variables
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_HOST']}/{os.environ['DB_NAME']}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

import os

class Config:
    # Flask secret key (used for sessions and flash messages)
    SECRET_KEY = os.environ.get('SECRET_KEY', 'mysecret')

    # SQLAlchemy database URI
    # Use environment variable DATABASE_URL if set (for Render cloud)
    # Otherwise, fallback to local MySQL for testing
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'mysql+pymysql://root:1234@localhost/product_db'
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

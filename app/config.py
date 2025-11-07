# app/config.py

import os

class Config:
    # Database file path
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DB_PATH = os.path.join(BASE_DIR, '..', 'bms.sqlite')

    # SQLAlchemy database URI
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Other configs (later we’ll use for email, logging, etc.)
    DEBUG = True
    SECRET_KEY = "super-secret-key"

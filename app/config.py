import os


class Config:
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'super-sekret')
    WTF_CSRF_ENABLED = True

    CSV_ROWS = 10
    CSV_COLS = 3


class TestConfig:
    WTF_CSRF_ENABLED = False

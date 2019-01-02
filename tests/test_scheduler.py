import sqlite3

from app.db import get_db
from app.scheduler import fetch_data_from_yahoo


def test_fetch_data_from_yahoo(app):
    with app.app_context():
        fetch_data_from_yahoo()


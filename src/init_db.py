import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from config import Config
from models import db


def init_database():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")

        from models import Task

        print(f"Task table columns:")
        for column in Task.__table__.columns:
            print(f"  - {column.name}: {column.type}")


if __name__ == "__main__":
    init_database()

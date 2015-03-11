__author__ = 'alexanderventura'

from configuration.app import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

if __name__ == '__main__':
    db.create_all(app=app)

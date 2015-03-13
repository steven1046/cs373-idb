__author__ = 'alexanderventura'

from configuration.app import app
from configuration.config import config
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

if __name__ == '__main__':
    print(config["SQLALCHEMY_DATABASE_URI"])
    db.create_all(app=app)

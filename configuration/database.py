__author__ = 'alexanderventura'

from configuration.app import app, test_app
from configuration.config import config
from flask_sqlalchemy import SQLAlchemy


#defaults to prod db. run_models_test will change this to sqlalchemy object using sqlite db
db = SQLAlchemy(app)


def change_db(new_db):
    global db
    db = new_db


if __name__ == '__main__':
    print(config["SQLALCHEMY_DATABASE_URI"])
    db.create_all(app=app)

__author__ = 'alexanderventura'

from configuration.app import app, test_app
from configuration.config import config
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

# Todo. When running model tests you have to uncomment the line below. Need to see how I can change what database is
# Todo.     being used in Model class

# db = SQLAlchemy(test_app)

if __name__ == '__main__':
    print(config["SQLALCHEMY_DATABASE_URI"])
    db.create_all(app=app)

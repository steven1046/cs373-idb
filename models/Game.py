__author__ = 'alexanderventura'

from configuration.database import db
from sqlalchemy.dialects.postgresql import ARRAY


class Game(db.Model):
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    # genres = db.Column(ARRAY)
    release_date = db.Column(db.DateTime)
    description = db.Column(db.String(1000))
    # platforms
    # company
    # reviews

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return ''


def create_game(game):
    new_game = Game(game["name"], game["description"])
    db.session.add(new_game)
    db.session.commit()

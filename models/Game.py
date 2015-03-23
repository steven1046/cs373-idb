__author__ = 'alexanderventura'

from configuration.database import db
from sqlalchemy.dialects.postgresql import ARRAY


class Game(db.Model):
    __tablename__ = 'games'

    game_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    image = db.Column(db.String(80))
    original_release_date = db.Column(db.DateTime)
    deck = db.Column(db.Text)
    description = db.Column(db.Text)
    company_id = db.Column(db.Integer)

    def __init__(self, game_id, name, image, original_release_date, deck, description, company_id) :
        self.game_id = game_id
        self.name = name
        self.image = image
        self.original_release_date = original_release_date
        self.deck = deck
        self.description = description
        self.company_id = company_id

    def __repr__(self):
        return ''


def create_game(game):
    new_game = Game(game["game_id"], game["name"], game["image"], game["original_release_date"], game["deck"], game["description"], game["company_id"])
    db.session.add(new_game)
    db.session.commit()

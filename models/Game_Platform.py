__author__ = 'nicopelico'

from configuration.database import db
from utils.json_utils import to_json

class Game_Platform(db.Model):
    __tablename__ = "game_platforms"

    game_id = db.Column(db.Integer, db.ForeignKey("games.game_id"), primary_key=True)
    platform_id = db.Column(db.Integer, db.ForeignKey("platforms.platform_id"), primary_key=True)

    def __init__(self, game_id, platform_id):
        self.game_id = game_id
        self.platform_id = platform_id

    def __repr__(self):
        return ""


# Todo. Add a connect game_id to platform_id function. Inserts into game_genres table

#use to find the genre_id for the given game_id
@to_json
def find_by_id(game_id):
    return Game_Platform.query.filter_by(game_id=game_id).all()
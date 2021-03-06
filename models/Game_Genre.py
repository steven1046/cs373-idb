__author__ = 'nicopelico'

from configuration.database import db
from utils.json_utils import to_json

class Game_Genre(db.Model):
    __tablename__ = "game_genres"

    game_id = db.Column(db.Integer, db.ForeignKey("games.game_id"), primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey("genres.genre_id"), primary_key=True)

    def __init__(self, game_id, genre_id):
        self.game_id = game_id
        self.genre_id = genre_id

    def __repr__(self):
        return ""


# Create a connection between a game and a genre
def create_game_genre(game_genre):
    new_game_genre = Game_Genre(game_genre["game_id"], game_genre["genre_id"])
    db.session.add(new_game_genre)
    db.session.commit()


#use to find the genre_id for the given game_id
@to_json
def find_by_id(game_id):
    return Game_Genre.query.filter_by(game_id=game_id).all()



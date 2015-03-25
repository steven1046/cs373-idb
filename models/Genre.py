__author__ = 'nicopelico'

from configuration.database import db
from utils.json_utils import to_json


class Genre(db.Model):
    __tablename__ = "genres"

    genre_id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(80))

    def __init__(self, genre_id, genre):
        self.genre_id = genre_id
        self.genre = genre

    def __repr__(self):
        return ""


def create_genre(genre):
    new_genre = Genre(genre["genre_id"], genre["genre"])
    db.session.add(new_genre)
    db.session.commit()


@to_json
def find_by_id(genre_id):
    return Genre.query.filter_by(genre_id=genre_id).first()


def get_all_genres():
    # want a way to just do a select *. query.all() was giving me problems
    return Genre.query.with_entities(Genre.genre_id, Genre.genre).all()
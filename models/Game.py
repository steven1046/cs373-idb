__author__ = 'alexanderventura'

from configuration.database import db
from utils.json_utils import to_json
from models import Company


class Game(db.Model):
    __tablename__ = 'games'

    game_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    image = db.Column(db.String(80))
    original_release_date = db.Column(db.DateTime)
    deck = db.Column(db.Text)
    description = db.Column(db.Text)

    company_id = db.Column(db.Integer, db.ForeignKey("companies.company_id"))

    #Create a new game object using all the parameter atributes
    def __init__(self, game_id, name, image, original_release_date, deck, description, company_id):
        self.game_id = game_id
        self.name = name
        self.image = image
        self.original_release_date = original_release_date
        self.deck = deck
        self.description = description
        self.company_id = company_id

    #Returns a dictionary representation of the model
    def __repr__(self) :
        return str(self.to_dict())

    #Creates a dictionary of the model to_dict is called on
    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = str(getattr(self, column.name))
        return d


#Create a new game using the json sent in
def create_game(game):
    new_game = Game(game["game_id"], game["name"], game["image"], game["original_release_date"], game["deck"], game["description"], game["company_id"])
    db.session.add(new_game)
    db.session.commit()


#Returns a list of all the games in a json
@to_json
def find_all():
    return Game.query.all()


#Returns a json of the game model matching the game id passed in
@to_json
def find_by_id(game_id):
    return Game.query.filter_by(game_id=game_id).first()


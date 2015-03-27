
# from configuration.database import db
# from utils.json_utils import to_json
# from models import Company
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
db = SQLAlchemy(app)

def to_json(f):

    def handle_object(*args, **kwargs):
        sql_alchemy_model = f(*args, **kwargs)

        if isinstance(sql_alchemy_model, collections.Iterable):
            return serialize_collection(sql_alchemy_model)
        return serialize(sql_alchemy_model)

    return handle_object


db=0
to_json=0
Company=0


class Game(db.Model):
    __tablename__ = 'games'

    game_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    image = db.Column(db.String(80))
    original_release_date = db.Column(db.DateTime)
    deck = db.Column(db.Text)
    description = db.Column(db.Text)

    company_id = db.Column(db.Integer, db.ForeignKey("companies.company_id"))

    def __init__(self, game_id, name, image, original_release_date, deck, description, company_id):
        '''
        Create a new game object using all the parameter atributes
        '''
        self.game_id = game_id
        self.name = name
        self.image = image
        self.original_release_date = original_release_date
        self.deck = deck
        self.description = description
        self.company_id = company_id

    
    def __repr__(self) :
        '''
        Returns a dictionary representation of the model
        '''
        return str(self.to_dict())

    
    def to_dict(self):
        '''
        Creates a dictionary of the model to_dict is called on
        '''
        d = {}
        for column in self.__table__.columns:
            d[column.name] = str(getattr(self, column.name))
        return d

    
    def create_game(game):
        '''
        Create a new game using the json sent in
        '''
        new_game = Game(game["game_id"], game["name"], game["image"], game["original_release_date"], game["deck"], game["description"], game["company_id"])
        db.session.add(new_game)
        db.session.commit()

    
    @to_json
    def find_all():
        '''
        Returns a list of all the games in a json
        '''
        return Game.query.all()

    
    @to_json
    def find_by_id(game_id):
        '''
        Returns a json of the game model matching the game id passed in
        '''
        return Game.query.filter_by(game_id=game_id).first()

class Company(db.Model) :
    __tablename__ = "companies"

    company_id = db.Column("company_id", db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    deck = db.Column(db.Text)
    description = db.Column(db.Text)
    image = db.Column(db.String(80))
    address = db.Column(db.String(80))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    country = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    date_founded = db.Column(db.DateTime)
    website = db.Column(db.String(80))

    def __init__(self, company_id, name, deck, description, image, address, city, state, country, phone, date_founded,
                 website, test=False) :

        self.company_id = company_id
        self.name = name
        self.deck = deck
        self.description = description
        self.image = image
        self.address = address
        self.city = city
        self.state = state
        self.country = country
        self.phone = phone
        self.date_founded = date_founded
        self.website = website

    
    def __repr__(self) :
        '''
        prints out the dictionary as a string
        '''
        return str(self.to_dict())

    
    def to_dict(self):
        '''
        creates a dictionary representing the model for making a json
        '''
        d = {}
        for column in self.__table__.columns:
            d[column.name] = str(getattr(self, column.name))
        return d

    
    def create_company(company) :
        '''
        Create a new company using the data sent in as a json
        '''
        new_company = Company(company["company_id"], company["name"], company["deck"], company["description"],
                            company["image"], company["address"], company["city"], company["state"], company["country"], 
                            company["phone"], company["date_founded"], company["website"])
        db.session.add(new_company)
        db.session.commit()

    
    @to_json
    def find_by_id(company_id):
        '''
        Returns a json of the company that matches the company id
        '''
        return Company.query.filter_by(company_id=company_id).first()

    
    @to_json
    def find_all_companies():
        '''
        Returns a json of a dictionary for each company
        '''
        return Company.query.all()

    # @to_json
    # def get_company_games(company_id):
    #     return Company.query.join(Game, Game.c.)


class Game_Genre(db.Model):

    __tablename__ = "game_genres"

    game_id = db.Column(db.Integer, db.ForeignKey("games.game_id"), primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey("genres.genre_id"), primary_key=True)

    def __init__(self, game_id, genre_id):
        self.game_id = game_id
        self.genre_id = genre_id

    def __repr__(self):
        return ""



def create_game_genre(game_genre):
    '''
    Create a connection between a game and a genre
    '''
    new_game_genre = Game_Genre(game_genre["game_id"], game_genre["genre_id"])
    db.session.add(new_game_genre)
    db.session.commit()



@to_json
def find_by_id(game_id):
    '''
    use to find the genre_id for the given game_id
    '''
    return Game_Genre.query.filter_by(game_id=game_id).all()


class Genre(db.Model):
    __tablename__ = "genres"

    genre_id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(80))

    
    def __init__(self, genre_id, genre):
        '''
        Create a new genre object
        Genre constructor
        '''
        self.genre_id = genre_id
        self.genre = genre

    
    def __repr__(self):
        '''
        Return a string representation of the Genre
        '''
        return ""

    
    def create_genre(genre):
        '''
        Create a new genre object and add it to the database and commit it
        '''
        new_genre = Genre(genre["genre_id"], genre["genre"])
        db.session.add(new_genre)
        db.session.commit()

    
    @to_json
    def find_by_id(genre_id):
        '''
        Returns a json representation of the genre matching the genre_id
        '''
        return Genre.query.filter_by(genre_id=genre_id).first()

    
    def get_all_genres():
        '''
        Returns a list of all of the genres
        '''
        # want a way to just do a select *. query.all() was giving me problems
        return Genre.query.with_entities(Genre.genre_id, Genre.genre).all()

class Platform(db.Model):
    __tablename__ = "platforms"

    platform_id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(80))

    
    def __init__(self, platform_id, platform):
        ''' 
        Platform constructor
        '''
        self.platform_id = platform_id
        self.platform = platform

    
    def __repr__(self):
        '''
        Returns a representation of the platform
        '''
        return ""

    
    def create_platform(platform):
        '''
        Create a new platform object and commit it
        '''
        new_platform = Platform(platform["genre_id"], platform["genre"])
        db.session.add(new_platform)
        db.session.commit()

    
    @to_json
    def find_by_id(platform_id):
        '''
        Returns a json of the platform matching the platform id
        '''
        return Platform.query.filter_by(platform_id=platform_id).first()

    
    def get_all_platforms():
        '''
        Return a json of each platform in their own dictionary 
        '''
        # want a way to just do a select *. query.all() was giving me problems
        return Platform.query.with_entities(Platform.platform_id, Platform.platform).all()




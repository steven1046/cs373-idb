__author__ = 'alexanderventura'

from configuration.database import db
from utils.json_utils import to_json


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

    #prints out the dictionary as a string
    def __repr__(self) :
        return str(self.to_dict())

    #creates a dictionary representing the model for making a json
    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = str(getattr(self, column.name))
        return d

#Create a new company using the data sent in as a json
def create_company(company) :
    new_company = Company(company["company_id"], company["name"], company["deck"], company["description"],
                        company["image"], company["address"], company["city"], company["state"], company["country"],
                        company["phone"], company["date_founded"], company["website"])
    db.session.add(new_company)
    db.session.commit()


#Returns a json of the company that matches the company id
@to_json
def find_by_id(company_id):
    return Company.query.filter_by(company_id=company_id).first()


#Returns a json of a dictionary for each company
@to_json
def find_all_companies():
    return Company.query.all()

# @to_json
# def get_company_games(company_id):
#     return Company.query.join(Game, Game.c.)



__author__ = 'alexanderventura'

from configuration.database import db
from sqlalchemy.dialects.postgresql import ARRAY

class Company(db.Model) :
    __tablename__ = "companies"

    company_id = db.Column(db.Integer, primarykey=True)
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

    def __init__(self, company_id, name, deck, description, image, address, city, state, country, phone, date_founded, website) :
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
    	return ''

def create_company(company) :
	new_company = Company(company["company_id"], company["name"], company["deck"], company["description"],
						company["image"], company["address"], company["city"], company["state"], company["country"], 
						company["phone"], company["date_founded"], company["website"])
	db.session.add(new_company)
	db.session.commit()




__author__ = 'nicopelico'

from configuration.app import test_app
from models import Game, Company
from configuration.database import db_test
from unittest import main, TestCase
from datetime import datetime
from flask import request
from flask import session
import sqlite3


class TestModels(TestCase):

    test_company = (100, "test_company", "a short summary", "a longer description", "fake_url", "101 abc lane",
                    "test_city", "test_state", "test_country", "555-555-5555", "1-1-2000", "company url")
    test_game = (1, "test", "fake_url", "1-10-2010", "a short summary", "a longer description", 100)

    def test_company_model_creation_1(self):
        expected = {"company_id": "100", "name": "test_company", "deck": "a short summary",
                    "description": "a longer description", "image": "fake_url", "address": "101 abc lane",
                    "city": "test_city", "state": "test_state", "country": "test_country", "phone": "555-555-5555",
                    "date_founded": "1-1-2000", "website": "company url"}
        c = Company.Company(*self.test_company)
        d = c.to_dict()
        for k in expected:
            assert(d[k] == expected[k])

    def test_company_model_creation_2(self):
        expected = {"company_id": "100", "name": "test_company", "deck": "a short summary",
                    "description": "a longer description", "image": "fake_url", "address": "101 abc lane",
                    "city": "test_city", "state": "test_state", "country": "test_country", "phone": "555-555-5555",
                    "date_founded": "1-1-2000", "website": "company url"}
        test_company1 = (100, "test_company", "a short summary", "a longer description", "fake_url", "101 abc lane",
                    "test_city", "test_state", "test_country", "555-555-5555", datetime.today(), "company url")
        c = Company.Company(*test_company1)
        db_test.session.add(c)

        db_test.session.commit()
        db_test.session.add(c)

        # session.add(c)
        # session.commit()
        # session.add(c)
        result = Company.find_by_id(100)
        d = c.to_dict()
        for k in expected:
            assert(d[k] == expected[k])

    # def test_company_model_creation_3(self):
    #     test = (200, "test_company", "a short summary", "a longer description", "fake_url", "101 abc lane",
    #                 "test_city", "test_state", "test_country", "555-555-5555", "1-1-2000", "company url")
    #     a = Company.Company(*test)
    #     b = Company.Company(*test)
    #     session.add(a)
    #     db.session.add(b)
    #     # try:
    #     #     db.session.add(b)
    #     #     assert(False)
    #     # except Exception as e:
    #     #     print(str(e))
    #     #     assert(True)







# def model_test():
#     # test_company = Company(company_id=100, name="test_company", deck="a short summary",
#     #                        description="a longer description", image="fake_url", address="101 abc lane",
#     #                        city="test_city", state="test_state", country="test_country", phone="555-555-5555",
#     #                        date_founded="1-1-2000", website="company_url")
#     # test_game = Game(game_id="1", name="test", image="fake_url", original_release_date="1-10-2010",
#     #                  deck="short summary", description="longer description", company_id="100")
#     db.session.add(test_company)
#     db.session.add(test_game)
#     print("here")
#     result = find_by_id(1)
#     print(type(result))


if __name__ == "__main__":
    # conn = sqlite3.connect(":memory:")
    # c = conn.cursor()
    # c.execute('''CREATE TABLE companies (
    #               company_id INTEGER NOT NULL,
    #               name CHARACTER VARYING,
    #               deck TEXT,
    #               description TEXT,
    #               image CHARACTER VARYING,
    #               address CHARACTER VARYING,
    #               city CHARACTER VARYING,
    #               state CHARACTER VARYING,
    #               country CHARACTER VARYING,
    #               phone CHARACTER VARYING,
    #               date_founded DATE,
    #               website CHARACTER VARYING,
    #               CONSTRAINT pk_companies PRIMARY KEY (company_id)
    #               )''')
    #
    # conn.commit()

    db_test.create_all()
    db_test.engine.execute('''CREATE TABLE companies (
                  company_id INTEGER NOT NULL,
                  name CHARACTER VARYING,
                  deck TEXT,
                  description TEXT,
                  image CHARACTER VARYING,
                  address CHARACTER VARYING,
                  city CHARACTER VARYING,
                  state CHARACTER VARYING,
                  country CHARACTER VARYING,
                  phone CHARACTER VARYING,
                  date_founded DATE,
                  website CHARACTER VARYING,
                  CONSTRAINT pk_companies PRIMARY KEY (company_id)
                  )''')

    conn = db_test.engine.connect()
    result = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")

    for row in result:
        print(row)

    with test_app.test_request_context("/"):
        test_app.open_session(request)
        main()
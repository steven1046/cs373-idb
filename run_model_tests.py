__author__ = 'nicopelico'

from configuration.app import test_app
from models import Game, Company, Genre
from configuration.database import db
from unittest import main, TestCase
from datetime import datetime, date
from flask import request
from flask import session
import sqlite3


class TestModels(TestCase):

    test_company = [100, "test_company", "a short summary", "a longer description", "fake_url", "101 abc lane",
                    "test_city", "test_state", "test_country", "555-555-5555", date.min, "company url"]
    test_company_dict = {"company_id": "100", "name": "test_company", "deck": "a short summary",
                         "description": "a longer description", "image": "fake_url", "address": "101 abc lane",
                         "city": "test_city", "state": "test_state", "country": "test_country", "phone": "555-555-5555",
                         "date_founded": date.min, "website": "company url"}
    test_game = [1, "test", "fake_url", date.min, "a short summary", "a longer description", 100]

    def test_company_model_creation_1(self):
        c = Company.Company(*self.test_company)
        d = c.to_dict()
        for k in TestModels.test_company_dict:
            if k == "date_founded":
                assert(str(d[k]).split()[0] == str(TestModels.test_company_dict[k]))
            else:
                assert(d[k] == TestModels.test_company_dict[k])

    # Make sure new Company can be queried for
    def test_company_model_creation_2(self):
        c = Company.Company(*TestModels.test_company)
        db.session.add(c)
        db.session.commit()
        result = Company.find_by_id(100)
        # company was found
        assert(len(result) > 0)

    # Two companies should be returned for the query all()
    def test_company_model_creation_3(self):
        # one record in Companies so far
        TestModels.test_company[0] = 200
        d = Company.Company(*TestModels.test_company)
        db.session.add(d)
        db.session.commit()
        result = Company.Company.query.all()
        # two records to Company so far
        assert(len(result) == 2)

    # Trying to add Company that already exists
    def test_company_model_creation_4(self):
        d = Company.Company(*TestModels.test_company)
        try:
            db.session.add(d)
            db.session.commit()
            assert(False)
        except:
            db.session.rollback()

    # Make sure game can be queried for once created
    def test_game_model_creation_1(self):
        g = Game.Game(*TestModels.test_game)
        db.session.add(g)
        db.session.commit()
        result = Game.Game.query.all()
        assert(len(result) == 1)

    # Make sure there are now two games.
    def test_game_model_creation_2(self):
        # one game so far
        TestModels.test_game[0] = 2
        g = Game.Game(*TestModels.test_game)
        db.session.add(g)
        db.session.commit()
        result = Game.Game.query.all()
        assert(len(result) == 2)

    # make sure games with duplicate ids can't be commited
    def test_game_model_creation_3(self):
        #two games so far
        g = Game.Game(*TestModels.test_game)
        try:
            db.session.add(g)
            db.session.commit()
            assert(False)
        except:
            db.session.rollback()


    # make sure game can't be added when the company doesnt exist
    def test_game_model_creation_4(self):
        # changing company_id to one that doesn't exist yet
        TestModels.test_game[6] = 500
        TestModels.test_game[0] = 3
        g = Game.Game(*TestModels.test_game)
        db.session.add(g)
        try:
            db.session.commit()
            assert(False)
        except:
            db.session.rollback()

    # creating genre
    def test_genre_model_creation_1(self):
        g = Genre.Genre(1, "test genre")
        db.session.add(g)
        result = Genre.Genre.query.all()
        assert(len(result) == 1)

    #creating another genre
    def test_genre_model_creation_2(self):
        g = Genre.Genre(2, "test genre 2")
        db.session.add(g)
        result = Genre.Genre.query.all()
        assert(len(result) == 2)

    #don't allow genre with duplicate id
    def test_genre_model_creation_3(self):
        g = Genre.Genre(2, "test genre 2")
        db.session.add(g)
        try:
            db.session.commit()
            assert(False)
        except:
            db.session.rollback()











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



if __name__ == "__main__":

    db.create_all()

    # !!!!! Apparently sqlite doesn't enforce foreign key constraints by default !!!!
    db.engine.execute("PRAGMA foreign_keys = ON")

    with test_app.test_request_context("/"):
        main()
        db.drop_all()
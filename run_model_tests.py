__author__ = 'nicopelico'

from configuration.app import test_app
from models import Game, Company, Genre, Platform, Game_Genre, Game_Platform
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

    def setUp(self):
        db.create_all()


    def tearDown(self):
        db.session.remove()
        db.drop_all()

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
        # first record
        c = Company.Company(*TestModels.test_company)
        db.session.add(c)
        # second record
        new_comp = list(TestModels.test_company)
        new_comp[0] = 200
        d = Company.Company(*new_comp)
        db.session.add(d)
        db.session.commit()
        result = Company.Company.query.all()
        # two records to Company so far
        assert(len(result) == 2)

    # Trying to add Company that already exists
    def test_company_model_creation_4(self):
        result = Company.Company.query.all()
        print(result)
        d = Company.Company(*TestModels.test_company)
        db.session.add(d)
        db.session.commit()
        e = Company.Company(*TestModels.test_company)
        try:
            db.session.add(e)
            db.session.commit()
            assert(False)
        except Exception as e:
            db.session.rollback()


    # Make sure game can be queried for once created
    def test_game_model_creation_1(self):
        c = Company.Company(*TestModels.test_company)
        db.session.add(c)
        db.session.commit()
        g = Game.Game(*TestModels.test_game)
        db.session.add(g)
        db.session.commit()
        result = Game.Game.query.all()
        assert(len(result) == 1)

    # Make sure there are now two games.
    def test_game_model_creation_2(self):
        # add company for fk constraint
        c = Company.Company(*TestModels.test_company)
        db.session.add(c)
        db.session.commit()
        g = Game.Game(*TestModels.test_game)
        db.session.add(g)
        db.session.commit()
        new_game = list(TestModels.test_game)
        # increment id
        new_game[0] = new_game[0] + 1
        e = Game.Game(*new_game)
        db.session.add(e)
        db.session.commit()
        result = Game.Game.query.all()
        assert(len(result) == 2)


    # make sure games with duplicate ids can't be commited
    def test_game_model_creation_3(self):
        # add company for fk constraint
        c = Company.Company(*TestModels.test_company)
        db.session.add(c)
        db.session.commit()
        g = Game.Game(*TestModels.test_game)
        db.session.add(g)
        db.session.commit()
        e = Game.Game(*TestModels.test_game)
        try:
            db.session.add(e)
            db.session.commit()
            assert(False)
        except Exception as e:
            db.session.rollback()


    # make sure game can't be added when the company doesnt exist
    def test_game_model_creation_4(self):
        # changing company_id to one that doesn't exist yet
        new_game = list(TestModels.test_game)
        # increment id
        new_game[6] = new_game[6] + 1
        g = Game.Game(*new_game)
        db.session.add(g)
        try:
            db.session.commit()
            assert(False)
        except Exception as e:
            db.session.rollback()

    # creating genre
    def test_genre_model_creation_1(self):
        g = Genre.Genre(1, "test genre")
        db.session.add(g)
        db.session.commit()
        result = Genre.Genre.query.all()
        assert(len(result) == 1)

    #creating two genres
    def test_genre_model_creation_2(self):
        g = Genre.Genre(2, "test genre 2")
        db.session.add(g)
        db.session.commit()
        e = Genre.Genre(3, "test genre")
        db.session.add(e)
        db.session.commit()
        result = Genre.Genre.query.all()
        assert(len(result) == 2)


    #don't allow genre with duplicate id
    def test_genre_model_creation_3(self):
        g = Genre.Genre(2, "test genre 3")
        db.session.add(g)
        db.session.commit()
        e = Genre.Genre(2, "duplicate")
        try:
            db.session.add(e)
            db.session.commit()
            assert(False)
        except Exception as e:
            db.session.rollback()


    # creating platform
    def test_platform_model_creation_1(self):
        g = Platform.Platform(1, "test platform")
        db.session.add(g)
        db.session.commit()
        result = Platform.Platform.query.all()
        assert(len(result) == 1)

    #creating two platforms
    def test_platform_model_creation_2(self):
        g = Platform.Platform(2, "test platform 2")
        db.session.add(g)
        db.session.commit()
        e = Platform.Platform(3, "test platform 3")
        db.session.add(e)
        db.session.commit()
        result = Platform.Platform.query.all()
        assert(len(result) == 2)


    #don't allow platform with duplicate id
    def test_platform_model_creation_3(self):
        g = Platform.Platform(2, "test platform 3")
        db.session.add(g)
        db.session.commit()
        e = Platform.Platform(2, "duplicate")
        try:
            db.session.add(e)
            db.session.commit()
            assert(False)
        except Exception as e:
            db.session.rollback()

    # connect a game to a genre (create new game_genre)
    def test_game_genre_model_creation_1(self):
        c = Company.Company(*TestModels.test_company)
        db.session.add(c)
        db.session.commit()
        new_game = Game.Game(*TestModels.test_game)
        db.session.add(new_game)
        db.session.commit()
        new_genre = Genre.Genre(1, "test genre")
        db.session.add(new_genre)
        db.session.commit()
        new_game_genre = Game_Genre.Game_Genre(1, 1)
        db.session.add(new_game_genre)
        db.session.commit()

    # dont allow creation. game doesn't exist
    def test_game_genre_model_creation_2(self):
        c = Company.Company(*TestModels.test_company)
        db.session.add(c)
        db.session.commit()
        new_genre = Genre.Genre(1, "test genre")
        db.session.add(new_genre)
        db.session.commit()
        new_game_genre = Game_Genre.Game_Genre(1, 1)
        try:
            db.session.add(new_game_genre)
            db.session.commit()
            assert(False)
        except Exception as e:
            db.session.rollback()

    #dont allow creation. Genre won't exist
    def test_game_genre_model_creation_3(self):
        c = Company.Company(*TestModels.test_company)
        db.session.add(c)
        db.session.commit()
        new_game = Game.Game(*TestModels.test_game)
        db.session.add(new_game)
        db.session.commit()
        new_game_genre = Game_Genre.Game_Genre(1, 1)
        try:
            db.session.add(new_game_genre)
            db.session.commit()
        except Exception as e:
            db.session.rollback()


    # connect a game to a genre (create new game_genre)
    def test_game_platform_model_creation_1(self):
        c = Company.Company(*TestModels.test_company)
        db.session.add(c)
        db.session.commit()
        new_game = Game.Game(*TestModels.test_game)
        db.session.add(new_game)
        db.session.commit()
        new_platform = Platform.Platform(1, "test platform")
        db.session.add(new_platform)
        db.session.commit()
        new_game_platform = Game_Platform.Game_Platform(1, 1)
        db.session.add(new_game_platform)
        db.session.commit()

    # dont allow creation. game doesn't exist
    def test_game_platform_model_creation_2(self):
        c = Company.Company(*TestModels.test_company)
        db.session.add(c)
        db.session.commit()
        new_platform = Platform.Platform(1, "test platform")
        db.session.add(new_platform)
        db.session.commit()
        new_game_platform = Game_Platform.Game_Platform(1, 1)
        try:
            db.session.add(new_game_platform)
            db.session.commit()
            assert(False)
        except Exception as e:
            db.session.rollback()

    #dont allow creation. Platform won't exist
    def test_game_platform_model_creation_3(self):
        c = Company.Company(*TestModels.test_company)
        db.session.add(c)
        db.session.commit()
        new_game = Game.Game(*TestModels.test_game)
        db.session.add(new_game)
        db.session.commit()
        new_game_platform = Game_Platform.Game_Platform(1, 1)
        try:
            db.session.add(new_game_platform)
            db.session.commit()
        except Exception as e:
            db.session.rollback()


if __name__ == "__main__":

    # !!!!! Apparently sqlite doesn't enforce foreign key constraints by default !!!!
    db.engine.execute("PRAGMA foreign_keys = ON")

    with test_app.test_request_context("/"):
        main()
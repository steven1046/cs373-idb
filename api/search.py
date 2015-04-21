__author__ = 'nicopelico'


from flask import Blueprint, request, jsonify
from sqlalchemy.sql.expression import or_, and_
from stop_words import get_stop_words
from models import Job, Company
from models.Game import Game

searches = Blueprint("searches", __name__)

@searches.route("/", methods=["GET"])
def search():
    try:
        if "s" in request.args:
            search = request.args["s"].rsplit(" ")
            for x in search:
                print(x)
            print(request.args["s"])

            a = search_games_whole_match(request.args["s"])

            terms = request.args["s"].rsplit(" ")

            if len(terms) > 1:
                b = search_games_contains_all(request.args["s"])
                a["results"] += b["results"]
            search_companies(request.args["s"])
            search_jobs(request.args["s"])

            print(len(a["results"]))

        return jsonify(a), 200

    except Exception as e:
        return jsonify(error=str(e)), 400


def search_games_whole_match(search_string):

    # AND results whole match
    print("searching for games for '" + search_string + "'")
    r1 = Game.query.filter(Game.name.ilike("%" + search_string + "%")).with_entities(Game.name, Game.game_id).all()
    r2 = Game.query.filter(Game.deck.ilike("%" + search_string + "%")).with_entities(Game.name, Game.game_id).all()
    r3 = Game.query.filter(Game.description.ilike("%" + search_string + "%")).with_entities(Game.name, Game.game_id).all()
    print(len(r1))
    print(len(r2))
    print(len(r3))


    result = {}
    result["results"] = []

    # name
    for game in r1:
        d = {"name": game[0], "game_id": game[1], "context": "whole match. name context", "type": "games"}
        result["results"].append(d)

    # deck
    for game in r2:
        d = {"name": game[0], "game_id": game[1], "context": "whole match. deck context", "type": "games"}
        result["results"].append(d)

    # description
    for game in r3:
        d = {"name": game[0], "game_id": game[1], "context": "whole match. description context", "type": "games"}
        result["results"].append(d)

    return result


def search_games_contains_all(search_string):
    # AND results. (only if multiple terms)

    result = {}
    result["results"] = []

    stop_words = get_stop_words("en")
    # print(stop_words)

    all_terms = request.args["s"].rsplit(" ")
    # print(all_terms)

    terms = [x for x in all_terms if x not in stop_words]

    print(terms)

    conditions1 = []
    conditions2 = []
    conditions3 = []
    print(request.args["s"])
    print(terms)

    for term in terms:
        conditions1.append(Game.name.like(term))
        conditions2.append(Game.deck.like(term))
        conditions3.append(Game.description.like(term))

    condition = or_(*conditions1)
    print(str(condition))

    r1 = Game.query.filter(and_(* [Game.name.ilike("%" + x + "%") for x in terms])).with_entities(Game.name, Game.game_id).all()
    r2 = Game.query.filter(and_(* [Game.deck.ilike("%" + x + "%") for x in terms])).with_entities(Game.name, Game.game_id).all()
    r3 = Game.query.filter(and_(* [Game.description.ilike("%" + x + "%") for x in terms])).with_entities(Game.name, Game.game_id).all()

    print(len(r1))
    print(len(r2))
    print(len(r3))

    # name
    for game in r1:
        d = {"name": game[0], "game_id": game[1], "context": "partial match. name context"}
        result["results"].append(d)

    # deck
    for game in r2:
        d = {"name": game[0], "game_id": game[1], "context": "partial match. deck context"}
        result["results"].append(d)

    # description
    for game in r3:
        d = {"name": game[0], "game_id": game[1], "context": "partial match. description context"}
        result["results"].append(d)

    return result

def search_games_contains_or(search_string):
    pass

def search_companies(search_string):
    print("searching for companies for '" + search_string + "'")


def search_jobs(search_string):
    print("searching for jobs for '" + search_string + "'")


# pass this method the text to be searched and the terms we want. Return a context that shows where these terms show up
# in "text". '...sample sample terms[0] sample... ...sample sample terms[1] sample sample...' (something like this)
def get_context_whole_match(text, terms):
    pass

def get_context_contains_all(text, terms):
    pass
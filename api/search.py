__author__ = 'nicopelico'


from flask import Blueprint, request, jsonify
from sqlalchemy.sql.expression import or_, and_
from stop_words import get_stop_words
from models.Job import Job
from models.Game import Game
from models.Company import Company
from collections import OrderedDict
import re

searches = Blueprint("searches", __name__)

@searches.route("/", methods=["GET"])
def search():
    a = {"results": []}
    try:
        if "s" in request.args:
            if request.args["s"] != "":
                search = request.args["s"].rsplit(" ")
                for x in search:
                    print(x)
                print(request.args["s"])
                a = execute_search(request.args["s"])

                print(len(a["results"]))

        return jsonify(a), 200

    except Exception as e:
        return jsonify(error=str(e)), 400


def execute_search(search_string):
    # whole match queries

    #Todo: Need to change to OrderedDicts ???
    a = {"results": []}

    print("WHOLE MATCH")

    game_queries = OrderedDict([("name", Game.name.ilike("%" + request.args["s"] + "%")),
                                ("deck", Game.deck.ilike("%" + request.args["s"] + "%")),
                                ("description", Game.description.ilike("%" + request.args["s"] + "%"))])

    company_queries = OrderedDict([("name", Company.name.ilike("%" + request.args["s"] + "%")),
                                   ("deck", Company.deck.ilike("%" + request.args["s"] + "%")),
                                   ("description", Company.description.ilike("%" + request.args["s"] + "%"))])

    job_queries = OrderedDict([("job_title", Job.job_title.ilike("%" + request.args["s"] + "%")),
                               ("description", Job.description.ilike("%" + request.args["s"] + "%")),
                               ("location", Job.location.ilike("%" + request.args["s"] + "%")),
                               ("company_name", Job.company_name.ilike("%" + request.args["s"] + "%"))])

    print("SEARCHING GAMES")

    games = search_models(a, request.args["s"], Game, "games", "whole match", "AND", game_queries, Game.name, Game.game_id)

    print("SEARCHING COMPANIES")

    companies = search_models(a, request.args["s"], Company, "companies", "whole match", "AND", company_queries, Company.name,
                              Company.company_id)

    print("SEARCHING JOBS")

    jobs = search_models(a, request.args["s"], Job, "jobs", "whole match", "AND", job_queries, Job.job_title, Job.job_id)

    a["results"] = games["results"] + companies["results"] + jobs["results"]

    # contains AND

    stop_words = get_stop_words("en")
    # print(stop_words)

    all_terms = request.args["s"].rsplit(" ")
    # print(all_terms)

    terms = [x for x in all_terms if x not in stop_words]

    print("going...")
    print(terms)

    if len(terms) > 1:

        print("PARTIAL AND")

        games_queries_and = OrderedDict([("name", and_(* [Game.name.ilike("%" + x + "%") for x in terms])),
                                         ("deck", and_(* [Game.deck.ilike("%" + x + "%") for x in terms])),
                                         ("description", and_(* [Game.description.ilike("%" + x + "%") for x in terms]))])

        companies_queries_and = OrderedDict([("name", and_(* [Company.name.ilike("%" + x + "%") for x in terms])),
                                             ("deck", and_(* [Company.deck.ilike("%" + x + "%") for x in terms])),
                                             ("description", and_(* [Company.description.ilike("%" + x + "%") for x in terms]))])

        jobs_queries_and = OrderedDict([("job_title", and_(* [Job.job_title.ilike("%" + x + "%") for x in terms])),
                                        ("description", and_(* [Job.description.ilike("%" + x + "%") for x in terms])),
                                        ("location", and_(* [Job.location.ilike("%" + x + "%") for x in terms])),
                                        ("company_name", and_(* [Job.company_name.ilike("%" + x + "%") for x in terms]))])

        games_and = search_models(a, request.args["s"], Game, "games", "partial match AND", "AND", games_queries_and, Game.name,
                                  Game.game_id)

        companies_and = search_models(a, request.args["s"], Company, "companies", "partial match AND", "AND",
                                      companies_queries_and, Company.name, Company.company_id)

        jobs_and = search_models(a, request.args["s"], Job, "jobs", "partial match AND", "AND", jobs_queries_and, Job.job_title,
                                 Job.job_id)

        a["results"] += games_and["results"] + companies_and["results"] + jobs_and["results"]

        # contains OR

        print("PARTIAL OR")

        games_queries_or = OrderedDict([("name", or_(* [Game.name.ilike("%" + x + "%") for x in terms])),
                                        ("deck", or_(* [Game.deck.ilike("%" + x + "%") for x in terms])),
                                        ("description", or_(* [Game.description.ilike("%" + x + "%") for x in terms]))])

        companies_queries_or = OrderedDict([("name", or_(* [Company.name.ilike("%" + x + "%") for x in terms])),
                                            ("deck", or_(* [Company.deck.ilike("%" + x + "%") for x in terms])),
                                            ("description", or_(* [Company.description.ilike("%" + x + "%") for x in terms]))])

        jobs_queries_or = OrderedDict([("job_title", or_(* [Job.job_title.ilike("%" + x + "%") for x in terms])),
                                       ("description", or_(* [Job.description.ilike("%" + x + "%") for x in terms])),
                                       ("location", or_(* [Job.location.ilike("%" + x + "%") for x in terms])),
                                       ("company_name", or_(* [Job.company_name.ilike("%" + x + "%") for x in terms]))])

        games_or = search_models(a, request.args["s"], Game, "games", "partial match OR", "OR", games_queries_or, Game.name,
                                 Game.game_id)

        companies_or = search_models(a, request.args["s"], Company, "companies", "partial match OR", "OR", companies_queries_or,
                                     Company.name, Company.company_id)

        jobs_or = search_models(a, request.args["s"], Job, "jobs", "partial match OR", "OR",
                                jobs_queries_or, Job.job_title, Job.job_id)

        a["results"] += games_or["results"] + companies_or["results"] + jobs_or["results"]

    return a


# search_string, filter, entities
def search_models(temp_result, search_string, model, type, match_type, result_type, queries, *entities):


    result = {}
    result["results"] = []

    terms = search_string.rsplit(" ")

    for q in queries:
        r = model.query.filter(queries[q]).with_entities(getattr(model, q), *entities).all()
        print(len(r))

        # item[0] is the data that contains the search terms. Pass to context function to get a context

        for item in r:
            contains = False

            for obj in temp_result["results"]:
                if obj["id"] == item[2] and obj["type"] == type:
                    contains = True
                # print(str(obj["id"]) + " | " + obj["type"])
                # print(obj["id"] == item[2] and obj["type"] == type)
                # print(str(obj["id"]) + ", " + str(item[2]) + " | " + obj["type"] + ", " + type)

            if not contains:
                if match_type == "whole match":
                    context, num_matches = create_context(item[0], search_string, "whole match")
                else:
                    context, num_matches = create_context(item[0], terms, "other")
                print("HERE")
                # Todo: Change to case
                if match_type == "whole match":
                    if num_matches > 0:
                        # "context": match_type + " : " + q + " : " + context
                        d = {"name": item[1], "id": item[2], "context": context, "type": type, "result_type": result_type}
                        result["results"].append(d)
                else:
                    if match_type == "partial match AND":
                        if num_matches == len(terms):
                            d = {"name": item[1], "id": item[2], "context": context, "type": type, "result_type": result_type}
                            result["results"].append(d)
                    else:
                        if num_matches > 0:
                            d = {"name": item[1], "id": item[2], "context": context, "type": type, "result_type": result_type}
                            result["results"].append(d)

    print("returning")
    return result


def create_context(text, terms, match_type):
    print("inside create_context")
    print(terms)

    context_before = 20
    context_after = 20
    context = ""

    # remove html tags
    text = re.sub("<.*?>", " ", text)

    # used for matching when term appears at beginning or end
    text = " " + text + " "


    num_matches = 0

    if match_type == "whole match":
        match = re.search(".{0,10} " + terms + " .{0,10}", text, re.IGNORECASE)
        if match is not None:
                print("match: " + match.group(0))
                context += "..." + match.group(0)
                num_matches += 1
        else:
            if terms == text:
                context += "..." + terms
                num_matches += 1

    else:
        for term in terms:
            match = re.search(".{0,10} " + term + " .{0,10}", text, re.IGNORECASE)
            if match is not None:
                print("match: " + match.group(0))
                context += "..." + match.group(0)
                num_matches += 1

    context += "..."
    return context, num_matches



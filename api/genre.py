__author__ = 'nicopelico'

from flask import Blueprint, request, jsonify
from models import Genre

genres = Blueprint("genres", __name__)

@genres.route("/", methods=["POST"])
def create():
    try:
        Genre.create_genre(request.json)
        return jsonify(200)

    except Exception as e:
        return jsonify(error=str(e))


@genres.route("/<genre_id>", methods=["GET"])
def get(genre_id):
    try:
        genre = Genre.find_by_id(genre_id)
        return jsonify(genre), 200

    except Exception as e:
        return jsonify(error=str(e))


@genres.route("/", methods=["GET"])
def get_all():
    try:
        all_genres = Genre.get_all_genres()
        print(all_genres)
        return jsonify(all_genres), 200

    except Exception as e:
        return jsonify(error=str(e))


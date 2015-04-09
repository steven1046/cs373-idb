__author__ = 'alexanderventura'

from flask import Blueprint, request, jsonify
from models import Game

games = Blueprint('games', __name__)

@games.route('/', methods=['POST'])
def create():
    try:
        Game.create_game(request.json)
        game = Game.find_by_id(request.json["game_id"])
        return jsonify(game), 201

    except Exception as e:
        print(e)
        return jsonify(error="couldn't add game"), 400


@games.route('/<game_id>', methods=['GET'])
def get(game_id):
    try:
        game = Game.find_by_id(game_id)
        return jsonify(game), 200
    except Exception as e:
        return jsonify(error=str(e))


@games.route('/', methods=['GET'])
def get_all():
    try:
        games = Game.find_all()
        return jsonify(games=games), 200
    except Exception as e:
        return jsonify(error=str(e))

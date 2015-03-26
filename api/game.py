__author__ = 'alexanderventura'

from flask import Blueprint, request, jsonify
from models import Game

games = Blueprint('games', __name__)


@games.route('/', methods=['POST'])
def create():
    try:
        print(request.json)
        Game.create_game(request.json)
        return jsonify(200)

    except Exception as e:
        return jsonify(error=str(e))


@games.route('/<game_id>', methods=['GET'])
def get(game_id):
    try:
        print(game_id)
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

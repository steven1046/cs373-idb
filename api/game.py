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
        return jsonify(e)

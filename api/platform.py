__author__ = 'nicopelico'

from flask import Blueprint, request, jsonify
from models import Platform

platforms = Blueprint("platforms", __name__)

@platforms.route("/", methods=["POST"])
def create():
    try:
        Platform.create_platform(request.json)
        return jsonify(200)

    except Exception as e:
        return jsonify(error=str(e))


@platforms.route("/<platform_id>", methods=["GET"])
def get(platform_id):
    try:
        genre = Platform.find_by_id(platform_id)
        return jsonify(genre), 200

    except Exception as e:
        return jsonify(error=str(e))


@platforms.route("/", methods=["GET"])
def get_all():
    try:
        all_platforms = Platform.get_all_platforms()
        print(all_platforms)
        return jsonify(all_platforms), 200

    except Exception as e:
        return jsonify(error=str(e))

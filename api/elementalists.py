__author__ = 'ruben'


from flask import Blueprint, request, jsonify

elem_blueprint = Blueprint('elementalists', __name__)

@elem_blueprint.route('/', methods=["GET"])
def make_request():
    pass;
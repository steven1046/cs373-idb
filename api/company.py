__author__ = 'nicopelico'

from flask import Blueprint, request, jsonify
from models import Company

companies = Blueprint('companies', __name__)

@companies.route('/', methods=["POST"])
def create():
    try:
        Company.create_company(request.json)
        company = Company.find_by_id(request.json["company_id"])
        return jsonify(company), 201

    except Exception as e:
        return jsonify(error="couldn't add game"), 400


@companies.route('/<company_id>', methods=["GET"])
def get(company_id):
    try:
        company = Company.find_by_id(company_id)
        return jsonify(company), 200

    except Exception as e:
        return jsonify(error=str(e))


@companies.route('/', methods=["GET"])
def get_all():
    try:
        company = Company.find_all_companies()
        return jsonify(companies=company), 200

    except Exception as e:
        return jsonify(error=str(e))


__author__ = "Ruben Baeza"

__author__ = 'nicopelico'


from flask import Blueprint, request, jsonify
from models import Job


jobs = Blueprint('jobs', __name__)

@jobs.route('/', methods=['POST'])
def create():
	try:
        Job.create_job(request.json)
        job = Job.find_by_id(request.json["job_id"])
        return jsonify(job), 201

    except Exception as e:
        print(e)
        return jsonify(error="couldn't add job"), 400

@jobs.route('/<job_id>', methods=['GET'])
def get(job_id):
    try:
        job = Job.find_by_id(job_id)
        return jsonify(job), 200
    except Exception as e:
        return jsonify(error=str(e))


@jobs.route('/', methods=['GET'])
def get_all():
    try:
        jobs = Job.find_all()
        return jsonify(jobs=jobs), 200
    except Exception as e:
        return jsonify(error=str(e))

jobs = Blueprint("jobs", __name__)

@jobs.route("/", methods=["POST"])
def create():
    try:
        Job.create_job(request.json)
        job = Job.find_by_id(request.json["job_id"])
        return jsonify(job), 200

    except Exception as e:
        print(e)
        return jsonify(error="couldn't add job")


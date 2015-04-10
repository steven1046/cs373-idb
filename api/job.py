<<<<<<< HEAD

__author__ = "Ruben Baeza"

__author__ = 'nicopelico'

=======
__author__ = "Ruben Baeza"
>>>>>>> 04e0517b7b6c66be18a6fa0222ae915cf689e4a7

from flask import Blueprint, request, jsonify
from models import Job

<<<<<<< HEAD

=======
>>>>>>> 04e0517b7b6c66be18a6fa0222ae915cf689e4a7
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


<<<<<<< HEAD
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

=======
>>>>>>> 04e0517b7b6c66be18a6fa0222ae915cf689e4a7

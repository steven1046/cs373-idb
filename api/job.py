__author__ = 'nicopelico'

from flask import Blueprint, request, jsonify
from models import Job

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
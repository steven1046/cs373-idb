__author__ = 'nicopelico'


from flask import Blueprint, request, jsonify
import tests
import os
from io import StringIO
from subprocess import Popen, PIPE

test_blueprint = Blueprint('tests', __name__)

@test_blueprint.route('/', methods=["GET"])
def run_unittest():
    try:
        pipe = Popen("python3 tests.py -v", shell=True).wait()
        pipe2 = Popen("cat tests.out", shell=True, stdout=PIPE)
        text = pipe2.communicate()[0]
        s = text.decode()
        # s = s.replace("\n", "<br />")
        return jsonify(test_result=s), 200
    except Exception as e:
        return jsonify(error="error running unit tests"), 400

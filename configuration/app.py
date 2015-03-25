from flask_cors import CORS
from flask import Flask
from configuration.config import config, test_config

app = Flask(__name__)

app.config.update(config)
cors = CORS(app)

test_app = Flask(__name__)
test_app.config.from_object(test_config)


from flask import Flask
from configuration.config import config

app = Flask(__name__)

from api import game
app.register_blueprint(game.games, url_prefix=config['ROUTE_PREFIX'] + "games")

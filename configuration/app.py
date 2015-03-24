from flask import Flask
from configuration.config import config

app = Flask(__name__)

app.config.update(config)

from api import game, company, genre, platform
app.register_blueprint(game.games, url_prefix=config['ROUTE_PREFIX'] + "games")
app.register_blueprint(company.companies, url_prefix=config['ROUTE_PREFIX'] + "companies")
app.register_blueprint(genre.genres, url_prefix=config["ROUTE_PREFIX"] + "genres")
app.register_blueprint(platform.platforms, url_prefix=config["ROUTE_PREFIX"] + "platforms")
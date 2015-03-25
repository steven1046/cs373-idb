from flask import Flask
from configuration.config import config, test_config

app = Flask(__name__)

app.config.update(config)

test_app = Flask(__name__)
test_app.config.from_object(test_config)

from api import game, company, genre, platform
app.register_blueprint(game.games, url_prefix=config['ROUTE_PREFIX'] + "games")
app.register_blueprint(company.companies, url_prefix=config['ROUTE_PREFIX'] + "companies")
app.register_blueprint(genre.genres, url_prefix=config["ROUTE_PREFIX"] + "genres")
app.register_blueprint(platform.platforms, url_prefix=config["ROUTE_PREFIX"] + "platforms")



test_app.register_blueprint(game.games, url_prefix=config['ROUTE_PREFIX'] + "games")
test_app.register_blueprint(company.companies, url_prefix=config['ROUTE_PREFIX'] + "companies")
test_app.register_blueprint(genre.genres, url_prefix=config["ROUTE_PREFIX"] + "genres")
test_app.register_blueprint(platform.platforms, url_prefix=config["ROUTE_PREFIX"] + "platforms")
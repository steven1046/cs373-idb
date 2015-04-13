__author__ = 'alexanderventura'

from configuration.app import app
from configuration.config import config
from configuration.database import db
from api import job, game, company, genre, platform, test
from models import Game, Company, Game_Genre, Game_Platform, Job, Genre, Platform

app.register_blueprint(job.jobs, url_prefix=config["ROUTE_PREFIX"] + "jobs")
app.register_blueprint(game.games, url_prefix=config['ROUTE_PREFIX'] + "games")
app.register_blueprint(company.companies, url_prefix=config['ROUTE_PREFIX'] + "companies")
app.register_blueprint(genre.genres, url_prefix=config["ROUTE_PREFIX"] + "genres")
app.register_blueprint(platform.platforms, url_prefix=config["ROUTE_PREFIX"] + "platforms")
# app.register_blueprint(job.jobs, url_prefix=config["ROUTE_PREFIX"] + "jobs")
app.register_blueprint(test.test_blueprint, url_prefix=config["ROUTE_PREFIX"] + "tests")


if __name__ == '__main__':
    print('Routing Table')
    print(app.url_map)
    app.run(host=config["HOST"], port=config["PORT"], use_reloader=False, debug=False)
    # app.run(use_reloader=False)


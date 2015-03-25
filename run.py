__author__ = 'alexanderventura'

from configuration.app import app
from configuration.config import config
from api import game, company, genre, platform

app.register_blueprint(game.games, url_prefix=config['ROUTE_PREFIX'] + "games")
app.register_blueprint(company.companies, url_prefix=config['ROUTE_PREFIX'] + "companies")
app.register_blueprint(genre.genres, url_prefix=config["ROUTE_PREFIX"] + "genres")
app.register_blueprint(platform.platforms, url_prefix=config["ROUTE_PREFIX"] + "platforms")

if __name__ == '__main__':
    print('Routing Table')
    print(app.url_map)
    app.run(host=config["HOST"], port=config["PORT"], use_reloader=False)
    # app.run(use_reloader=False)


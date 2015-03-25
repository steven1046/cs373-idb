__author__ = 'alexanderventura'

from configuration.app import app
from configuration.config import config

if __name__ == '__main__':
    print('Routing Table')
    print(app.url_map)
    app.run(host=config["HOST"], port=config["PORT"], use_reloader=False)


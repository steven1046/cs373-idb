__author__ = 'alexanderventura'

from configuration.app import app

if __name__ == '__main__':
    print('Routing Table')
    print(app.url_map)
    app.run(use_reloader=False)

if __name__ != '__main__':
    print('this is a script that should be executed directly.')
    quit()

import logging

from config import load_config
from settings import Settings, init_settings
from app import *
from setup import setup

setup.init()

logging.info(app_ver)

config = load_config()
settings = init_settings(config['db'])

my_key = settings.get_or_input('secret_key', 'your secret key')
logging.debug('secret key = ' + my_key)

#app.secret_key = rep_key
#http_server = HTTPServer(WSGIContainer(app))
#http_server.listen(rep_port)
#IOLoop.instance().start()
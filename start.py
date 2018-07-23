if __name__ != '__main__':
    print('this is a script that should be executed directly.')
    quit()

import json

from setup import *
from flask import Flask, request, send_from_directory, send_file, render_template
from flask_compress import Compress
from flask_reggie import Reggie

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from config import load_config
from settings import Settings, init_settings

app_ver = 'wordman test 1.0.0'

setup.init()
logging.info(app_ver)

config = load_config()
settings = init_settings(config['db'])

my_key = settings.get_or_input('secret_key', 'your secret key')
logging.debug('secret key = ' + my_key)

my_port = settings.get_or_input('http_port', 'your http port', type(0))
logging.debug('http port = ' + my_port)


# Start HTTP Server
app = Flask(__name__, template_folder = './themes')
Reggie(app)
compress = Compress()
compress.init_app(app)

def put_data():
    ret = {}
    data = {'Apple':{'Ref':5, 'Date':'2017-01-01 00:00:00'}, 'Box':{'Ref':11, 'Date':'2017-01-01 12:34:56'}, 'Car':{'Ref':756, 'Date':'2017-01-01 02:47:01'}}
    ret['app_ver'] = app_ver
    ret['data'] = data
    return ret

@app.route('/')
def main():
    return render_template('aaa/index.html', data=put_data()) # html_minify()

@app.route('/themes/<path:name>')
def themes(name = None):
    parent_dir = './themes/' + os.path.dirname(name)
    file_name = os.path.basename(name)
    return send_from_directory(parent_dir, file_name)

app.secret_key = my_key

http_server = HTTPServer(WSGIContainer(app))
http_server.listen(my_port)
IOLoop.instance().start()

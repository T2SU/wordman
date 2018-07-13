if __name__ != '__main__':
    print('this is a script that should be executed directly.')
    quit()

from setup import *
from flask import Flask, request, send_from_directory, send_file
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
app = Flask(__name__)
Reggie(app)
compress = Compress()
compress.init_app(app)

@app.route('/')
def main():
    return send_from_directory('./themes/aaa', 'index.html')

@app.route('/themes/<path:name>')
def themes(name = None):
    parent_dir = './themes/' + os.path.dirname(name)
    file_name = os.path.basename(name)
    #ext = os.path.splitext(file_name)[1][1:]
    #if ext == 'css' or ext == 'less' or ext == 'scss':
    #    return css_minify(send_from_directory(parent_dir, file_name))   
    #elif ext == 'js' or ext =='json':
    #    return js_minify(send_from_directory(parent_dir, file_name))
    #elif ext == 'html':
    #    return html_minify(send_from_directory(parent_dir, file_name))   
    #else:
    return send_from_directory(parent_dir, file_name)

app.secret_key = my_key

http_server = HTTPServer(WSGIContainer(app))
http_server.listen(my_port)
IOLoop.instance().start()
if __name__ != '__main__':
    print('this is a script that should be executed directly.')
    quit()

import json

from setup import *
from flask import Flask, request, send_from_directory, send_file, render_template, abort
from flask_compress import Compress
from flask_reggie import Reggie

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from config import load_config
from settings import Settings, init_settings
from word import *

app_ver = 'wordman test 1.0.1'




###### 프로그램 초기화 및 설정 시작 ######


setup.init()
logging.info(app_ver)

config = load_config()
settings = init_settings(config['db'])
words = init_words(config['db'])
examples = init_examples(config['db'])
synonyms = init_synonyms(config['db'])
antonyms = init_antonyms(config['db'])

my_key = settings.get_or_input('secret_key', 'your secret key')
logging.debug('secret key = ' + my_key)

my_port = settings.get_or_input('http_port', 'your http port', type(0))
logging.debug('http port = ' + my_port)


# Start HTTP Server
app = Flask(__name__, template_folder = './themes')
Reggie(app)
compress = Compress()
compress.init_app(app)


###### 프로그램 초기화 및 설정 끝 ######





###### 로직 영역 시작 ######


# 사전 단어 데이터 가져오는 함수.
def get_data(orderby, d, page):
    ret = {}                                          # 데이터를 저장하여 반환할 딕쎠너리
    ret['app_ver'] = app_ver
    ret['data'] = words.load_words(orderby, d, page)  # 디비에서 지정된 옵션으로 단어를 가져온다.
    return ret

@app.route('/')
def main():
    orderby = request.args.get('orderby')            # GET 으로 전달된 'orderby' 값 (어느 열 기준으로 정렬할지)
    d = request.args.get('dir')                      # GET 으로 전달된 'dir' 값. (오름차순/내림차순)
    page = request.args.get('page')                  # GET 으로 전달된 'page' 값. (몇 페이지를 볼 것인가?)

    return render_template('aaa/index.html', data=get_data(orderby, d, page)) # get_data 함수로 사전 단어 데이터를 가져온다.

@app.route('/add', methods=['POST'])
def add_word():
    word = request.form['word']
    logging.debug('add word = ' + word)

    try:
        words.new_word(word)           # 새 단어를 DB에 넣는다.
        ret = {}                       # HTML로 전달할 데이터용 딕쎠너리를 생성.
        ret['word'] = word
        ret['ref'] = '0'
        ret['time'] = curtime()        # 현재시간을 Last Referred로 기본 지정.
        return json.dumps(ret)         # JSON으로 만들어서 HTML로 반환. (AJAX 기법을 사용한다.)
    
    except sqlite3.IntegrityError: # 단어 추가시도하다가 이미 있는 단어면 이 예외가 나오더라.
        abort(400)                 # HTTP 에러 코드 400을 보냄. html에서 400을 받으면 중복 단어로 처리하게 만들어야 한다.
        


###### 로직 영역 끝 ######








# 기타 HTML 처리 파트 및 서버 시작 파트.


@app.route('/themes/<path:name>')
def themes(name = None):
    parent_dir = './themes/' + os.path.dirname(name)
    file_name = os.path.basename(name)
    return send_from_directory(parent_dir, file_name)

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

app.secret_key = my_key
app.config['TEMPLATES_AUTO_RELOAD'] = True

http_server = HTTPServer(WSGIContainer(app))
http_server.listen(my_port)
IOLoop.instance().start()

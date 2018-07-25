import sqlite3
import logging
from setup import curtime

# 단어 관련 클래스 집합 스크립트


# 새로운 단어 관리 클래스
def init_words(db_name):
    return Words(db_name)

# 새로운 Example 관리 클래스
def init_examples(db_name):
    return ExampleWordContext(db_name)

#새로운 Synonym 관리 클래스
def init_synonyms(db_name):
    return SynonymWordContext(db_name)

#새로운 Antonym 관리 클래
def init_antonyms(db_name):
    return AntonymWordContext(db_name)


# Words 클래스. 단어들을 관리하는 클래스임.

class Words:
    def __init__(self, name):
        self.db_name = name
        with sqlite3.connect(self.db_name + '.db', check_same_thread = False) as conn:
            curs = conn.cursor()
            curs.execute('create table if not exists `words` (`word` text not null, `ref` integer, `lastref` text, primary key (`word`))')
            curs.execute('create table if not exists `examples` (`word` text not null, `example` text)')
            curs.execute('create table if not exists `synonyms` (`word` text not null, `synonym` text)')
            curs.execute('create table if not exists `antonyms` (`word` text not null, `antonym` text)')
        logging.debug('[words] ready db')

    # 새로운 단어 등록.
    def new_word(self, word):
        with sqlite3.connect(self.db_name + '.db', check_same_thread = False) as conn:
            curs = conn.cursor()
            curs.execute('insert into `words` (`word`, `ref`, `lastref`) values (?, ?, ?)', [word, 0, curtime()])

    # 등록된 단어 디비에서 불러오기
    def load_words(self, _orderby, _d, _page):
        with sqlite3.connect(self.db_name + '.db', check_same_thread = False) as conn:
            curs = conn.cursor()

            # 기본값
            page = 1
            orderby = 'word'
            d = 'asc'

            # _page 값이 있으면 (= None 이 아니면) 그 값을 가져옴.
            if (_page is not None):
                page = int(_page)
                
            # _orderby와 _d 값이 있으면 (= None 이 아니면) 그 값을 가져옴.
            if (_orderby is not None and _d is not None):
                orderby = str(_orderby)
                d = str(_d)

            # 한 페이지에 50개의 단어
            s = (page - 1) * 50
                
            query = 'select `word`, `ref`, `lastref` from `words` order by `' + orderby + '` collate nocase ' + d + ' limit ' + str(s) + ', 50';
            curs.execute(query)
            ret = curs.fetchall()
            return ret

# Examples, Synonyms, Antonyms 등 단어의 세부 항목들을 관리하는데 사용할 기본 클래스. 필요한 항목에서 상속하여 사용한다.
class WordContext:
    def __init__(self, dbname, name):
        self.name = name
        self.db_name = dbname
        with sqlite3.connect(self.db_name + '.db', check_same_thread = False) as conn:
            curs = conn.cursor()
            curs.execute('create table if not exists `' + self.name + 's` (`word` text not null, `' + self.name + '` text)')
        logging.debug('[' + name + 's] ready db')

    # 단어 추가/수정/삭제.
    #
    # 추가:
    #   oldone값이 없고, newone 값이 있다.
    # 수정:
    #   oldone값이 있고, newone 값이 있다.
    # 삭제:
    #   oldone값이 있고, newone 값이 없다.
    #
    def change(self, word, oldone, newone):
        with sqlite3.connect(self.db_name + '.db', check_same_thread = False) as conn:
            curs = conn.cursor()
            o_one = oldone.strip()
            n_one = newone.strip()
            if (len(n_one) == 0):
                curs.execute('delete from `' + self.name + 's` where `word` = ? and `' + self.name + '` = ?', [word, o_one])
                return 'del'
            elif (len(o_one) == 0):
                curs.execute('insert into `' + self.name + 's` (`word`, `' + self.name + '`) values (?, ?)', [word, n_one])
                return 'new'
            else:
                curs.execute('update `' + self.name + 's` set `' + self.name + '` = ? where `word` = ? and `' + self.name + '` = ?', [n_one, word, o_one])
                return 'mod'
    # 해당 단어의 현재 클래스가 관리하는 세부 항목을 가져온다.
    def get(self, word):
        with sqlite3.connect(self.db_name + '.db', check_same_thread = False) as conn:
            curs = conn.cursor()
            curs.execute('select `' + self.name + '` from `' + self.name + 's` where `word` = ?', [word])
            got_data = curs.fetchall()
            if got_data:
                return got_data
            return []



# 세부 항목 상속 클래스

class ExampleWordContext(WordContext):
    def __init__(self, dbname):
        super().__init__(dbname, 'example')
        
class SynonymWordContext(WordContext):
    def __init__(self, dbname):
        super().__init__(dbname, 'synonym')
    
class AntonymWordContext(WordContext):
    def __init__(self, dbname):
        super().__init__(dbname, 'antonym')

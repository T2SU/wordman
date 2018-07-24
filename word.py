import sqlite3
import logging
from setup import curtime

# 단어 관련 클래스 집합 스크립트


def init_words(db_name):
    return Words(db_name)

def init_examples(db_name):
    return ExampleWordContext(db_name)

def init_synonyms(db_name):
    return SynonymWordContext(db_name)

def init_antonyms(db_name):
    return AntonymWordContext(db_name)


# Words 클래스

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
        
    def new_word(self, word):
        with sqlite3.connect(self.db_name + '.db', check_same_thread = False) as conn:
            curs = conn.cursor()
            curs.execute('insert into `words` (`word`, `ref`, `lastref`) values (?, ?, ?)', [word, 0, curtime()])

    def load_words(self, _orderby, _d, _page):
        with sqlite3.connect(self.db_name + '.db', check_same_thread = False) as conn:
            curs = conn.cursor()

            page = 1
            orderby = 'word'
            d = 'asc'
            
            if (_page is not None):
                page = int(_page)

            if (_orderby is not None or _d is not None):
                orderby = str(_orderby)
                d = str(_d)

            s = (page - 1) * 50
                
            query = 'select `word`, `ref`, `lastref` from `words` order by `' + orderby + '` collate nocase ' + d + ' limit ' + str(s) + ', 50';
            curs.execute(query)
            ret = curs.fetchall()
            return ret
        
class WordContext:
    def __init__(self, dbname, name):
        self.name = name
        self.db_name = dbname
        with sqlite3.connect(self.db_name + '.db', check_same_thread = False) as conn:
            curs = conn.cursor()
            curs.execute('create table if not exists `' + self.name + 's` (`word` text not null, `' + self.name + '` text)')
        logging.debug('[' + name + 's] ready db')

    def change(self, word, oldone, newone):
        with sqlite3.connect(self.db_name + '.db', check_same_thread = False) as conn:
            curs = conn.cursor()
            o_one = oldone.strip()
            n_one = newone.strip()
            if (len(n_one) == 0):
                curs.execute('update `' + self.name + 's` set `' + self.name + '` = ? where `word` = ? and `' + self.name + '` = ?', [n_one, word, o_one])
            elif (len(o_one) == 0):
                curs.execute('insert into `' + self.name + 's` (`word`, `' + self.name + '`) values (?, ?)', [word, n_one])
            else:
                curs.execute('delete from `' + self.name + 's` where `word` = ? and `' + self.name + '` = ?', [word, o_one])
        
    def get(self, word):
        with sqlite3.connect(self.db_name + '.db', check_same_thread = False) as conn:
            curs = conn.cursor()
            curs.execute('select `' + self.name + '` from `' + self.name + 's` where `word` = ?', [word])
            got_data = curs.fetchall()
            if got_data:
                return got_data
            return []

class ExampleWordContext(WordContext):
    def __init__(self, dbname):
        super().__init__(dbname, 'example')
        
class SynonymWordContext(WordContext):
    def __init__(self, dbname):
        super().__init__(dbname, 'synonym')
    
class AntonymWordContext(WordContext):
    def __init__(self, dbname):
        super().__init__(dbname, 'antonym')

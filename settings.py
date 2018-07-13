import sqlite3
import logging
from input import read_input

def init_settings(db_name):
    return Settings(db_name)

class Settings:
    def __init__(self, name):
        self.db_name = name
        logging.debug('db name = ' + self.db_name)
        with sqlite3.connect(self.db_name + '.db', check_same_thread = False) as conn:
            curs = conn.cursor()
            curs.execute('create table if not exists `settings` (`key` text not null, `data` text, primary key (`key`))')
        logging.debug('ready db and settings')

    def set(self, key, value):
        with sqlite3.connect(self.db_name + '.db', check_same_thread = False) as conn:
            curs = conn.cursor()
            curs.execute('insert or replace into `settings` (`key`, `data`) values (?, ?)', [key, value])

    def get(self, key):
        with sqlite3.connect(self.db_name + '.db', check_same_thread = False) as conn:
            curs = conn.cursor()
            curs.execute('select `data` from `settings` where `key` = ?', [key])
            got_data = curs.fetchall()
            if got_data:
                return got_data[0][0]
            return ''

    def get_or_input(self, key, input_name):
        my_data = self.get(key)
        if not my_data:
            my_data = read_input(input_name)
            self.set(key, my_data)
        return my_data;


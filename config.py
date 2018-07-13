import json
import logging
from input import read_input

def read_config():
    config_text = open('config.json').read()
    config = json.loads(config_text)
    return config

def write_config(data):
    data_text = json.dumps(data)
    with open('config.json', 'w') as f:
        f.write(data_text)

def init_config():
    logging.info('config.json was not found. generate a new config file')
    setting_data = {}
    setting_data['db'] = read_input('db name')
    write_config(setting_data)
    return setting_data

def load_config():
    logging.debug('load config')
    try:
        return read_config()
    except:
        return init_config()
import json
from input import *

def read_settings():
	settings_text = open('settings.json').read()
	settings = json.loads(settings_text)
	return settings

def write_settings(data):
	data_text = json.dumps(data)
	with open('settings.json', 'w') as f:
		f.write(data_text)

def init_settings():
	print('settings.json was not found. generate a new settings file')
	setting_data = {}
	setting_data['db'] = read_input('db name')
	write_settings(setting_data)
	return setting_data

def load_settings():
	print('load settings')
	try:
		return read_settings()
	except:
		return init_settings()

def db_conn(db_name):
	conn = sqlite3.connect(db_name + '.db', check_same_thread = False)
	curs = conn.cursor()

import logging
import os
import time

class setup:
	def init():
		if not os.path.exists('themes'):
			os.makedirs('themes')
		if not os.path.exists('logs'):
			os.makedirs('logs')
		setup.init_logger()

	def init_logger():
		logFormatter = logging.Formatter(fmt='[%(asctime)s](%(levelname)s) %(message)s', datefmt='%Y/%m/%d %H:%M:%S')
		rootLogger = logging.getLogger()
		
		logFileIndex = 0
		logFilePath = ''
		while 1:
			logFilePath = '{0}/{1}.log'.format('logs', 'wordmanlog' + str(logFileIndex));
			if not os.path.exists(logFilePath):
				break
			logFileIndex += 1

		fileHandler = logging.FileHandler(logFilePath)
		fileHandler.setFormatter(logFormatter)
		rootLogger.addHandler(fileHandler)

		consoleHandler = logging.StreamHandler()
		consoleHandler.setFormatter(logFormatter)
		rootLogger.addHandler(consoleHandler)

		rootLogger.setLevel(logging.DEBUG)
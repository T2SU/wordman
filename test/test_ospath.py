import os

while 1:
	text = input()
	try:
		print('basename = ' + os.path.basename(text))
	except:
		print('unknown basename')
		pass
	try:
		print('dirname = ' + os.path.dirname(text))
	except:
		print('unknown durname')
		pass
	try:
		print('splitext = ' + str(os.path.splitext(text)))
	except:
		print('unknown splitext')
		pass
def read_input(what, expected_type = type('')):
	while 1:
		print('type ' + what + '? ', end='')
		input_raw = input()
		try:
			if input_raw != '':
				if expected_type is int:
					return int(input_raw)
				elif expected_type is bool:
					return bool(input_raw)
				elif expected_type is float:
					return float(input_raw)
				elif expected_type is str:
					return str(input_raw)
				else:
					return input_raw
		except:
			pass
			
		print('error. please type ' + what + '.')
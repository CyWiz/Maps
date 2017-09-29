import json
#path='C:\Users\ANMOL\Desktop\dataset\chicago_2500'
with open('chicago_2500.json') as data_file:
	crime_data=json.load(data_file)
	for key, value in crime_data.items():
		if key=='data':
			for key_1 in value: #datalevel
				print(key_1[9])
				print(key_1[12])
				print(key_1[22])
				print key_1[23],'\n\n'
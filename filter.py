import json
import csv
import sys
path='chicago_2500.json'
i=600
with open('chicago_2500.json') as data_file:
	crime_data=json.load(data_file)
with open('test.csv','wb') as file_name:
    writer = csv.writer(file_name)
    writer.writerow( ('id', 'Time_Slot', 'Type_of_crime','Latitude','Longitude','Crime id'))
    for key,value in crime_data.items():
        if key=='data':
            for key_1 in value: #datalevel
                if(key_1[12]=='THEFT'):
                    writer.writerow( (i,key_1[9], key_1[12],key_1[22],key_1[23],6))
                    i+=1
                if(key_1[12]=='ROBBERY'):
                    writer.writerow( (i,key_1[9], key_1[12],key_1[22],key_1[23],5))
                    i+=1
                if(key_1[12]=='ASSAULT'):
                    writer.writerow( (i,key_1[9], key_1[12],key_1[22],key_1[23],4))
                    i+=1
                if(key_1[12]=='CRIM SEXUAL ASSAULT'):
                    writer.writerow( (i,key_1[9], key_1[12],key_1[22],key_1[23],2))
                    i+=1
                if(key_1[12]=='SEX OFFENSE'):
                    writer.writerow( (i,key_1[9], key_1[12],key_1[22],key_1[23],1))
                    i+=1
                if(key_1[12]=='INTIMADATION'):
                    writer.writerow( (i,key_1[9], key_1[12],key_1[22],key_1[23],3))
                    i+=1
                if(key_1[12]=='OTHER OFFENCE'):
                    #writer.writerow( (i,key_1[9], key_1[12],key_1[22],key_1[23],7))
                    print('\n')
    file_name.close()

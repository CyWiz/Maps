import googlemaps
import polyline
from datetime import datetime
import datetime
import mysql.connector


#source=raw_input("Source:")
#destination=raw_input("Destination:")
gmaps = googlemaps.Client(key='AIzaSyCsS5mQWcb4-yvDVr50J4a79ww0xK43W0o')

# Geocoding an address
#geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

# Look up an address with reverse geocoding
#reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

# Request directions via public transit
#now = datetime.now()
route_list=[]
way_points=[]
crime_id=[1,2,3,4,5,6]
crime_weight=[1074,678,211,77,583,139]
crime_threshold=[0.95510,1.4749,4.7393,12.98,1.7152,5.3475]
score=[]
frequency_list=[3,14,11,17,5,14]

#function defination for computation
def freq_factor(threshold,frequency, apna_distance):
	#print (threshold,'\t',frequency,'\t',apna_distance) 
	return ((((frequency*5/(apna_distance)-threshold)**2)*0.2)/(threshold**2))+0.8

def score_per_crime(f_fact,frequency,weight):
	return weight*frequency*f_fact

def route_score(final_weight_list):
	score_sum=0
	for i in final_weight_list:
		score_sum+=i
	return score_sum

def weight_list_gen(crime_id,crime_threshold,crime_weight, apna_distance):
	final_weight_list=[]
	for i in range(len(crime_id)):
		f_fact=freq_factor(crime_threshold[i],frequency_list[i], apna_distance)
		#print f_fact
		final_weight_list.append(score_per_crime(f_fact,frequency_list[i],crime_weight[i]))

	return final_weight_list


def mysql_query(way_point_dict):
	frequency_dict = {}
	cnx = mysql.connector.connect(user='maps',password='maps',database='CRIME')
	cursor = cnx.cursor()
	frequency_list=[0,0,0,0,0,0]
  	six=0
	five=0
	four=0
	three=0
	two=0
	one=0
	for k1,v1 in way_point_dict.items():
		latitude = k1
		longitude = v1
		query = ("SELECT     id,crime_id,(       6373 * acos (       cos ( radians("+str(latitude)+") )       * cos( radians( X(location) ) )       * cos( radians( Y(location) ) - radians("+str(longitude)+") )       + sin ( radians("+str(latitude)+") )       * sin( radians( X(location) ) )     ) ) AS distance FROM spatial_storage HAVING distance < 0.5;")
		cursor.execute(query)
		for (id,crime_id,x) in cursor:
			if (id, crime_id) not in frequency_dict.items():
				#print id,'\t',crime_id
				frequency_dict[id] = crime_id
	cnx.close()

	for i,j in frequency_dict.items():
		if j==6:
			six+=1
      		#print six
      	if j==5:
      		five+=1
      	if j==4:
      		four+=1
      	if j==3:
      		three+=1
      	if j==2:
      		two+=1
      	if j==1:
    		one+=1
	frequency_list[0]=one
	frequency_list[1]=two
	frequency_list[2]=three
	frequency_list[3]=four
	frequency_list[4]=five
	frequency_list[5]=six
	return (frequency_list)
#end of function defination block


directions_result = gmaps.directions(source,
                                     destination,
                                     mode="walking",
                                     alternatives="True")

apna_distance = 0
for routes in directions_result:
	for key,value in routes.items():
		if key == 'legs':
			for k,v in value[0].items():
  				if k == "distance":
  					#apna_distance = str(v['text'])
  					#print(float(apna_distance.split()[0]))
  					distance_str = str(v['text'])
  					apna_distance = float(distance_str.split()[0])
  					#print apna_distance


for routes in directions_result:
	for key,value in routes.items():  				
		if key == 'overview_polyline':
			for points,poly in value.items():
				#print (poly,'\n\n')
				#route_list.append(poly)
				#way_points.append(polyline.decode(poly))
				#pass the waypoints of this route to mysql
				#function returns frequency list for this route
				frequency_list=[]
				frequency_list=mysql_query(dict(polyline.decode(poly)))
				score.append(route_score(weight_list_gen(crime_id,crime_threshold,crime_weight, apna_distance)))

print(score)


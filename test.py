import googlemaps
import polyline
from datetime import datetime
source=raw_input("Source:")
destination=raw_input("Destination:")
gmaps = googlemaps.Client(key='AIzaSyCsS5mQWcb4-yvDVr50J4a79ww0xK43W0o')

# Geocoding an address
#geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

# Look up an address with reverse geocoding
#reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

# Request directions via public transit
now = datetime.now()
route_list=[]
way_points=[]
crime_id=[1,2,3,4,5,6]
crime_weight=[1074,678,211,77,583,139]
crime_threshold=[0.95510,1.4749,4.7393,12.98,1.7152,5.3475]
score=[]
frequency_list=[3,14,11,17,5,14]

#function defination for computation
def freq_factor(threshold,frequency):
	return ((((frequency-threshold)**2)*0.2)/(threshold**2))+0.8


def score_per_crime(f_fact,frequency,weight):
	return weight*frequency*f_fact

def route_score(final_weight_list):
	score_sum=0
	for i in final_weight_list:
		score_sum+=i
	return score_sum

def weight_list_gen(crime_id,crime_threshold,crime_weight):
	final_weight_list=[]
	for i in range(len(crime_id)):
		f_fact=freq_factor(crime_threshold[i],frequency_list[i])
		final_weight_list.append(score_per_crime(f_fact,frequency_list[i],crime_weight[i]))

	return final_weight_list


'''def final_route_score(route_list):
	score=[]
	for every_route in route_list:
		score.append(route_score(weight_list_gen(crime_id,crime_threshold,crime_weight)))'''

#end of function defination block


directions_result = gmaps.directions(source,
                                     destination,
                                     mode="walking",
                                     departure_time=now,alternatives="True")
#print (directions_result)
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
				frequency_list=mysql_query(polyline.decode(poly))

				score.append(route_score(weight_list_gen(crime_id,crime_threshold,crime_weight)))

print(score)




'''for i in range(len(way_points)):
	print route_list[i],'\n\n'
	print way_points[i],'\n\n'
	#print(j)'''



import datetime
import mysql.connector

cnx = mysql.connector.connect(user='maps',password='maps',database='CRIME')
cursor = cnx.cursor()
latitude=13.01561604
longitude=77.678186

query = ("SELECT     id,crime_id,(       6373 * acos (       cos ( radians("+str(latitude)+") )       * cos( radians( X(location) ) )       * cos( radians( Y(location) ) - radians("+str(longitude)+") )       + sin ( radians("+str(latitude)+") )       * sin( radians( X(location) ) )     ) ) AS distance FROM spatial_storage HAVING distance < 4;")
cursor.execute(query)
for (id,type_of_crime,location) in cursor:
  print("{}|	 {} |	{}".format(
    id,type_of_crime,location))


cursor.close()
cnx.close()

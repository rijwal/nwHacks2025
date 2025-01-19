from pymongo import MongoClient
from twilio.rest import Client
from math import radians, sin, cos, sqrt, atan2




account_sid = "AC060399fb65751638f99022d9c082e7bc" 
auth_token = "692a2f635bedd834c0c0301fb1acb4b1"
twilio_phone_number = "+15872065879" 




mongo_uri = "YOUR_MONGO_DB_CONNECTION_URI"
database_name = "YOUR_DATABASE_NAME"
collection_name = "YOUR_COLLECTION_NAME"


# FIGURE OUT HOW TO GET THIS FROM MONGODB
fire_latitude = 37.7749 
fire_longitude = -122.4194 




EARTH_RADIUS_KM = 6371.0




def calculate_distance(lat1, lon1, lat2, lon2):
   lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
   dlat = lat2 - lat1
   dlon = lon2 - lon1
   a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
   c = 2 * atan2(sqrt(a), sqrt(1 - a))
   distance = EARTH_RADIUS_KM * c
   return distance




client = Client(account_sid, auth_token)




mongo_client = MongoClient(mongo_uri)
db = mongo_client[database_name]
collection = db[collection_name]




try:
   user_data = collection.find({}, {"phoneNumber": 1, "latitude": 1, "longitude": 1, "_id": 0})


   if user_data.count() == 0:
       print("No user data found in the database.")
   else:
       print("Processing user data...")




       for user in user_data:
           phone_number = user.get("phoneNumber")
           user_latitude = user.get("latitude")
           user_longitude = user.get("longitude")


           if phone_number and user_latitude and user_longitude:
 
               distance = calculate_distance(fire_latitude, fire_longitude, user_latitude, user_longitude)


               print(f"Distance to {phone_number}: {distance:.2f} km")

                if distance < 50:
                   try:
                       message = client.messages.create(
                           body=f"Alert: A fire is detected near your location. Please stay away from the area. Distance: {distance:.2f} km.",
                           from_=twilio_phone_number,
                           to=phone_number
                       )
                       print(f"Alert sent to {phone_number}! SID: {message.sid}")
                   except Exception as e:
                       print(f"Failed to send alert to {phone_number}: {e}")
               else:
                   print(f"{phone_number} is safe. No alert sent.")
           else:
               print("Incomplete user data. Skipping...")
except Exception as e:
   print(f"Failed to process user data: {e}")
finally:
   mongo_client.close()

from pymongo import MongoClient
from twilio.rest import Client
from math import radians, sin, cos, sqrt, atan2


#USERS API DETAILS...




mongo_uri = "mongodb+srv://nwhacksuser:nwhackspassword@nwhacks.nmgdk.mongodb.net/?retryWrites=true&w=majority&appName=nwhacks"
database_name = "wildfires"
coordinates_collection_name = "coordinates"
users_collection_name = "users"




EARTH_RADIUS_KM = 6371.0
ALERT_DISTANCE_KM = 700 #for demo purposes number is inflated, this value should truely be approximately 50-100km.


def calculate_distance(lat1, lon1, lat2, lon2):
   lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
   dlat = lat2 - lat1
   dlon = lon2 - lon1
   a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
   c = 2 * atan2(sqrt(a), sqrt(1 - a))
   return EARTH_RADIUS_KM * c


mongo_client = MongoClient(mongo_uri)
db = mongo_client[database_name]
coordinates_collection = db[coordinates_collection_name]
users_collection = db[users_collection_name]


try:
   fire_data = list(coordinates_collection.find({}, {"latitude": 1, "longitude": 1, "_id": 0}))
   if not fire_data:
       print("No wildfire data found in the database.")
   else:
       print(f"Retrieved wildfire data: {fire_data}")
except Exception as e:
   print(f"An error occurred while fetching wildfire data: {e}")




try:
   user_data = list(users_collection.find({}, {
       "phoneNumber": 1,
       "location.latitude": 1,
       "location.longitude": 1,
       "_id": 0
   }))


   if not user_data:
       print("No user data found in the database.")
   else:
       print(f"Retrieved user data: {user_data}")


       twilio_client = Client(account_sid, auth_token)


       for user in user_data:
           phone_number = user.get("phoneNumber")
           user_location = user.get("location", {})
           user_latitude = user_location.get("latitude")
           user_longitude = user_location.get("longitude")


           print(f"User: {phone_number}, Latitude={user_latitude}, Longitude={user_longitude}")


           if phone_number and user_latitude is not None and user_longitude is not None:
               for fire in fire_data:
                   fire_latitude = fire["latitude"]
                   fire_longitude = fire["longitude"]
                   print(f"Checking fire location: Latitude={fire_latitude}, Longitude={fire_longitude}")


                   distance = calculate_distance(fire_latitude, fire_longitude, user_latitude, user_longitude)


                   print(f"Distance from fire to user {phone_number}: {distance:.2f} km")


                   if distance < ALERT_DISTANCE_KM:


                       try:
                           message = twilio_client.messages.create(
                               body=(
                                   f"Alert: A fire is detected near your location. "
                                   f"Please stay away from the area. Distance: {distance:.2f} km."
                               ),
                               from_=twilio_phone_number,
                               to=phone_number
                           )
                           print(f"Alert sent to {phone_number}! SID: {message.sid}")
                       except Exception as e:
                           print(f"Failed to send alert to {phone_number}: {e}")
                       break
                   else:
                       print(f"Fire at {fire_latitude}, {fire_longitude} is too far from {phone_number}.")
           else:
               print("Incomplete user data. Skipping...")
except Exception as e:
   print(f"An error occurred while processing user data: {e}")
finally:
   mongo_client.close()









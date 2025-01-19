from pymongo import MongoClient

# MongoDB Atlas connection string
mongo_uri = "mongodb+srv://nwhacksuser:nwhackspassword@nwhacks.nmgdk.mongodb.net/?retryWrites=true&w=majority&appName=nwhacks"

# Connect to MongoDB
client = MongoClient(mongo_uri)
db = client["wildfires"]  # Database name
collection = db["coordinates"]  # Collection name

# Fetch all documents (latitude and longitude data)
try:
    lat_lon_data = list(collection.find({}, {"_id": 0}))  # Exclude the _id field
    print("Retrieved data:", lat_lon_data)
except Exception as e:
    print(f"An error occurred while fetching data: {e}")

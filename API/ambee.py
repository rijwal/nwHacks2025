import csv
import requests
from pymongo import MongoClient

# Replace with your actual FIRMS MAP_KEY
MAP_KEY = "aed1d2f0a335f1545bb8e3ca8b526751"

# MongoDB Atlas connection string (replace <db_username> and <db_password>)
mongo_uri = "mongodb+srv://nwhacksuser:nwhackspassword@nwhacks.nmgdk.mongodb.net/?retryWrites=true&w=majority&appName=nwhacks"

# Connect to MongoDB Atlas
client = MongoClient(mongo_uri)
db = client["wildfires"]  # Database name
collection = db["coordinates"]  # Collection name

# Define the API URL for wildfire data
country_code = "USA"
dataset = "VIIRS_SNPP_NRT"  # Example dataset
days = "2"  # Fetch data for the last 2 days
url = f"https://firms.modaps.eosdis.nasa.gov/api/country/csv/{MAP_KEY}/{dataset}/{country_code}/{days}"

try:
    # Fetch data from the API
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad status codes

    # Decode the CSV response
    data = response.text.splitlines()
    reader = csv.DictReader(data)

    # Extract latitude and longitude and prepare for MongoDB insertion
    lat_lon_data = []
    for row in reader:
        if "latitude" in row and "longitude" in row:
            lat_lon_data.append({
                "latitude": float(row["latitude"]),
                "longitude": float(row["longitude"])
            })

    if lat_lon_data:
        # Insert data into MongoDB
        result = collection.insert_many(lat_lon_data)
        print(f"Inserted {len(result.inserted_ids)} wildfire locations into MongoDB!")
    else:
        print("No wildfire data to store.")

except requests.exceptions.RequestException as e:
    print(f"Error fetching data: {e}")
except Exception as e:
    print(f"An error occurred: {e}")

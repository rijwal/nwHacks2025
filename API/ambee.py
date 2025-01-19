# import csv
# import requests

# # Replace with your actual FIRMS MAP_KEY
# MAP_KEY = "aed1d2f0a335f1545bb8e3ca8b526751"

# # Define the API URL for Canada's wildfire data (VIIRS example, last 3 days)
# country_code = "USA"
# dataset = "VIIRS_SNPP_NRT"  # Example dataset
# days = "2"  # Fetch data for the last 3 days
# url = f"https://firms.modaps.eosdis.nasa.gov/api/country/csv/{MAP_KEY}/{dataset}/{country_code}/{days}"

# try:
#     # Make the API request
#     response = requests.get(url)
#     response.raise_for_status()  # Raise an error for bad status codes

#     # Decode the CSV response
#     data = response.text.splitlines()
#     reader = csv.DictReader(data)

#     # Extract latitude and longitude
#     lat_lon_data = [(row["latitude"], row["longitude"]) for row in reader]

#     # Display the results
#     for lat, lon in lat_lon_data:
#         print(f"Latitude: {lat}, Longitude: {lon}")

# except requests.exceptions.RequestException as e:
#     print(f"Error fetching data: {e}")

import csv
import requests
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Replace with your actual FIRMS MAP_KEY
MAP_KEY = "aed1d2f0a335f1545bb8e3ca8b526751"

# Define the API URL for wildfire data (VIIRS example, last 2 days)
country_code = "USA"
dataset = "VIIRS_SNPP_NRT"  # Example dataset
days = "2"  # Fetch data for the last 2 days
url = f"https://firms.modaps.eosdis.nasa.gov/api/country/csv/{MAP_KEY}/{dataset}/{country_code}/{days}"

# MongoDB connection details
uri = "mongodb+srv://<db_username>:<db_password>@costas1.y4kzr.mongodb.net/?retryWrites=true&w=majority&appName=Costas1"
DATABASE_NAME = "wildfire_data"
COLLECTION_NAME = "fire_locations"

# MongoDB setup
client = MongoClient(uri, server_api=ServerApi('1'))

try:
    # Confirm connection
    client.admin.command('ping')
    print("Pinged your deployment. Successfully connected to MongoDB!")

    # Fetch wildfire data
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad status codes
    data = response.text.splitlines()
    reader = csv.DictReader(data)

    # Extract latitude and longitude
    fire_data = [{"latitude": float(row["latitude"]), "longitude": float(row["longitude"])} for row in reader]

    # Insert data into MongoDB
    if fire_data:
        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]
        result = collection.insert_many(fire_data)
        print(f"Inserted {len(result.inserted_ids)} records into MongoDB.")
    else:
        print("No data to insert.")

except requests.exceptions.RequestException as e:
    print(f"Error fetching data: {e}")

except Exception as e:
    print(f"Error: {e}")



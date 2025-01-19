from apscheduler.schedulers.blocking import BlockingScheduler
import csv
import requests
from pymongo import MongoClient
import logging

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Replace with your actual FIRMS API key
MAP_KEY = "aed1d2f0a335f1545bb8e3ca8b526751"

# MongoDB Atlas connection string
mongo_uri = "mongodb+srv://nwhacksuser:nwhackspassword@nwhacks.nmgdk.mongodb.net/?retryWrites=true&w=majority&tlsAllowInvalidCertificates=true"

# Connect to MongoDB Atlas
client = MongoClient(mongo_uri)
db = client["wildfires"]
collection = db["coordinates"]

# API Configuration
country_code = "CAN"
dataset = "VIIRS_SNPP_NRT"
days = "2"
url = f"https://firms.modaps.eosdis.nasa.gov/api/country/csv/{MAP_KEY}/{dataset}/{country_code}/{days}"

def fetch_and_store_data():
    try:
        # Fetch data from the API
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.text.splitlines()
        if not data or len(data) <= 1:
            logger.warning("No data returned from the API or invalid response format.")
            return

        # Parse CSV data
        reader = csv.DictReader(data)
        lat_lon_data = []
        for row in reader:
            try:
                latitude = float(row["latitude"])
                longitude = float(row["longitude"])
                confidence = row["confidence"]
                lat_lon_data.append({
                    "latitude": latitude,
                    "longitude": longitude,
                    "confidence": confidence
                })
            except ValueError as ve:
                logger.warning(f"Invalid data found and skipped: {row}, error: {ve}")

        # Replace old data in MongoDB
        collection.delete_many({})
        logger.info("Old data deleted from the database.")

        if lat_lon_data:
            result = collection.insert_many(lat_lon_data)
            logger.info(f"Inserted {len(result.inserted_ids)} new wildfire locations into MongoDB.")
        else:
            logger.info("No valid wildfire data to store.")

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching data from API: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

# Scheduler setup
scheduler = BlockingScheduler()
scheduler.add_job(fetch_and_store_data, 'interval', hours=1)

logger.info("Scheduler started. Fetching data every hour...")
fetch_and_store_data()  # Remove this if you don't want an immediate run
scheduler.start()
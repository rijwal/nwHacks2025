import csv
import requests
import pymongo  # Add this import statement
from datetime import datetime
from config import MAP_KEY, MONGO_URI, DATABASE_NAME, COLLECTION_NAME

def fetch_and_store_firms_data():
    # MongoDB connection
    client = pymongo.MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]

    # FIRMS API URL for wildfire data (e.g., USA)
    country_code = "USA"
    dataset = "VIIRS_SNPP_NRT"  # Example dataset
    days = "1"  # Fetch data for the last 1 day
    url = f"https://firms.modaps.eosdis.nasa.gov/api/country/csv/{MAP_KEY}/{dataset}/{country_code}/{days}"

    try:
        # Make the API request
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes

        # Decode the CSV response
        data = response.text.splitlines()
        reader = csv.DictReader(data)

        # Prepare data for MongoDB
        wildfire_data = []
        for row in reader:
            # Convert values as needed
            row["latitude"] = float(row["latitude"])
            row["longitude"] = float(row["longitude"])
            row["bright_ti4"] = float(row["bright_ti4"]) if "bright_ti4" in row else None
            row["bright_ti5"] = float(row["bright_ti5"]) if "bright_ti5" in row else None
            row["acq_date"] = datetime.strptime(row["acq_date"], "%Y-%m-%d")
            row["acq_time"] = row["acq_time"]
            row["confidence"] = int(row["confidence"]) if "confidence" in row else None

            wildfire_data.append(row)

        # Insert data into MongoDB
        if wildfire_data:
            result = collection.insert_many(wildfire_data)
            print(f"Inserted {len(result.inserted_ids)} records into MongoDB.")
        else:
            print("No data to insert.")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
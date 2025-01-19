import csv
import requests

# Replace with your actual FIRMS MAP_KEY
MAP_KEY = "aed1d2f0a335f1545bb8e3ca8b526751"

# Define the API URL for Canada's wildfire data (VIIRS example, last 3 days)
country_code = "USA"
dataset = "VIIRS_SNPP_NRT"  # Example dataset
days = "2"  # Fetch data for the last 3 days
url = f"https://firms.modaps.eosdis.nasa.gov/api/country/csv/{MAP_KEY}/{dataset}/{country_code}/{days}"

try:
    # Make the API request
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad status codes

    # Decode the CSV response
    data = response.text.splitlines()
    reader = csv.DictReader(data)

    # Extract latitude and longitude
    lat_lon_data = [(row["latitude"], row["longitude"]) for row in reader]

    # Display the results
    for lat, lon in lat_lon_data:
        print(f"Latitude: {lat}, Longitude: {lon}")

except requests.exceptions.RequestException as e:
    print(f"Error fetching data: {e}")
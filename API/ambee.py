import requests
import csv
from io import StringIO

# Replace with your actual FIRMS API MAP_KEY
MAP_KEY = "aed1d2f0a335f1545bb8e3ca8b526751"

# API URL for area data
# Replace 'VIIRS_SNPP_NRT' with another dataset ID if needed (e.g., MODIS_NRT)
area_url = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{MAP_KEY}/VIIRS_SNPP_NRT/-168,5,-52,83/1"

try:
    # Make the request to the API
    response = requests.get(area_url)
    response.raise_for_status()  # Raise an HTTPError for bad responses

    # Read the CSV content
    csv_data = response.text

    # Parse the CSV data
    csv_reader = csv.reader(StringIO(csv_data))
    headers = next(csv_reader)  # Skip the header row

    # Extract longitude and latitude into a 2D array
    coordinates = [[float(row[1]), float(row[0])] for row in csv_reader]  # [longitude, latitude]

    # Print the 2D array
    print("Coordinates (longitude, latitude):")
    print(coordinates)

    # Optional: Save the coordinates to a file
    with open("north_america_coordinates.txt", "w") as file:
        for coord in coordinates:
            file.write(f"{coord[0]}, {coord[1]}\n")

    print("Coordinates successfully saved to 'north_america_coordinates.txt'.")
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")


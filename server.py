from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS

# MongoDB connection
mongo_uri = "mongodb+srv://nwhacksuser:nwhackspassword@nwhacks.nmgdk.mongodb.net/?retryWrites=true&w=majority&appName=nwhacks"
client = MongoClient(mongo_uri)
db = client["wildfires"]  # Database name
collection = db["users"]  # Collection name

@app.route('/save-user-data', methods=['POST'])
def store-user-info():
    """
    API endpoint to save user phone number and location.
    """
    data = request.json

    # Validate input
    phone = data.get('phoneNumber')
    location = data.get('location')
    if not phone or not location:
        return jsonify({'error': 'Phone number and location are required.'}), 400

    try:
        # Insert data into MongoDB
        result = collection.insert_one({
            'phone_number': phone,
            'location': {
                'latitude': location['latitude'],
                'longitude': location['longitude']
            }
        })
        return jsonify({'message': 'User data saved successfully!', 'id': str(result.inserted_id)}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)  # Make sure Flask listens to all interfaces
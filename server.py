from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)


mongo_uri = "mongodb+srv://<username>:<password>@cluster.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(mongo_uri)
db = client["user_data"] 
collection = db["user_locations"]  

@app.route('/save-user-data', methods=['POST'])
def save_user_data():
    """
    API endpoint to save user phone number and location.
    """
    data = request.json

 
    phone = data.get('phoneNumber')
    location = data.get('location')
    if not phone or not location:
        return jsonify({'error': 'Phone number and location are required.'}), 400

    try:

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
    app.run(debug=True)
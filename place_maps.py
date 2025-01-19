from flask import Flask, jsonify
from pymongo import MongoClient
from flask_cors import CORS






app = Flask(__name__)
CORS(app)


mongo_uri = "mongodb+srv://nwhacksuser:nwhackspassword@nwhacks.nmgdk.mongodb.net/?retryWrites=true&w=majority&appName=nwhacks"
client = MongoClient(mongo_uri)
db = client['wildfires']
coordinates_collection = db['coordinates']


@app.route('/api/fires', methods=['GET'])
def get_fires():
   try:
       fire_data = [
           [doc['longitude'], doc['latitude']]
           for doc in coordinates_collection.find({}, {"_id": 0, "latitude": 1, "longitude": 1})
       ]
       return jsonify(fire_data)
   except Exception as e:
       return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
   app.run(debug=True)



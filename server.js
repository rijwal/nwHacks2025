const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const { MongoClient } = require('mongodb');

// MongoDB connection URI
const mongoUri = "mongodb+srv://nwhacksuser:nwhackspassword@nwhacks.nmgdk.mongodb.net/?retryWrites=true&w=majority&appName=nwhacks";

// Initialize Express app
const app = express();
const PORT = 3000;

// Middleware
app.use(cors()); // Enable CORS for all origins
app.use(bodyParser.json()); // Parse JSON request bodies

// MongoDB connection
let db, usersCollection;
MongoClient.connect(mongoUri, { useUnifiedTopology: true })
    .then(client => {
        console.log("Connected to MongoDB");
        db = client.db("wildfires"); // Replace with your database name
        usersCollection = db.collection("users"); // Replace with your collection name
    })
    .catch(error => {
        console.error("MongoDB connection failed:", error);
        process.exit(1);
    });

// Preflight OPTIONS request handling
app.options('*', cors());

// Endpoint to handle user data submission
app.post('/save-user-data', (req, res) => {
    console.log("Incoming Request Body:", req.body);

    const { phoneNumber, location } = req.body;

    // Validate request data
    if (!phoneNumber || !location) {
        console.error("Missing phoneNumber or location:", req.body);
        return res.status(400).json({ error: "Phone number and location are required." });
    }

    const userData = {
        phoneNumber,
        location,
        timestamp: new Date(),
    };

    // Store data in MongoDB
    usersCollection.insertOne(userData)
        .then(result => {
            console.log("Data successfully stored:", result);
            res.status(201).json({ message: "User data stored successfully!" });
        })
        .catch(error => {
            console.error("Database insertion error:", error);
            res.status(500).json({ error: "Failed to store user data." });
        });
});

// Start server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
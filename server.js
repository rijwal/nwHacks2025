const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");

const app = express();
const PORT = 3000;

// Middleware
app.use(cors());
app.use(express.json()); // To parse JSON bodies

// MongoDB connection
const mongoURI = "mongodb+srv://nwhacksuser:nwhackspassword@nwhacks.nmgdk.mongodb.net/?retryWrites=true&w=majority&appName=nwhacks"; // Replace with your URI
mongoose.connect(mongoURI, { useNewUrlParser: true, useUnifiedTopology: true });

const userSchema = new mongoose.Schema({
    phoneNumber: { type: String, required: true },
    location: {
        latitude: { type: Number, required: true },
        longitude: { type: Number, required: true }
    }
});

const User = mongoose.model("User", userSchema);

// API to save user data
app.post("/save-user-data", async (req, res) => {
    const { phoneNumber, location } = req.body;

    if (!phoneNumber || !location || !location.latitude || !location.longitude) {
        return res.status(400).json({ error: "Phone number and valid location are required." });
    }

    try {
        const newUser = new User({
            phoneNumber,
            location
        });

        const savedUser = await newUser.save();
        res.status(201).json({ message: "User data saved successfully!", userId: savedUser._id });
    } catch (error) {
        console.error("Error saving user data:", error);
        res.status(500).json({ error: "Internal Server Error" });
    }
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});

app.get("/", (req, res) => {
    res.send("Welcome to the Wildfire API!");
});
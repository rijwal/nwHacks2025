const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");

const app = express();
const PORT = 3000;

// Middleware
app.use(cors());

// MongoDB connection
const mongoURI = "mongodb+srv://nwhacksuser:nwhackspassword@nwhacks.nmgdk.mongodb.net/?retryWrites=true&w=majority&appName=nwhacks"; // Replace with your URI
mongoose.connect(mongoURI, { useNewUrlParser: true, useUnifiedTopology: true });

const wildfireSchema = new mongoose.Schema({
    latitude: Number,
    longitude: Number,
});

const Wildfire = mongoose.model("Wildfire", wildfireSchema);

// API to get wildfire data
app.get("/wildfires", async (req, res) => {
    try {
        const wildfires = await Wildfire.find({});
        res.json(wildfires);
    } catch (err) {
        console.error("Error fetching wildfires:", err);
        res.status(500).json({ error: "Internal Server Error" });
    }
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
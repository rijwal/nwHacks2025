// Replace with your actual API keys
const ambeeApiKey = 'c5d1cbd954309bf235a0a6709af2d84a4b08711f79fb3107bb64eb007aa523b8';
const mapboxAccessToken = 'pk.eyJ1IjoicnNhbmdleSIsImEiOiJjbTYybnd1Z2IxMjR3MmxvdThzMHRxejBjIn0.FHJ1aQP5xd0N0t5rg9F8oQ';

// Initialize the Mapbox map
mapboxgl.accessToken = mapboxAccessToken;
const map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v11',
    center: [-125.0, 54.0], // Centered on British Columbia
    zoom: 5
});

// Define the geographical boundaries of British Columbia
const north = 60.0;
const south = 48.3;
const east = -114.0;
const west = -139.0;

// Fetch wildfire data from Ambee
fetch('https://api.ambeedata.com/latest/fire', {
    method: 'GET',
    headers: {
        'x-api-key': ambeeApiKey,
        'Content-type': 'application/json'
    }
})
.then(response => response.json())
.then(data => {
    data.data.forEach(fire => {
        const { latitude, longitude, confidence } = fire;
        // Check if the fire is within British Columbia boundaries
        if (latitude >= south && latitude <= north && longitude >= west && longitude <= east) {
            // Add a marker to the map
            new mapboxgl.Marker({ color: 'red' })
                .setLngLat([longitude, latitude])
                .setPopup(new mapboxgl.Popup().setHTML(`<strong>Confidence:</strong> ${confidence}`))
                .addTo(map);
        }
    });
})
.catch(error => console.error('Error fetching wildfire data:', error));
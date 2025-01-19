WildCan - nwHacks Project 2025

As a team of first-year students at the University of British Columbia, hacking at our first major hackathon, we set out to create a project with real impact. After countless hours of hard work, determination, and many hours of sleep sacrificed, we are proud to present WildCan!

What It Does

WildCan collects real-time data about wildfires of all sizes and integrates it into our dynamic data map. Using advanced parameters, the application calculates the potential impact radius of each fire. If a wildfire is detected near a user or within a predefined impact distance, WildCan instantly sends a notification to their phone. This ensures users are always aware of nearby threats and can take action to stay safe.

To personalize alerts, we collect user data, such as location and phone numbers, ensuring accurate notifications. Additionally, we’ve included a donate page linking to a wildfire relief fund, so if our application inspires users to help, they can easily contribute to ongoing relief efforts.

Getting Started

Prerequisites

Node.js and npm installed

Python installed with necessary dependencies

Installation

Clone the repository:

git clone <repository-url>
cd wildcan

Install Node.js dependencies:

npm install

Start the server:

npm start

Run the Python scripts:

python place_maps.py & python notify.py

Open the application in your web browser:

http://127.0.0.1:5501/index.html

Features

Real-Time Data Collection: Monitors wildfire activity and provides up-to-date information.

Impact Radius Calculation: Dynamically determines the potential impact of each fire.

Personalized Notifications: Alerts users based on their location and proximity to active wildfires.

Donation Integration: Includes a link to a wildfire relief fund for users who wish to contribute.

Contribution

We welcome contributions from the community to improve WildCan. To get started:

Fork the repository.

Create a new branch for your feature or bug fix.

Submit a pull request describing your changes.



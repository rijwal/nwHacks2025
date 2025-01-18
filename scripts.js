document.addEventListener("DOMContentLoaded", () => {
    const tabs = document.querySelectorAll(".tab");
    const content = document.querySelector(".content");
    const currentPath = window.location.pathname.split("/").pop();

    // Highlight active tab
    tabs.forEach((tab) => {
        if (tab.getAttribute("href") === currentPath) {
            tab.classList.add("active");
        } else {
            tab.classList.remove("active");
        }
    });

    const fetchData = async () => {
        try {
            const response = await fetch("https://api.ambeedata.com/fire/latest/by-place?place=Los Angeles, CA", {
                headers: {
                    "x-api-key": "c5d1cbd954309bf235a0a6709af2d84a4b08711f79fb3107bb64eb007aa523b8",
                },
            });
    
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
    
            const data = await response.json();
            return data;
        } catch (error) {
            console.error("Error fetching data:", error);
            content.innerHTML = "<p>Failed to load data. Please try again later.</p>";
        }
    };

    const displayData = async () => {
        content.innerHTML = "<p>Loading data...</p>"; // Show loading message
        const data = await fetchData(); // Fetch data
    
        if (data && data.data) {
            content.innerHTML = ""; // Clear the loading message
            data.data.forEach((fire) => {
                const fireElement = document.createElement("div");
                fireElement.classList.add("fire-item");
                fireElement.setAttribute("aria-label", `Fire at latitude ${fire.latitude}, longitude ${fire.longitude}, confidence ${fire.confidence}%`);
                fireElement.innerHTML = `
                    <p><strong>Latitude:</strong> ${fire.latitude}</p>
                    <p><strong>Longitude:</strong> ${fire.longitude}</p>
                    <p><strong>Confidence:</strong> ${fire.confidence}</p>
                `;
                content.appendChild(fireElement); // Append to content container
            });
        } else {
            content.innerHTML = "<p>No data available at the moment.</p>";
        }
    };

    // Run displayData only on the homepage
    if (currentPath === "index.html") {
        displayData();
    }
});
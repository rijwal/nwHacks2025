document.addEventListener("DOMContentLoaded", () => {
    const sectionLinks = document.querySelectorAll(".section-link");

    sectionLinks.forEach((link) => {
        link.addEventListener("click", (e) => {
            e.preventDefault();
            const targetId = link.getAttribute("href").substring(1);
            const targetSection = document.getElementById(targetId);

            // Smooth scroll to the section
            window.scrollTo({
                top: targetSection.offsetTop - 80, // Offset for sticky navbar
                behavior: "smooth",
            });
        });
    });
});

document.addEventListener("DOMContentLoaded", () => {
    const donateButton = document.getElementById("donateButton");
    const transactionSummary = document.getElementById("transactionSummary");

    donateButton.addEventListener("click", () => {
        // Get form values
        const name = document.getElementById("name").value;
        const email = document.getElementById("email").value;
        const amount = document.getElementById("amount").value;

        // Validate input
        if (!name || !email || !amount || amount <= 0) {
            alert("Please fill out all fields and enter a valid amount.");
            return;
        }

        // Display transaction summary
        document.getElementById("summaryName").textContent = name;
        document.getElementById("summaryEmail").textContent = email;
        document.getElementById("summaryAmount").textContent = amount;

        transactionSummary.style.display = "block";

        // Optionally reset the form
        document.getElementById("donationForm").reset();
    });
});
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
});
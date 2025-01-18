document.addEventListener("DOMContentLoaded", () => {
    const tabs = document.querySelectorAll(".tab");
    const currentPath = window.location.pathname.split("/").pop();

    tabs.forEach((tab) => {
      
        if (tab.getAttribute("href") === currentPath) {
            tab.classList.add("active");
        } else {
            tab.classList.remove("active");
        }
    });
});
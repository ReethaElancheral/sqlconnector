document.addEventListener("DOMContentLoaded", () => {
    const timeBadge = document.getElementById("time-badge");

    async function updateTime() {
        try {
            const res = await fetch("/api/time");
            const data = await res.json();
            timeBadge.textContent = data.time;

            // Simple animation effect
            timeBadge.classList.remove("bg-success");
            void timeBadge.offsetWidth; // trigger reflow
            timeBadge.classList.add("bg-success");

        } catch(err) {
            console.error(err);
            timeBadge.textContent = "Error";
        }
    }

    // Update every second
    updateTime(); // initial load
    setInterval(updateTime, 1000);
});

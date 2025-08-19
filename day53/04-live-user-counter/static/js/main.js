let previousCount = parseInt(document.getElementById("user-count").textContent);

async function fetchUserCount() {
    try {
        const res = await fetch("/api/users/count");
        const data = await res.json();
        const count = data.count;

        // Update badge
        document.getElementById("user-count").textContent = count;

        // Show flash alert if new users joined
        if (count > previousCount) {
            const diff = count - previousCount;
            showAlert(`${diff} new user(s) joined!`);
        }

        previousCount = count;
    } catch (err) {
        console.error("Error fetching user count:", err);
    }
}

// Poll every 5 seconds
setInterval(fetchUserCount, 5000);

function showAlert(message) {
    const alertContainer = document.getElementById("alert-container");
    const alert = document.createElement("div");
    alert.className = "alert alert-success";
    alert.textContent = message;
    alertContainer.appendChild(alert);

    // Remove alert after 3 seconds
    setTimeout(() => alert.remove(), 3000);
}

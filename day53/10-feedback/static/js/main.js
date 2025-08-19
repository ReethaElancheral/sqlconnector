document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("feedback-form");
    const nameInput = document.getElementById("name");
    const messageInput = document.getElementById("message");
    const alertContainer = document.getElementById("alert-container");
    const feedbackList = document.getElementById("feedback-list");

    // Load existing feedbacks
    async function loadFeedbacks() {
        const res = await fetch("/api/feedbacks");
        const data = await res.json();
        feedbackList.innerHTML = "";
        data.forEach(fb => {
            const li = document.createElement("li");
            li.className = "list-group-item";
            li.textContent = `${fb.name}: ${fb.message}`;
            feedbackList.appendChild(li);
        });
    }

    loadFeedbacks();

    function showAlert(msg, type="success") {
        const alert = document.createElement("div");
        alert.className = `alert alert-${type} mt-2`;
        alert.textContent = msg;
        alertContainer.appendChild(alert);
        setTimeout(() => alert.remove(), 3000);
    }

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const name = nameInput.value.trim();
        const message = messageInput.value.trim();
        if(!name || !message) return showAlert("Please fill all fields", "danger");

        try {
            const res = await fetch("/api/feedback", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({name, message})
            });
            const data = await res.json();
            if(data.status === "success") {
                showAlert(data.message);
                form.reset();
                loadFeedbacks();
            } else {
                showAlert(data.message, "danger");
            }
        } catch(err) {
            console.error(err);
            showAlert("Error submitting feedback", "danger");
        }
    });
});

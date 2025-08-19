document.addEventListener("DOMContentLoaded", () => {
    const voteButtons = document.querySelectorAll(".vote-btn");
    const ctx = document.getElementById("resultsChart").getContext("2d");
    let chart;

    async function loadChart() {
        const data = await fetchPoll();
        const labels = Object.keys(data.options);
        const values = Object.values(data.options);

        chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Votes',
                    data: values,
                    backgroundColor: ['#007bff','#28a745','#dc3545','#ffc107']
                }]
            },
            options: {
                responsive: true,
                scales: { y: { beginAtZero: true } }
            }
        });
    }

    async function fetchPoll() {
        const res = await fetch("/api/poll");
        return res.json();
    }

    async function updateChart() {
        const data = await fetchPoll();
        chart.data.datasets[0].data = Object.values(data.options);
        chart.update();
    }

    function showAlert(msg, type="success") {
        const container = document.getElementById("alert-container");
        const alert = document.createElement("div");
        alert.className = `alert alert-${type} mt-2`;
        alert.textContent = msg;
        container.appendChild(alert);
        setTimeout(() => alert.remove(), 3000);
    }

    voteButtons.forEach(btn => {
        btn.addEventListener("click", async () => {
            const option = btn.dataset.option;
            try {
                const res = await fetch("/api/vote", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({option})
                });
                const data = await res.json();
                if(data.status === "success") {
                    showAlert(`You voted for ${option}`);
                    updateChart();
                } else {
                    showAlert(data.message, "danger");
                }
            } catch(err) {
                console.error(err);
                showAlert("Error sending vote", "danger");
            }
        });
    });

    // Load chart initially
    loadChart();
});

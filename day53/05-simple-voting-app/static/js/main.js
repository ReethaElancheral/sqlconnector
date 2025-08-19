document.addEventListener("DOMContentLoaded", () => {

    const voteButtons = document.querySelectorAll(".vote-btn");

    voteButtons.forEach(btn => {
        btn.addEventListener("click", async () => {
            const candidate = btn.dataset.candidate;
            try {
                const res = await fetch("/api/vote", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({candidate})
                });
                const data = await res.json();
                if(data.status === "success") {
                    showAlert(`You voted for ${candidate}`);
                    updateBars();
                } else {
                    showAlert(data.message, "danger");
                }
            } catch(err) {
                console.error(err);
            }
        });
    });

    async function updateBars() {
        try {
            const res = await fetch("/api/results");
            const results = await res.json();
            const totalVotes = Object.values(results).reduce((a,b)=>a+b,0) || 1;

            for(const candidate in results){
                const candidateId = candidate.replace(/ /g, "_");
                const bar = document.getElementById(`bar-${candidateId}`);
                const percent = Math.round((results[candidate]/totalVotes)*100);
                bar.style.width = percent + "%";
                bar.textContent = `${results[candidate]} votes`;
            }
        } catch(err){
            console.error(err);
        }
    }

    function showAlert(msg, type="success"){
        const container = document.getElementById("alert-container");
        const alert = document.createElement("div");
        alert.className = `alert alert-${type} mt-2`;
        alert.textContent = msg;
        container.appendChild(alert);
        setTimeout(()=> alert.remove(),3000);
    }

    // Initial load
    updateBars();
});

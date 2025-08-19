document.addEventListener("DOMContentLoaded", () => {
    const suggestBtn = document.getElementById("suggest-btn");
    const modalBody = document.getElementById("modal-body");
    const bookModal = new bootstrap.Modal(document.getElementById('bookModal'));

    suggestBtn.addEventListener("click", async () => {
        modalBody.textContent = "Loading...";
        bookModal.show();
        try {
            const res = await fetch("/api/book/suggest");
            const book = await res.json();
            modalBody.innerHTML = `
                <p><strong>Title:</strong> ${book.title}</p>
                <p><strong>Author:</strong> ${book.author}</p>
                <p><strong>Year:</strong> ${book.year}</p>
            `;
        } catch(err) {
            console.error(err);
            modalBody.textContent = "Error fetching book suggestion.";
        }
    });
});

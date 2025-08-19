document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("search-input");
    const container = document.getElementById("products-container");
    const loading = document.getElementById("loading");

    async function fetchProducts(query="") {
        loading.style.display = "block";
        const res = await fetch(`/api/products?q=${query}`);
        const data = await res.json();
        loading.style.display = "none";
        renderProducts(data);
    }

    function renderProducts(products) {
        container.innerHTML = "";
        if(products.length === 0){
            container.innerHTML = "<p>No products found.</p>";
            return;
        }
        products.forEach(p => {
            const card = document.createElement("div");
            card.className = "col-md-3 mb-3";
            card.innerHTML = `
                <div class="card h-100">
                    <div class="card-body">
                        <h5 class="card-title">${p.name}</h5>
                        <p class="card-text">Price: ₹${p.price}</p>
                        <p class="card-text">${p.in_stock ? 'In Stock' : 'Out of Stock'}</p>
                    </div>
                </div>
            `;
            container.appendChild(card);
        });
    }

    // Initial load
    fetchProducts();

    // Live search
    input.addEventListener("input", () => {
        const query = input.value.trim();
        fetchProducts(query);
    });
});

// Helpers
async function addToCart(productId, quantity=1) {
  const res = await fetch('/api/cart/add', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ product_id: productId, quantity })
  });
  if (!res.ok) throw new Error('Failed to add to cart');
  return res.json();
}

async function updateCartItem(itemId, quantity) {
  const res = await fetch(`/api/cart/item/${itemId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ quantity })
  });
  if (!res.ok) throw new Error('Failed to update cart item');
  return res.json();
}

async function deleteCartItem(itemId) {
  const res = await fetch(`/api/cart/item/${itemId}`, { method: 'DELETE' });
  if (!res.ok) throw new Error('Failed to delete cart item');
  return res.json();
}

function bumpCartCount() {
  const badge = document.getElementById('cart-count');
  if (!badge) return;
  const n = parseInt(badge.textContent || '0', 10) + 1;
  badge.textContent = String(n);
}

document.addEventListener('click', async (e) => {
  const btn = e.target.closest('.add-to-cart');
  if (btn) {
    const id = parseInt(btn.dataset.productId, 10);
    try {
      await addToCart(id, 1);
      bumpCartCount();
    } catch (err) {
      alert('Error: ' + err.message);
    }
  }
});

// Cart page quantity listeners
window.addEventListener('DOMContentLoaded', () => {
  const rows = document.querySelectorAll('tr[data-item-id]');
  rows.forEach((row) => {
    const itemId = row.getAttribute('data-item-id');
    const qtyInput = row.querySelector('.qty-input');
    const removeBtn = row.querySelector('.remove-item');
    if (qtyInput) {
      qtyInput.addEventListener('change', async () => {
        const qty = parseInt(qtyInput.value || '1', 10);
        try {
          await updateCartItem(itemId, qty);
          location.reload();
        } catch (err) {
          alert('Error: ' + err.message);
        }
      });
    }
    if (removeBtn) {
      removeBtn.addEventListener('click', async () => {
        try {
          await deleteCartItem(itemId);
          location.reload();
        } catch (err) {
          alert('Error: ' + err.message);
        }
      });
    }
  });
});

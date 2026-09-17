function showFlash(message, type = 'info') {
    const list = document.getElementById('flash-messages');
    if (!list) return;
    const li = document.createElement('li');
    li.className = type;
    li.textContent = message;
    list.appendChild(li);
    setTimeout(() => li.remove(), 4000);
}

function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str ?? '';
    return div.innerHTML;
}

async function loadCart() {
    const content = document.getElementById('cart-content');

    if (!Auth.isAuthenticated()) {
        content.innerHTML = `
            <div class="empty-cart">
                <div class="emoji">🔒</div>
                <p>Devi accedere per vedere il tuo carrello.</p>
                <a href="login.html">Accedi</a>
            </div>`;
        return;
    }

    try {
        const items = await apiJson('/cart/items');

        if (!items.length) {
            content.innerHTML = `
                <div class="empty-cart">
                    <div class="emoji">🫒</div>
                    <p>Il tuo carrello è vuoto.</p>
                    <a href="index.html">Sfoglia i prodotti</a>
                </div>`;
            return;
        }

        const itemsHtml = items.map((item) => `
            <div class="cart-item">
                <div class="cart-item-icon">🫒</div>
                <div class="cart-item-info">
                    <h4>${escapeHtml(item.product.name)}</h4>
                    <p>€${Number(item.product.price).toFixed(2)} / bottiglia</p>
                </div>
                <span class="cart-item-qty">x${item.quantity}</span>
                <div class="cart-item-price">€${(item.product.price * item.quantity).toFixed(2)}</div>
            </div>
        `).join('');

        const total = items.reduce((sum, item) => sum + item.product.price * item.quantity, 0);

        content.innerHTML = `
            <div class="cart-list">${itemsHtml}</div>
            <div class="cart-summary">
                <div class="cart-summary-row">
                    <span>Articoli</span>
                    <span>${items.reduce((n, i) => n + i.quantity, 0)}</span>
                </div>
                <div class="cart-summary-row total">
                    <span>Totale</span>
                    <span>€${total.toFixed(2)}</span>
                </div>
                <button class="btn-checkout" id="btn-checkout">✔ Completa l'Ordine</button>
            </div>`;

        document.getElementById('btn-checkout').addEventListener('click', checkout);
    } catch (err) {
        content.innerHTML = `
            <div class="empty-cart">
                <div class="emoji">⚠️</div>
                <p>Impossibile caricare il carrello (${escapeHtml(err.message)}).</p>
            </div>`;
    }
}

async function checkout() {
    const btn = document.getElementById('btn-checkout');
    btn.disabled = true;
    btn.textContent = 'Elaborazione ordine...';
    try {
        const order = await apiJson('/orders/checkout?payment_provider=stripe', { method: 'POST' });
        showFlash(`Ordine #${order.id} completato! Totale: €${Number(order.total_amount).toFixed(2)}`, 'success');
        setTimeout(loadCart, 800);
    } catch (err) {
        showFlash(`Errore durante il checkout: ${err.message}`, 'error');
        btn.disabled = false;
        btn.textContent = "✔ Completa l'Ordine";
    }
}

document.addEventListener('DOMContentLoaded', loadCart);

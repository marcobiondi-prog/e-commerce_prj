function showFlash(message, type = 'info') {
    const list = document.getElementById('flash-messages');
    if (!list) return;
    const li = document.createElement('li');
    li.className = type;
    li.textContent = message;
    list.appendChild(li);
    setTimeout(() => li.remove(), 4000);
}

function productCardHtml(product) {
    const loggedIn = Auth.isAuthenticated();
    const outOfStock = product.stock_quantity === 0;

    const imgBlock = product.image_url
        ? `<img src="${product.image_url}" alt="${escapeHtml(product.name)}">`
        : '🫒';

    let actionBlock;
    if (loggedIn) {
        actionBlock = `
            <button class="btn-add-cart" data-product-id="${product.id}" ${outOfStock ? 'disabled' : ''}>
                ${outOfStock ? 'Esaurito' : '🛒 Aggiungi al Carrello'}
            </button>`;
    } else {
        actionBlock = `<p class="login-prompt"><a href="login.html">Accedi</a> per acquistare</p>`;
    }

    return `
        <div class="product-card" id="product-${product.id}">
            <div class="card-img-placeholder">${imgBlock}</div>
            <div class="card-body">
                <div class="card-tag">Olio Extra Vergine</div>
                <h3>${escapeHtml(product.name)}</h3>
                <p>${escapeHtml(product.description)}</p>
            </div>
            <div class="card-footer">
                <div class="price">€${Number(product.price).toFixed(2)}<span>/bottiglia</span></div>
                <span class="stock-badge">📦 ${product.stock_quantity} disponibili</span>
            </div>
            ${actionBlock}
        </div>`;
}

function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str ?? '';
    return div.innerHTML;
}

async function loadProducts(params = {}) {
    const grid = document.getElementById('product-grid');
    const countEl = document.getElementById('product-count');
    grid.innerHTML = `<div class="empty-state"><div class="emoji">🫒</div><p>Caricamento prodotti...</p></div>`;

    const query = new URLSearchParams();
    if (params.q) query.set('q', params.q);
    if (params.min_price) query.set('min_price', params.min_price);
    if (params.max_price) query.set('max_price', params.max_price);

    try {
        const products = await apiJson(`/products/?${query.toString()}`);
        countEl.textContent = `${products.length} prodotti`;

        if (!products.length) {
            grid.innerHTML = `
                <div class="empty-state">
                    <div class="emoji">🫒</div>
                    <p>Nessun prodotto trovato con questi filtri.</p>
                </div>`;
            return;
        }

        grid.innerHTML = products.map(productCardHtml).join('');

        grid.querySelectorAll('.btn-add-cart').forEach((btn) => {
            btn.addEventListener('click', () => addToCart(btn.dataset.productId, btn));
        });
    } catch (err) {
        grid.innerHTML = `
            <div class="empty-state">
                <div class="emoji">⚠️</div>
                <p>Impossibile caricare i prodotti (${escapeHtml(err.message)}).</p>
            </div>`;
    }
}

async function addToCart(productId, btn) {
    btn.disabled = true;
    const originalText = btn.textContent;
    btn.textContent = 'Aggiungo...';
    try {
        await apiJson('/cart/items', {
            method: 'POST',
            body: JSON.stringify({ product_id: Number(productId), quantity: 1 }),
        });
        showFlash('Prodotto aggiunto al carrello 🛒', 'success');
        btn.textContent = '✓ Aggiunto';
        setTimeout(() => { btn.textContent = originalText; btn.disabled = false; }, 1200);
    } catch (err) {
        showFlash(`Errore: ${err.message}`, 'error');
        btn.textContent = originalText;
        btn.disabled = false;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    loadProducts();

    const form = document.getElementById('search-form');
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        loadProducts({
            q: document.getElementById('search-input').value.trim(),
            min_price: document.getElementById('price-min').value,
            max_price: document.getElementById('price-max').value,
        });
    });
});

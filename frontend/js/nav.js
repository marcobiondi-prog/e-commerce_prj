function toggleMenu() {
    const nav = document.getElementById('nav-links');
    nav.classList.toggle('open');
}

function renderNav() {
    const slot = document.getElementById('nav-auth-slot');
    if (!slot) return;

    if (Auth.isAuthenticated()) {
        const email = localStorage.getItem('user_email') || 'utente';
        slot.innerHTML = `
            <li>
                <a href="cart.html" class="btn-cart" id="nav-cart">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/>
                        <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/>
                    </svg>
                    Carrello
                </a>
            </li>
            <li><span class="user-welcome">Ciao, ${email} 👋</span></li>
            <li><button type="button" class="btn-logout" id="nav-logout">Esci</button></li>
        `;
        document.getElementById('nav-logout').addEventListener('click', () => {
            Auth.clearToken();
            localStorage.removeItem('user_email');
            window.location.href = 'index.html';
        });
    } else {
        slot.innerHTML = `<li><a href="login.html" class="btn-login" id="nav-login">Accedi</a></li>`;
    }
}

document.addEventListener('DOMContentLoaded', renderNav);

// Base URL delle API FastAPI. Con Nginx configurato come da nginx.conf,
// il frontend e le API vivono sullo stesso host, quindi lasciamo vuoto
// per usare percorsi relativi (es. /products/, /auth/login, ...).
const API_BASE = '';

const Auth = {
    getToken() {
        return localStorage.getItem('access_token');
    },
    setToken(token) {
        localStorage.setItem('access_token', token);
    },
    clearToken() {
        localStorage.removeItem('access_token');
    },
    isAuthenticated() {
        return !!this.getToken();
    },
};

async function apiFetch(path, options = {}) {
    const headers = options.headers ? { ...options.headers } : {};
    const token = Auth.getToken();
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    const response = await fetch(`${API_BASE}${path}`, { ...options, headers });
    if (response.status === 401) {
        Auth.clearToken();
    }
    return response;
}

async function apiJson(path, options = {}) {
    const headers = options.headers ? { ...options.headers } : {};
    if (options.body && !(options.body instanceof URLSearchParams)) {
        headers['Content-Type'] = 'application/json';
    }
    const response = await apiFetch(path, { ...options, headers });
    let data = null;
    try {
        data = await response.json();
    } catch (e) {
        data = null;
    }
    if (!response.ok) {
        const message = (data && (data.detail || data.message)) || `Errore ${response.status}`;
        throw new Error(typeof message === 'string' ? message : JSON.stringify(message));
    }
    return data;
}

# Ecommerce — FastAPI + MySQL + Docker

Architettura a livelli (router → service → repository), con Nginx come
reverse proxy, MySQL come database relazionale, Redis come cache e come
broker per i task asincroni eseguiti da Celery.

## Struttura

```
.
├── docker-compose.yml
├── .env.example
├── nginx/
│   └── nginx.conf              # serve il frontend + reverse proxy verso FastAPI
├── frontend/                   # frontend statico (grafica identica al sito OLIO)
│   ├── index.html              # home con catalogo prodotti e filtri
│   ├── login.html / register.html
│   ├── cart.html                # carrello e checkout
│   ├── css/                    # stile "Oleificio d'Eccellenza" (verde/oro)
│   ├── js/                     # chiamate alle API (fetch + JWT)
│   └── images/                 # logo e banner del brand
└── api/
    ├── Dockerfile
    ├── requirements.txt
    └── app/
        ├── main.py             # entrypoint FastAPI
        ├── config.py           # settings da variabili d'ambiente
        ├── database.py         # engine SQLAlchemy async + Unit of Work
        ├── dependencies.py     # dependency injection (utente autenticato)
        ├── api/routes/         # router layer: HTTP + validazione
        ├── schemas/            # Pydantic DTO (input/output API)
        ├── models/             # modelli ORM SQLAlchemy
        ├── repositories/       # accesso dati (Repository pattern)
        ├── services/           # logica di business
        │   └── payment.py      # Strategy pattern per i provider di pagamento
        ├── core/                # security (JWT, hashing), cache Redis
        └── tasks/               # Celery app + task in background
```

## Avvio

```bash
cp .env.example .env
docker compose up --build
```

- Sito (frontend): http://localhost/
- API: http://localhost/products
- Documentazione interattiva: http://localhost/docs

## Frontend

Il frontend è statico (HTML/CSS/JS, nessun framework/build step) e riprende
la stessa identità grafica del sito Django "Oleificio d'Eccellenza"
(https://github.com/lorenzomastandrea-create/OLIO): stessa palette
verde/oro, stessi font (Cormorant Garamond + Inter), stessa navbar, hero
banner e griglia prodotti. Parla con il backend FastAPI via `fetch`,
usando il token JWT restituito da `/auth/login` (salvato in
`localStorage`) per le richieste autenticate a `/cart` e `/orders`.

Nginx serve i file di `frontend/` sulla root `/` e fa da reverse proxy
solo per le rotte `/auth`, `/products`, `/cart`, `/orders`, `/docs`,
`/redoc`, `/openapi.json` e `/health` verso FastAPI.

## Note

- `api` e `worker` condividono la stessa immagine Docker: stesso codice,
  comando diverso (`uvicorn` vs `celery worker`).
- Le tabelle non vengono create automaticamente: aggiungere Alembic per le
  migrazioni prima di andare in produzione.
- `payment.py` mostra lo Strategy pattern: aggiungere un nuovo provider di
  pagamento non richiede modifiche a `OrderService`.

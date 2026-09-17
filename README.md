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
│   └── nginx.conf              # reverse proxy davanti a FastAPI
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

- API: http://localhost/products
- Documentazione interattiva: http://localhost/docs

## Note

- `api` e `worker` condividono la stessa immagine Docker: stesso codice,
  comando diverso (`uvicorn` vs `celery worker`).
- Le tabelle non vengono create automaticamente: aggiungere Alembic per le
  migrazioni prima di andare in produzione.
- `payment.py` mostra lo Strategy pattern: aggiungere un nuovo provider di
  pagamento non richiede modifiche a `OrderService`.

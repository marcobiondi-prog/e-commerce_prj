from app.tasks.celery_app import celery_app


@celery_app.task(name="app.tasks.email_tasks.send_order_confirmation")
def send_order_confirmation(order_id: int) -> None:
    """Task eseguito dal worker Celery, fuori dal ciclo richiesta/risposta
    dell'API (Producer/Consumer pattern)."""
    # qui la vera integrazione con un provider email (SES, SendGrid, ecc.)
    print(f"[worker] Sending confirmation email for order {order_id}")

from celery import Celery

from app.config import settings

celery_app = Celery(
    "ecommerce",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["app.tasks.email_tasks"],
)

celery_app.conf.task_routes = {
    "app.tasks.email_tasks.*": {"queue": "emails"},
}

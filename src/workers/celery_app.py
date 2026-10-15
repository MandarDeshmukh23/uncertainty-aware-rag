from celery import Celery
from src.core.config import settings

# Initialize the Celery app, pointing it to our RabbitMQ broker
celery_app = Celery(
    "rag_worker",
    broker=settings.celery_broker_url,
    include=["src.workers.tasks"]
)

# Optional: configure worker prefetch limits for better load balancing
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    worker_prefetch_multiplier=1 # Ensures workers only take 1 task at a time
)
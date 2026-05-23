import os
from celery import Celery

# Set default settings module for Celery
# If you are using pydantic-settings, you can load env variables from .env
# For now, we'll use a standard Redis broker config, defaulting to localhost if not found in env
redis_url = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "worker",
    broker=redis_url,
    backend=redis_url,
    include=["app.tasks.clasificacion_tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    # Configure task routing if necessary
    # task_routes={
    #     "app.tasks.clasificacion_tasks.*": {"queue": "clasificacion"},
    # }
)

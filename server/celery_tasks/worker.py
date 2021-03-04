from celery import Celery


from app.factory import create_app
from celery_tasks.celery import configure_celery

celery: Celery = configure_celery(create_app())
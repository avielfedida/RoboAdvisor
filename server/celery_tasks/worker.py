from celery import Celery


from server.app.factory import create_app
from server.celery_tasks.celery import configure_celery

celery: Celery = configure_celery(create_app())
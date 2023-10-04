# celery_app.py
from celery import Celery

from . import celery_config

celery_app = Celery("plagd_app")
celery_app.config_from_object(celery_config)

import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ya_booker.settings")
app = Celery("ya_booker")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

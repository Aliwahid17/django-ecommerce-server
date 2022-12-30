from __future__ import absolute_import
import os
from celery import Celery
from core.settings import INSTALLED_APPS
import env

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')


# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
# app.autodiscover_tasks()
app.autodiscover_tasks(lambda: INSTALLED_APPS)
app.conf.enable_utc = False
app.conf.update(timezone="Asia/Kolkata",
                broker_url=os.environ.get("REDIS_URL"),
                result_backend=os.environ.get('POSTGRESQL_URL'),
                task_track_started=True,
                CELERY_TASK_TIME_LIMIT=30 * 60,
                result_serializer="json",
                accept_content=['application/json'],
                CELERY_RESULT_EXTENDED=True,
                )


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

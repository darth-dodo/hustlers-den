from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
from den.settings.base import get_env_variable

os.environ.setdefault('DJANGO_SETTINGS_MODULE', get_env_variable('DJANGO_SETTINGS_MODULE'))
app = Celery("den")

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()



@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


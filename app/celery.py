import datetime
import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
app = Celery('app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'print-message-five-seconds': {
        'task': 'pokedex.tasks.refresh_pokedex',
        'schedule': datetime.timedelta(hours=24)
    }
}
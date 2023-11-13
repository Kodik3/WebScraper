import os
from celery import Celery
from celery.schedules import crontab
# Django
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.base')

app = Celery('web_scraper')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.PROJECT_APPS)

app.conf.beat_schedule = {
    'every-1-week-every-day': {
        'task': 'clearing-old-queries',
        'schedule': crontab(day_of_week='*/1')
    }
}
app.conf.timezone = 'UTC'


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """
    выводит информацию о запросе, когда задача выполняется.
    """
    print(f'Request: {self.request!r}')
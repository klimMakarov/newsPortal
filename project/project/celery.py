import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('news')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    # 'print_every_5_seconds': {
    #     'task': 'news.tasks.printer',
    #     'schedule': 5,
    #     'args': (5,),
    # },
    'weekly_digest_monday_8am': {
        'task': 'news.tasks.send_weekly_digest',
        # 'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        'schedule': crontab(),
    }
}
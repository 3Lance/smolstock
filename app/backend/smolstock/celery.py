from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smolstock.settings')

app = Celery('smolstock')
app.conf.enable_utc = False
app.conf.update(timezone = 'Asia/Kolkata')
app.config_from_object(settings, namespace='CELERY')

#CELERY BEAT SETTINGS
app.conf.beat_schedule = {
   'delete_sign_up_users': {
        'task': 'Authentication.tasks.delete_sign_up_users',
        'schedule': crontab(minute ='*/15'),
    },
   'delete_email_otps': {
        'task': 'Authentication.tasks.delete_email_otps',
        'schedule': crontab(minute ='*/5'),
    },
   'delete_sms_otps': {
        'task': 'Authentication.tasks.delete_sms_otps',
        'schedule': crontab(minute ='*/2'),
    },
    # 'update_coins_data': {
    #     'task': 'Investments.tasks.update_coins',
    #     'schedule': 10,
    # },
    'update_news_database': {
        'task': 'Investments.tasks.update_news',
        'schedule': crontab(hour ='*/3'),
    },
}

app.autodiscover_tasks()

@app.task(bind = True)
def debug_task(self):
    print(f'Request: {self.request!r}')
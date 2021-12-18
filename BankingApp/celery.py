from __future__ import absolute_import, unicode_literals

import os
from celery import Celery
#from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BankingApp.settings')

app = Celery("BankingApp",
	broker="redis://localhost:6379",
	backend="db+sqlite:///results.db")
#app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task
def multiply(a,b):
	return a*b

@app.task(bind=True)
def debug_task(self):
	print('Request: {0!r}'.format(self.request))
# -*- coding: utf-8 -*-
# author: zltningx

import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dragonM.settings')

app = Celery('dragonM')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.task_routes = ([
    ('apps.backend.tasks.*', {
        'queue': 'backend'
    }),
    ('apps.vulmannager.tasks.*', {
        'queue': 'vulmannager'
    }),
], )

app.set_current()

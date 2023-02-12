from celery import Celery

# Create your celeries here.

app = Celery("project_03v2")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
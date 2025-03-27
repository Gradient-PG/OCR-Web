import os
from celery import Celery, current_task

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379')
celery.conf.result_backend = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379')

@celery.task(name='create_task')
def create_task(taskEntityDict: dict):
    """Executes a task based on the taskEntity."""
    task_id = current_task.request.id
    # Simulate task logic here
    result = {"task_id": task_id, "status": "completed"}
    return result
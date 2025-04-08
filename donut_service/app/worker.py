import os
import time
import logging
from celery import Celery, current_task
from datetime import datetime, timezone
from app.entity.task import DATEFORMAT
from app.services.image import ImageService
from app.repository.mongodb.image import ImageRepository

logger = logging.getLogger(__name__)

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get('CELERY_BROKER_URL', 'redis://redis:6379/0')
celery.conf.result_backend = os.environ.get('CELERY_RESULT_BACKEND', 'redis://redis:6379/0')

image_repositiry = ImageRepository()
image_service = ImageService(image_repositiry)

@celery.task(name='create_task')
def create_task(args: dict):
    """Executes a task based on the TaskEntity."""

    task_id = current_task.request.id
    logger.info(f"Task {task_id} started with args: {args}")
    start_time = datetime.now(timezone.utc).strftime(DATEFORMAT)
    current_task.update_state(state='STARTED', meta={"start_time": start_time, "task_type": args.get("task_type")})

    try:
        # Simulate task logic here
        time.sleep(10)  
        end_time = datetime.now(timezone.utc).strftime(DATEFORMAT)
        result = {
            "task_id": task_id,
            "status": "completed",
            "start_time": start_time,
            "end_time": end_time,
            "output": {"message": "Task completed successfully"}
        }
        logger.info(f"Task {task_id} completed successfully")
        return result
    except Exception as e:
        logger.error(f"Task {task_id} failed: {str(e)}")
        current_task.update_state(state='FAILURE', meta={"error": str(e)})
        raise
    
@celery.task(name='augmentation_task')
def augmentation_task(image_codes: list):
    """Executes an augmentation task."""
    task_id = current_task.request.id
    logger.info(f"Augmentation task {task_id} started with {len(image_codes)} image codes")
    if not image_codes:
        raise ValueError("No image codes provided for augmentation task")
    
    
    start_time = datetime.now(timezone.utc).strftime(DATEFORMAT)
    current_task.update_state(state='STARTED', meta={"start_time": start_time})

    try:
        
        # Simulate augmentation logic here
        time.sleep(10)  
        end_time = datetime.now(timezone.utc).strftime(DATEFORMAT)
        result = {
            "task_id": task_id,
            "status": "completed",
            "start_time": start_time,
            "end_time": end_time,
            "output": {"message": "Augmentation completed successfully"}
        }
        logger.info(f"Augmentation task {task_id} completed successfully")
        return result
    except Exception as e:
        logger.error(f"Augmentation task {task_id} failed: {str(e)}")
        current_task.update_state(state='FAILURE', meta={"error": str(e)})
        raise
    

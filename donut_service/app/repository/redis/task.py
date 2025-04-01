import os
import json
from redis import Redis

from celery.result import AsyncResult
from app.entity.task import TaskEntity, TaskStatus, TaskType

class TaskNotFoundException(Exception):
    """Custom exception for when a task is not found."""
    def __init__(self, task_id: str):
        super().__init__(f"Task with ID '{task_id}' does not exist.")

# python3 -c "from redis import Redis ; client=Redis.from_url('redis://localhost:6379') ; print(client.keys())"
class TaskRepository:
    """Class responsible for task records management in redis DB.

    Available methods include task retrieval
    """
    def __init__(self, redis_url: str = "redis://6379/0"):
        self.redis = Redis.from_url(redis_url)

    def get_task(self, task_id: str) -> TaskEntity:
        """Retrieve task information and return a TaskEntity."""
        task_result = AsyncResult(task_id)

        # Check if the task exists
        if not task_result:
            raise TaskNotFoundException(task_id)
        
        # Map Celery task status to TaskStatus enum
        status_mapping = {
            "PENDING": TaskStatus.PENDING,
            "STARTED": TaskStatus.IN_PROGRESS,
            "SUCCESS": TaskStatus.COMPLETED,
            "FAILURE": TaskStatus.FAILED,
            "REVOKED": TaskStatus.TIMEOUT,
        }
        task_status = status_mapping.get(task_result.status, TaskStatus.FAILED)
        
        result = task_result.result if task_result.result else {}
        meta = task_result.info if isinstance(task_result.info, dict) else {}
        return TaskEntity(
            id=task_id,
            start_time=meta.get("start_time", ""),
            end_time=result.get("end_time", ""),
            task_type=TaskType(meta.get("task_type")) if meta.get("task_type") else self.get_task_metadata(task_id).get("task_type"),
            status=task_status,
        )
        
    def get_task_metadata(self, task_id: str) -> dict:
        metadata = self.redis.get(f"task:{task_id}:metadata")
        return json.loads(metadata) if metadata else None
    
    def save_task_metadata(self, task_id: str, metadata: dict):
        self.redis.set(f"task:{task_id}:metadata", json.dumps(metadata))
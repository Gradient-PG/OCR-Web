import os

from celery.result import AsyncResult
from redis import Redis


# python3 -c "from redis import Redis ; client=Redis.from_url('redis://localhost:6379') ; print(client.keys())"
class TaskRepository:
    """Class responsible for task records management in redis DB.

    Available methods include task retrieval and updating task progress
    """

    def __init__(self):
        redis_url = os.environ.get(
            'CELERY_RESULT_BACKEND', 'redis://localhost:6379')
        self.client = Redis.from_url(redis_url)

    def get_task(self, task_id: str) -> dict | None:
        """IN: task_id

        OUT: {'task_id': task_id, 'status': task_result.status, 'result': task_result.result} | None
        """
        task_result = AsyncResult(task_id)
        progress = self.client.get(task_id)
        progress_value = progress if progress else 'Not started'

        return {
            'task_id': task_id,
            'status': task_result.status,
            'result': task_result.result,
            'progress': progress_value,
        } if task_result else None

    def update_task_progress(self, task_id: str, progress: str) -> dict | None:
        """Update progress of a task in redis

        task_id: str - id obtained upon task creation
        progress: str - progress in task completion
        """
        self.client.set(task_id, progress)
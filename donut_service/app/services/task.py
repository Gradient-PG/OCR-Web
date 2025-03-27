import logging

from ..entity.task import TaskEntity, TaskResult, TaskStatus
from ..repository.redis.task import TaskRepository
from ..worker import create_task as worker_create_task

DELAY = 60


class TaskService:
    """Provides an interface to work with tasks.

    Allows creating tasks, getting their status and results

    """
    # static field to be accessed from any instance
    # frameworks = {}

    def __init__(self):
        self.task_repository = TaskRepository()

    async def get_task(self, task_id: str) -> dict:
        """Retrieves task from the database.

        Args:
            task_id (str): The unique identifier of the task.

        Returns:
            dict: The task.
        """
        task = self.task_repository.get_task(task_id)
        return task

    async def get_task_status(self, task_id: str) -> TaskStatus:
        """Retrieves the status of a task from the database.

        Args:
            task_id (str): The unique identifier of the task.

        Returns:
            str: The current status of the task.
        """
        task = self.task_repository.get_task(task_id)
        return task['status']

    async def get_task_result(self, task_id: str) -> TaskResult | None:
        """Retrieves the result of a task from the database.

        Args:
            task_id (str): The unique identifier of the task.

        Returns:
            str: The result of the task.
        """
        task = self.task_repository.get_task(task_id)
        return task['result']

    async def create_task(self, taskEntity: TaskEntity) -> str:
        """Creates and queues a new task, writes the TaskEntity to redis.

        Returns:
            str: The unique identifier of the newly created task.
        """
        r = worker_create_task.delay(taskEntity.__dict__)
        task_id = r.task_id

        logging.info(f'{__file__} :: task id: {task_id}')
        return task_id
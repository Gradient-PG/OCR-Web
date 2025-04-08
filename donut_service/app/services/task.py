import logging

from ..entity.task import TaskEntity, TaskStatus, TaskType
from ..repository.redis.task import TaskRepository
from ..worker import augmentation_task as worker_augmentation_task
from typing import Any

DELAY = 60


class TaskService:
    """Provides an interface to work with tasks.

    Allows creating tasks, getting their status and results

    """

    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    async def get_task(self, task_id: str) -> TaskEntity:
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
        return task.status

    async def get_task_type(self, task_id: str) -> TaskType:
        """Retrieves the type of a task from the database.

        Args:
            task_id (str): The unique identifier of the task.

        Returns:
            str: The type of the task.
        """
        task = self.task_repository.get_task(task_id)
        return task.task_type

    async def create_task(self, task_type: str, args: Any) -> str:
        """Creates and queues a new task, writes the TaskEntity to redis.

        Returns:
            str: The unique identifier of the newly created task.
        """
        match task_type:
            case 'augmentation':
                r = worker_augmentation_task.delay({"image_codes": args})
            case _:
                raise ValueError(f"Unsupported task type: {task_type}")
    
    
        task_id = r.task_id
        self.task_repository.save_task_metadata(task_id, {"task_type": task_type})

        logging.info(f'{__file__} :: task id: {task_id}')
        return task_id
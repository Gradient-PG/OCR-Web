from dataclasses import dataclass
from enum import Enum
from typing import List

DATEFORMAT = '%Y-%m-%dT%H:%M:%S'

class TaskType(str, Enum):
    AUGMENTATION = 'augmentation'
    TRAINING = 'training'
    PREDICTION = 'prediction'

class TaskStatus(str, Enum):
    """Task status enum

    Implies state of the task, one of: PENDING, IN_PROGRESS, COMPLETED
    """
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    FAILED = 'failed'
    TIMEOUT = 'timeout'

@dataclass
class TaskEntity:
    """THIS MIGHT BE A BIT OUTDATED

    represents a text classification task
    mode, callable and args fields are necessary
    to create a celery coroutine to delegate the task
    """

    id: str | None
    start_time: str
    end_time: str | None = None
    task_type: TaskType | None = None
    status: TaskStatus | None = None
    result: List[dict] | None = None
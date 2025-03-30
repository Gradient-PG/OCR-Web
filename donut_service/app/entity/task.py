from dataclasses import dataclass
from enum import Enum

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

class TaskResult(str, Enum):
    """Binary task result enum

    Implies either success or a failure
    """

    SUCCEED = 'succeed'
    FAILED = 'failed'


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
    args: str | None = None  # JSON serialized dict
    status: TaskStatus | None = None
    result: TaskResult | None = None
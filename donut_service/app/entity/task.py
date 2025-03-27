from dataclasses import dataclass
from enum import Enum

DATEFORMAT = '%Y-%m-%dT%H:%M:%S'


class TaskMode(str, Enum):
    """Enumeration of available tasks"""
    ZERO_SHOT = 0
    FEW_SHOT = 1


class Language(str, Enum):
    """Enumeration of available languages"""
    PL = 'pl'
    EN = 'en'


class Framework(str, Enum):
    """Enumeration of available frameworks"""

    STORMTROOPER = 'stormtrooper'
    BULLET = 'bullet'
    TARS = 'tars'
    BIELIK_API = 'bielik_api'


def map_to_enum(language: str, framework: str):
    """Convert string representations of specified language and framework to enums defined within this module.

    This function also provides input validation.
    """
    try:
        language_enum = Language(language)
        framework_enum = Framework(framework)

        if framework_enum == Framework.BIELIK_API and language_enum != Language.PL:
            raise ValueError('Bielik supports only PL language')

        return language_enum, framework_enum

    except ValueError as e:
        raise ValueError(f'Wrong input: {e}') from e


class TaskStatus(str, Enum):
    """Task status enum

    Implies state of the task, one of: PENDING, IN_PROGRESS, COMPLETED
    """
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'


# TODO Change ENUM class to class with real result from model
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
    mode: TaskMode | None = None
    framework: Framework | None = None
    args: str | None = None  # JSON serialized dict
    language: Language | None = None
    status: TaskStatus | None = None
    result: TaskResult | None = None